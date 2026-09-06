# Barcode Reader for Dify

A small Dify Tool Plugin that decodes common 1D/2D barcodes from an uploaded image.

The image is processed inside the plugin runtime. This plugin does not call an external barcode API.

## Supported flow

```text
Dify User Input (image)
        ↓
Read Barcode Tool
        ↓
barcode / format / found
        ↓
Database Plugin
        ↓
SQL Server
```

## Development

Python 3.12 is recommended.

```bash
pip install -r requirements.txt
```

For remote debugging, copy `.env.example` to `.env` and set the values shown by Dify's Plugin debug screen.

```bash
python -m main
```

## Packaging

Use the official Dify Plugin CLI:

```bash
dify plugin package . -o barcode_reader-0.0.1.difypkg
```

Do not include `.env` in the package.

## Workflow outputs

- `found`: boolean
- `barcode`: first decoded barcode value
- `format`: detected format
- `count`: number of detected codes
- `all_barcodes`: all decoded values

## Notes

Barcode recognition quality depends on focus, lighting, image resolution, angle, and quiet zone around the code.
