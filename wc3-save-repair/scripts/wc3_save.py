"""Local Warcraft III backup, inspection, and donor checksum repair.

Supports only the observed 68-byte/12-byte/1-MiB W3Z profile.
Copyright (c) 2026 Johann Dirry. MIT license.
"""

import argparse
import binascii
import hashlib
import json
import os
import pathlib
import shutil
import struct
import sys
import zlib
from dataclasses import dataclass


SIGNATURE = b'Warcraft III recorded game\x1a\0'
BLOCK_SIZE = 1048576
MAX_EXPANDED = 1024 * BLOCK_SIZE


def require(condition, message):
    if not condition:
        raise ValueError(message)


def crc32(data):
    return binascii.crc32(data) & 0xffffffff


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(file_path):
    digest = hashlib.sha256()
    with file_path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(BLOCK_SIZE), b''):
            digest.update(chunk)
    return digest.hexdigest()


def header_crc(header):
    copy = bytearray(header)
    copy[-4:] = bytes(4)
    return crc32(copy)


def block_crc(compressed, expanded_size):
    def fold(value):
        return (value ^ (value >> 16)) & 0xffff
    framing = struct.pack('<III', len(compressed), expanded_size, 0)
    return (fold(crc32(compressed)) << 16) | fold(crc32(framing))


def compress(raw):
    stream = zlib.compressobj(1, zlib.DEFLATED, 15, 8, zlib.Z_DEFAULT_STRATEGY)
    return stream.compress(raw) + stream.flush(zlib.Z_SYNC_FLUSH)


def inflate(compressed, expected):
    stream = zlib.decompressobj(15)
    raw = stream.decompress(compressed, expected + 1)
    require(len(raw) == expected, 'Wrong expanded block size.')
    require(not stream.unconsumed_tail and not stream.unused_data, 'Unexpected zlib input or excess expansion.')
    return raw


def decode_settings(encoded):
    result = bytearray()
    mask = 0
    for index, value in enumerate(encoded):
        if index % 8 == 0:
            mask = value
        else:
            result.append(value if mask & (1 << (index % 8)) else value - 1)
    return bytes(result)


def encode_settings(decoded):
    result = bytearray()
    for start in range(0, len(decoded), 7):
        mask = 1
        group = bytearray(decoded[start:start + 7])
        for index, value in enumerate(group):
            if value & 1:
                mask |= 1 << (index + 1)
            else:
                group[index] += 1
        result.append(mask)
        result.extend(group)
    return bytes(result)


def normalized(value):
    return value.replace('\\', '/').lower()


@dataclass
class Identity:
    map_path: str
    checksum: bytes
    settings_start: int
    settings_end: int
    settings: bytes
    plain_offset: int


def identity(raw):
    end = raw.find(b'\0', 0, 256)
    require(end > 0, 'Map path is missing or too long.')
    map_bytes = raw[:end]
    require(all(32 <= value < 127 for value in map_bytes), 'Unsupported map path encoding.')
    map_path = map_bytes.decode('ascii')
    candidates = []
    for start in range(end + 3, min(len(raw), 512)):
        if raw[start - 2:start] != b'\0\0' or raw[start] == 0:
            continue
        stop = raw.find(b'\0', start)
        if stop < start + 16:
            continue
        encoded = raw[start:stop]
        try:
            decoded = decode_settings(encoded)
        except ValueError:
            continue
        if len(decoded) < 14 or encode_settings(decoded) != encoded:
            continue
        name_end = decoded.find(b'\0', 13)
        if name_end < 0:
            continue
        path_bytes = decoded[13:name_end]
        if not all(32 <= value < 127 for value in path_bytes):
            continue
        if normalized(path_bytes.decode('ascii')) != normalized(map_path):
            continue
        slot_start = stop + 9
        if slot_start + 3 > len(raw):
            continue
        slot_size = struct.unpack_from('<H', raw, slot_start)[0]
        slots = raw[slot_start + 2]
        if slots > 24 or slot_size != 1 + slots * 9 + 6:
            continue
        plain_offset = slot_start + 2 + slot_size + 4
        require(plain_offset + 4 <= len(raw), 'Plain map checksum is missing.')
        checksum = decoded[9:13]
        require(raw[plain_offset:plain_offset + 4] == checksum, 'Structured map checksums disagree.')
        candidates.append(Identity(map_path, checksum, start, stop, decoded, plain_offset))
    require(len(candidates) == 1, 'Missing or ambiguous supported map identity.')
    return candidates[0]


@dataclass
class Save:
    data: bytes
    raw_blocks: list
    block_spans: list
    info: Identity
    payload_size: int


