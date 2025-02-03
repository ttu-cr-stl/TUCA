# TUCA Assembler

![Version](https://img.shields.io/badge/version-5.1-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-stable-green)

This is an assembler for the TUCA-5.1 instruction set architecture. It converts TUCA assembly language into machine code and can output in various formats suitable for both simulation and hardware implementation.

## Features

- **Assembly Language Support**

  - Full TUCA-5.1 instruction set
  - Label resolution
  - Support for comments and whitespace
  - Flexible instruction formatting

- **Output Formats**

  - Memory initialization files (for emulation and synthesis)
  - Hex format output
  - Error reporting with line numbers

- **Error Handling**
  - Detailed error messages
  - Line number tracking
  - Syntax validation
  - Range checking for immediates
  - Label resolution verification

## Project Structure

```
assembler/
├── src/
│   ├── assembler.py     # Main assembler logic
│   ├── parser.py        # Assembly code parser
│   ├── instruction.py   # Instruction encoding/decoding
│   └── __init__.py      # Package initialization
└── requirements.txt     # Project dependencies
```

## Installation

1. **Set up virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   .\venv\Scripts\activate   # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The assembler is primarily used through the TUCA build system. For direct usage, see the examples below.

### Assembly Language Syntax

#### Basic Instructions

```
# Arithmetic
add r1, r2, r3      # r1 = r2 + r3
sub r1, r2, r3      # r1 = r2 - r3

# Data Movement
ldi 0x42, r1        # r1 = 0x42
load r1, r2         # r1 = mem[r2]

# Control Flow
jmp label           # PC = label
if r1               # Conditional execution
```

#### Labels

```
start:              # Define label
    ldi 0x00, r1    # Initialize r1
loop:               # Loop label
    add r1, r2, r1  # Add r2 to r1
    jmp loop        # Jump back to loop
```

#### Directives

```
.org 0x100          # Set origin address
.word 0x1234        # Define word constant
```

## Development

### Code Style

- Follow PEP 8
- Use type hints
- Document all public functions
- Keep functions focused and small

## Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines on:

- Code style
- Testing requirements
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
