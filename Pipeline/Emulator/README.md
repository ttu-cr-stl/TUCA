# TUCA-5.1 Emulator

![Version](https://img.shields.io/badge/version-5.1-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-stable-green)

A cycle-accurate emulator for the TUCA-5.1 computer architecture, designed for educational purposes and program verification.

## Features

- **Cycle-Accurate Execution**

  - Precise instruction timing
  - Register state tracking
  - Memory state tracking
  - Branch handling

- **Interactive Debugging**

  - Step-by-step execution
  - Register state inspection
  - Memory visualization
  - Instruction tracing

- **Testing Support**
  - Batch mode for automated testing
  - Memory state verification
  - Expected value checking
  - Integration with build system

## Project Structure

```
Emulator/
├── src/
│   ├── TUCA51_emulator.py  # Core emulator implementation
│   └── run.py              # Command-line interface
└── TUCA51_emulator - Original.py  # Original reference implementation
```

## Usage

The emulator is primarily used through the TUCA build system. For direct usage, see the examples below.

### Operating Modes

#### 1. Interactive Mode (Default)

- Full instruction trace
- Register state after each step
- Memory visualization
- Example output:

  ```
  Instruction Memory:
  0x000: loadpc r5 r6
  0x002: jmp main
  ...

  Register State:
  R0: 0x0000  R4: 0x0000  R8:  0x0000  R12: 0x0000
  R1: 0x0042  R5: 0x0000  R9:  0x0000  R13: 0x0000
  R2: 0x0000  R6: 0x0000  R10: 0x0000  R14: 0x0000
  R3: 0x0000  R7: 0x0000  R11: 0x0000  R15: 0x0000

  Memory Map:
  0x00: 0x42 ✅
  0x01: 0x24 ❓
  0x02: 0x66 ✅
  ```

#### 2. Batch Mode

- Minimal output
- Final memory state only
- Verification results
- Perfect for automated testing
- Example output:
  ```
  0x00=0x42
  0x01=0x24
  0x02=0x66
  ```

### Input File Formats

#### Assembly Program (prog.txt)

```
# Comments start with #
loadpc r5 r6     # Load PC into registers
jmp main         # Jump to main
main:
    ldi 0x42 r1  # Load immediate
    halt         # Stop execution
```

#### Memory Initialization (mem.txt)

```
# Address 0x00
42
# Address 0x01
24
# Address 0x02
66
```

## Development

### Code Style

- Follow PEP 8
- Document all functions
- Keep functions focused and small

## Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines on:

- Code style
- Testing requirements
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.

## Authors

- Juan Carlos Rojas - _Initial work_
- Andres Antillon - _Modifications and improvements_
