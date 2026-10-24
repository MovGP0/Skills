import contextlib
import io
import pathlib
import struct
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
import wc3_save as tool


def fixture(checksum=b'\x10\x20\x30\x40', map_path='Campaign\\Example\\Map01.w3xd', build=7000):
    path_bytes = map_path.encode('ascii')
    settings = bytes(9) + checksum + path_bytes + b'\0' + b'Player\0'
    encoded = tool.encode_settings(settings)
    first = bytearray(path_bytes + b'\0' + bytes(4) + b'Local Game\0\0' + encoded + bytes(9))
    first.extend(struct.pack('<H', 16) + b'\x01' + bytes(15))
    first.extend(b'KEEP' + checksum + b'unchanged saved data')
    first.extend(bytes(tool.BLOCK_SIZE - len(first)))
    later = bytes(range(32))
    raws = [bytes(first), later + bytes(tool.BLOCK_SIZE - len(later))]
    body = bytearray()
    for raw in raws:
        compressed = tool.compress(raw)
        body.extend(struct.pack('<III', len(compressed), tool.BLOCK_SIZE, tool.block_crc(compressed, tool.BLOCK_SIZE)))
        body.extend(compressed)
    header = bytearray(tool.SIGNATURE + bytes(40))
    struct.pack_into('<5I', header, 28, 68, 68 + len(body), 1, tool.BLOCK_SIZE + 32, 2)
    struct.pack_into('<IIHHI', header, 48, 0x57335850, 10200, build, 0, 12345)
    struct.pack_into('<I', header, 64, tool.header_crc(header))
    return bytes(header + body)


class SaveTests(unittest.TestCase):
    def test_crc_standard_vector(self):
        self.assertEqual(tool.crc32(b'123456789'), 0xcbf43926)

    def test_settings_roundtrip_all_bytes(self):
        data = bytes(range(256))
        self.assertEqual(tool.decode_settings(tool.encode_settings(data)), data)

    def test_repair_changes_only_identity_and_preserves_build_and_later_blocks(self):
        source = fixture()
        donor = fixture(b'\xab\xcd\xef\x01', build=7003)
        output, report = tool.repair_bytes(source, donor)
        before, after = tool.parse_save(source), tool.parse_save(output)
        self.assertEqual(after.info.checksum, b'\xab\xcd\xef\x01')
        self.assertEqual(output[48:64], source[48:64])
        self.assertEqual(after.raw_blocks[1:], before.raw_blocks[1:])
        self.assertEqual(output[after.block_spans[0][1]:], source[before.block_spans[0][1]:])
        self.assertEqual(after.raw_blocks[0][after.info.plain_offset - 4:after.info.plain_offset], b'KEEP')
        allowed = set(report['changed_payload_offsets'])
        self.assertLessEqual(len(allowed), 10)
        for index, (left, right) in enumerate(zip(before.raw_blocks[0], after.raw_blocks[0])):
            if index not in allowed:
                self.assertEqual(left, right)

    def test_same_map_accepts_slash_and_case_variants(self):
        output, _ = tool.repair_bytes(fixture(), fixture(b'\x01\x02\x03\x04', 'campaign/example/map01.w3xd'))
        self.assertEqual(tool.parse_save(output).info.checksum, b'\x01\x02\x03\x04')

    def test_different_map_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'different map'):
            tool.repair_bytes(fixture(), fixture(b'\x01\x02\x03\x04', 'Campaign/Example/Map02.w3xd'))

    def test_already_matching_checksum_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'already matches'):
            tool.repair_bytes(fixture(), fixture())

    def test_corrupt_header_is_rejected(self):
        data = bytearray(fixture())
        data[60] ^= 1
        with self.assertRaisesRegex(ValueError, 'header CRC'):
            tool.parse_save(bytes(data))

    def test_corrupt_block_is_rejected(self):
        data = bytearray(fixture())
        data[90] ^= 1
        with self.assertRaisesRegex(ValueError, 'block CRC'):
            tool.parse_save(bytes(data))

    def test_truncation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Truncated'):
            tool.parse_save(fixture()[:-1])

    def test_noncanonical_compression_is_rejected(self):
        data = fixture()
        parsed = tool.parse_save(data)
        import zlib
        compressed = zlib.compress(parsed.raw_blocks[0], 9)
        block = struct.pack('<III', len(compressed), tool.BLOCK_SIZE, tool.block_crc(compressed, tool.BLOCK_SIZE)) + compressed
        header = bytearray(data[:68])
        body = block + data[parsed.block_spans[0][1]:]
        struct.pack_into('<I', header, 32, 68 + len(body))
        struct.pack_into('<I', header, 64, tool.header_crc(header))
        with self.assertRaisesRegex(ValueError, 'compression cannot be reproduced'):
            tool.repair_bytes(bytes(header) + body, fixture(b'\x01\x02\x03\x04'))

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            output = root / 'original.w3z'
            output.write_bytes(b'never overwrite')
            args = ['wc3_save.py', 'repair', '--source', str(root / 'missing.w3z'), '--donor', str(root / 'missing2.w3z'), '--output', str(output), '--target-build', 'example']
            with mock.patch.object(sys, 'argv', args):
                with self.assertRaisesRegex(ValueError, 'already exists'):
                    tool.main()
            self.assertEqual(output.read_bytes(), b'never overwrite')

    def test_cli_writes_verified_new_file_without_modifying_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source, donor, output = [root / name for name in ['old.w3z', 'fresh.w3z', 'new.w3z']]
            source.write_bytes(fixture())
            donor.write_bytes(fixture(b'\x01\x02\x03\x04'))
            before = [source.read_bytes(), donor.read_bytes()]
            args = ['wc3_save.py', 'repair', '--source', str(source), '--donor', str(donor), '--output', str(output), '--target-build', 'verified-by-agent']
            with mock.patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
                tool.main()
            self.assertEqual([source.read_bytes(), donor.read_bytes()], before)
            self.assertEqual(tool.parse_save(output.read_bytes()).info.checksum, b'\x01\x02\x03\x04')


class BackupTests(unittest.TestCase):
    def test_backup_includes_nested_non_save_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / 'campaign'
            (source / 'zones').mkdir(parents=True)
            (source / 'zones/Map01.w3z').write_bytes(b'save')
            (source / 'Campaigns.w3v').write_bytes(b'cache')
            result = tool.backup(source, root / 'backup')
            self.assertTrue(result['verified'])
            self.assertEqual(result['files'], 2)
            self.assertEqual((root / 'backup/Originals/Campaigns.w3v').read_bytes(), b'cache')
            self.assertTrue((root / 'backup/manifest.json').is_file())

    def test_backup_rejects_existing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                tool.backup(root, root.parent)

    def test_backup_rejects_destination_inside_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with self.assertRaisesRegex(ValueError, 'outside'):
                tool.backup(root, root / 'bad-backup')

    def test_changed_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / 'campaign'
            source.mkdir()
            (source / 'state.w3v').write_bytes(b'original')
            with mock.patch.object(tool, 'file_hash', side_effect=['before', 'after']):
                with self.assertRaisesRegex(ValueError, 'source changed'):
                    tool.backup(source, root / 'backup')
            self.assertFalse((root / 'backup/manifest.json').exists())


if __name__ == '__main__':
    unittest.main()
