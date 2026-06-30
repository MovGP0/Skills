---
name: translations
description: Explains LocalExIm LCX and LCXZ translation file formats, compression headers, XML structure, RESX export rules, and language fallback behavior. Use when reading, writing, converting, or validating translation files.
---
# Translation Files

LocalExIm uses two file extensions for translation editor files:

- `.lcx`: uncompressed XML.
- `.lcxz`: compressed LCX XML.

Both formats contain the same XML model. The compressed `.lcxz` format adds a fixed file header and Deflate compression.

## LCX

An `.lcx` file is a plain XML document. It can be opened with `XElement.Load(...)` and saved with `XElement.Save(...)`.

The root element is:

```xml
<Locales xmlns="..."
         version="1"
         created="..."
         modified="..."
         xml:space="preserve">
```

The file contains:

- `Languages`: one `Language` element per localized language, using names such as `de`, `de-ch`, `en-gb`, `pl`, or `zh`.
- `Entry`: one localizable resource entry.
- `Default`: the neutral language value.
- `Translation`: one translated value for a language.
- `O`: original text.
- `M`: modified text, used when the editor stores a changed value.

Resource IDs are repository-relative resource paths plus the RESX key, for example:

```text
Some.Project.Name/i18n/LocalizedStrings/FooBar
```
maps to
```text
./Some.Project.Name/i18n/LocalizedStrings.resx
```
```xml
<data name="FooBar">
  <value>...</value>
</data>
```

## LCXZ

An `.lcxz` file is:

1. A 12-byte ASCII header: `MSEALCXZ0010`.
2. A .NET `DeflateStream` payload.
3. The decompressed payload is UTF-8 encoded LCX XML.

This is not a ZIP file and not GZip. It is raw .NET Deflate data after the LocalExIm header.

## Reading LCXZ

To read an `.lcxz` file:

1. Open the file as bytes or a stream.
2. Read and validate the first 12 bytes as ASCII `MSEALCXZ0010`.
3. Deflate-decompress the remaining stream.
4. Decode the decompressed bytes as UTF-8 text.
5. Parse the text as LCX XML.

```csharp
using System.IO.Compression;
using System.Text;
using System.Xml.Linq;

static XDocument ReadLcxz(string path)
{
    var expectedHeader = Encoding.ASCII.GetBytes("MSEALCXZ0010");

    using var input = File.OpenRead(path);
    var header = new byte[expectedHeader.Length];
    if (input.Read(header, 0, header.Length) != header.Length ||
        !header.SequenceEqual(expectedHeader))
    {
        throw new InvalidDataException("Unsupported LCXZ header.");
    }

    using var deflate = new DeflateStream(input, CompressionMode.Decompress);
    using var reader = new StreamReader(deflate, Encoding.UTF8);
    var xml = reader.ReadToEnd();

    return XDocument.Parse(xml, LoadOptions.PreserveWhitespace);
}
```

## Writing LCXZ

To write an `.lcxz` file:

1. Build the LCX XML document.
2. Serialize it as XML text.
3. Encode the XML text as UTF-8 bytes.
4. Create the output file.
5. Write the ASCII header `MSEALCXZ0010`.
6. Write the UTF-8 bytes through a .NET `DeflateStream`.

```csharp
using System.IO.Compression;
using System.Text;
using System.Xml.Linq;

static void WriteLcxz(string path, XDocument document)
{
    var header = Encoding.ASCII.GetBytes("MSEALCXZ0010");
    var xml = document.ToString(SaveOptions.OmitDuplicateNamespaces);
    var payload = Encoding.UTF8.GetBytes(xml);

    using var output = File.Create(path);
    output.Write(header, 0, header.Length);

    using var deflate = new DeflateStream(output, CompressionMode.Compress, leaveOpen: true);
    deflate.Write(payload, 0, payload.Length);
}
```

## Reading LCX

To read an uncompressed `.lcx` file, load it directly as XML:

```csharp
using System.Xml.Linq;

static XDocument ReadLcx(string path)
{
    return XDocument.Load(path, LoadOptions.PreserveWhitespace);
}
```

## Writing LCX

To write an uncompressed `.lcx` file, save the XML document directly:

```csharp
using System.Xml.Linq;

static void WriteLcx(string path, XDocument document)
{
    document.Save(path, SaveOptions.OmitDuplicateNamespaces);
}
```

## RESX Export Notes

- Language names in LCX/LCXZ files are lower-case, for example `de-ch`, `en-gb`, and `pt-br`.
- Language names in RESX files are following the ISO 639-2 and IETF BCP 47 standard, for example `de` and `de-AT`.
- Language neutral values come from `<ResourceFileName>.resx`.
- Localized values come from `<ResourceFileName>.<language>.resx` 
- Regionally localized values come from `<ResourceFileName>.<language>-<REGION>.resx`
- Localized files can omit entries when they should fall back to the neutral value.
- The neutral language is US english (`en`/`en-US`) and used as fallback. Therefore `*.en.resx`/`*.en-US.resx` files are omitted.
- The default region for english is `en-US` and the default region for german is `de-DE`, therefore those files are omitted.
- When a string is the same in a language file (e.g. `*.en.resx`, `*.de.resx`) as in the neutral-language file (`*.resx`), the value can be omitted from the language file.
- When a string is the same in the regional language (e.g. `*.en-GB.resx`, `*.de-AT.resx`, `*.de-CH.resx`) and the primary language (e.g. `*.en.resx`, `*.de.resx`), the regional value can be omitted.
