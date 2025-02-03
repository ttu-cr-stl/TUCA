# TUCA Assembler

This is an assembler for the TUCA-5.1 instruction set architecture. It converts TUCA assembly language into machine code and can output in various formats suitable for both simulation and hardware implementation.

## Features

- Converts TUCA assembly (.txt) to binary format
- Supports output in multiple formats:
  - Raw binary
  - Hex format (for Verilog simulation)
  - Memory initialization files

## Project Structure

```
assembler/
├── src/
│   ├── assembler.py     # Main assembler logic
│   ├── parser.py        # Assembly code parser
│   └── instruction.py   # Instruction encoding/decoding
└── requirements.txt     # Project dependencies
```

## Usage

```bash
# Coming soon
```

## Development

1. Set up virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```