def parse_save(data):
    require(len(data) >= 80 and data[:28] == SIGNATURE, 'Unsupported Warcraft III signature.')
    header_size, file_size, version, payload_size, count = struct.unpack_from('<5I', data, 28)
    require(header_size == 68 and version == 1, 'Unsupported container header profile.')
    require(file_size == len(data), 'Truncated file or incorrect stored file size.')
    require(struct.unpack_from('<I', data, 64)[0] == header_crc(data[:68]), 'Invalid header CRC32.')
    require(0 < count <= MAX_EXPANDED // BLOCK_SIZE, 'Block count exceeds supported limits.')
    require((count - 1) * BLOCK_SIZE < payload_size <= count * BLOCK_SIZE, 'Inconsistent payload size.')
    offset = 68
    raw_blocks = []
    spans = []
    for index in range(count):
        require(offset + 12 <= len(data), f'Truncated block header {index}.')
        compressed_size, expanded_size, checksum = struct.unpack_from('<3I', data, offset)
        require(expanded_size == BLOCK_SIZE, 'Unsupported expanded block profile.')
        stop = offset + 12 + compressed_size
        require(compressed_size > 0 and stop <= len(data), f'Truncated block {index}.')
        compressed = data[offset + 12:stop]
        require(block_crc(compressed, expanded_size) == checksum, f'Invalid block CRC {index}.')
        raw_blocks.append(inflate(compressed, expanded_size))
        spans.append((offset, stop))
        offset = stop
    require(offset == len(data), 'Unexpected trailing container bytes.')
    last_used = payload_size - (count - 1) * BLOCK_SIZE
    require(not any(raw_blocks[-1][last_used:]), 'Unverified nonzero payload padding.')
    return Save(data, raw_blocks, spans, identity(raw_blocks[0]), payload_size)


def summary(save):
    return {
        'map_file': save.info.map_path.replace('\\', '/').rsplit('/', 1)[-1],
        'map_checksum_stored_bytes': save.info.checksum.hex(),
        'serialization_build': struct.unpack_from('<H', save.data, 56)[0],
        'game_identifier': save.data[48:52].hex(),
        'game_version_field': struct.unpack_from('<I', save.data, 52)[0],
        'blocks': len(save.raw_blocks),
        'payload_size': save.payload_size,
        'sha256': sha256(save.data),
        'container_verified': True,
        'lua_walk_performed': False,
        'game_load_tested': False,
    }


def repair_bytes(source_data, donor_data):
    source, donor = parse_save(source_data), parse_save(donor_data)
    require(normalized(source.info.map_path) == normalized(donor.info.map_path), 'Donor belongs to a different map.')
    require(source.data[48:56] == donor.data[48:56], 'Game identifier or serialization version differs.')
    old, target = source.info.checksum, donor.info.checksum
    require(old != target, 'Map checksum already matches the donor; no checksum repair is needed.')
    start, stop = source.block_spans[0]
    require(compress(source.raw_blocks[0]) == source.data[start + 12:stop], 'Original compression cannot be reproduced. Check zlib version and framing.')
    raw = bytearray(source.raw_blocks[0])
    decoded = bytearray(source.info.settings)
    decoded[9:13] = target
    encoded = encode_settings(decoded)
    require(len(encoded) == source.info.settings_end - source.info.settings_start, 'Settings encoding length changed.')
    raw[source.info.settings_start:source.info.settings_end] = encoded
    raw[source.info.plain_offset:source.info.plain_offset + 4] = target
    allowed = set(range(source.info.plain_offset, source.info.plain_offset + 4))
    for index in range(9, 13):
        allowed.add(source.info.settings_start + (index // 7) * 8)
        allowed.add(source.info.settings_start + (index // 7) * 8 + 1 + index % 7)
    changed = [index for index, (left, right) in enumerate(zip(source.raw_blocks[0], raw)) if left != right]
    require(set(changed) <= allowed, 'Unintended payload change.')
    compressed = compress(raw)
    block = struct.pack('<III', len(compressed), BLOCK_SIZE, block_crc(compressed, BLOCK_SIZE)) + compressed
    header = bytearray(source.data[:68])
    struct.pack_into('<I', header, 32, 68 + len(block) + len(source.data) - stop)
    struct.pack_into('<I', header, 64, header_crc(header))
    output = bytes(header) + block + source.data[stop:]
    checked = parse_save(output)
    require(checked.info.checksum == target, 'Output map identity failed verification.')
    require(output[48:64] == source.data[48:64], 'Save format or duration changed.')
    require(checked.raw_blocks[0] == bytes(raw), 'First block failed round trip.')
    require(checked.raw_blocks[1:] == source.raw_blocks[1:], 'Later payload blocks changed.')
    require(output[checked.block_spans[0][1]:] == source.data[stop:], 'Later compressed blocks changed.')
    require(checked.payload_size == source.payload_size, 'Payload size changed.')
    return output, {
        **summary(checked),
        'source_sha256': sha256(source_data),
        'donor_sha256': sha256(donor_data),
        'source_checksum_stored_bytes': old.hex(),
        'changed_payload_offsets': changed,
        'scope': 'Map checksum fields only; all other expanded bytes are identical.',
    }


def inventory(root):
    result = []
    for parent, directories, files in os.walk(root, followlinks=False):
        for name in directories + files:
            entry = pathlib.Path(parent) / name
            junction = getattr(entry, 'is_junction', lambda: False)()
            reparse = getattr(entry.lstat(), 'st_file_attributes', 0) & 0x400
            require(not entry.is_symlink() and not junction and not reparse, 'Backup source contains a link or reparse point. Resolve it explicitly first.')
        result.extend((pathlib.Path(parent) / name).relative_to(root) for name in files)
    return sorted(result)


def backup(source, destination):
    require(source.is_dir(), 'Backup source is not a directory.')
    source = source.resolve()
    destination = destination.resolve()
    require(not destination.is_relative_to(source), 'Backup destination must be outside the source tree.')
    require(not destination.exists(), 'Backup destination already exists.')
    entries = inventory(source)
    require(entries, 'Backup source has no files.')
    destination.mkdir(parents=True, exist_ok=False)
    originals = destination / 'Originals'
    originals.mkdir()
    rows = []
    for relative in entries:
        original, target = source / relative, originals / relative
        before_stat = original.stat()
        before = file_hash(original)
        target.parent.mkdir(parents=True, exist_ok=True)
        with original.open('rb') as input_stream, target.open('xb') as output_stream:
            shutil.copyfileobj(input_stream, output_stream, BLOCK_SIZE)
        after_stat = original.stat()
        require(before == file_hash(original) == file_hash(target), 'A source changed or a backup copy failed verification.')
        require((before_stat.st_size, before_stat.st_mtime_ns) == (after_stat.st_size, after_stat.st_mtime_ns), 'Source metadata changed during backup.')
        shutil.copystat(original, target)
        rows.append({'path': relative.as_posix(), 'size': before_stat.st_size, 'mtime_ns': before_stat.st_mtime_ns, 'sha256': before})
    require(entries == inventory(source), 'Source inventory changed during backup.')
    for row in rows:
        require(file_hash(source / row['path']) == row['sha256'], 'A source changed before backup completion.')
        require(file_hash(originals / row['path']) == row['sha256'], 'Backup final hash check failed.')
    manifest = {'source': str(source), 'verified': True, 'files': rows}
    with (destination / 'manifest.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(manifest, stream, indent=2)
    return {'backup': str(destination), 'files': len(rows), 'verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    inspect_parser = commands.add_parser('inspect', help='Validate without writing files.')
    inspect_parser.add_argument('save', type=pathlib.Path)
    backup_parser = commands.add_parser('backup', help='Create a new verified whole-folder backup.')
    backup_parser.add_argument('--source', type=pathlib.Path, required=True)
    backup_parser.add_argument('--destination', type=pathlib.Path, required=True)
    repair_parser = commands.add_parser('repair', help='Create a new donor-based checksum-only candidate.')
    for option in ['source', 'donor', 'output']:
        repair_parser.add_argument('--' + option, type=pathlib.Path, required=True)
    repair_parser.add_argument('--target-build', required=True, help='Verified installed version; provenance must be checked separately.')
    args = parser.parse_args()
    if args.command == 'backup':
        result = backup(args.source, args.destination)
    elif args.command == 'inspect':
        result = summary(parse_save(args.save.read_bytes()))
    else:
        require(not args.output.exists(), 'Output already exists; originals are never overwritten.')
        source_data, donor_data = args.source.read_bytes(), args.donor.read_bytes()
        output, result = repair_bytes(source_data, donor_data)
        require(args.source.read_bytes() == source_data and args.donor.read_bytes() == donor_data, 'An input changed during repair.')
        with args.output.open('xb') as stream:
            stream.write(output)
        reread = args.output.read_bytes()
        require(reread == output, 'Written output failed verification; do not install it.')
        parse_save(reread)
        result.update({'output': str(args.output), 'target_build_label': args.target_build, 'donor_provenance_verified_by_tool': False})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zlib.error, struct.error) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(2)
