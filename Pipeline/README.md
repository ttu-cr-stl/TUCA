# TUCA Pipeline

![Status](https://img.shields.io/badge/status-stable-green)
![Version](https://img.shields.io/badge/version-5.1-blue)

This directory contains the core implementation components of the TUCA architecture, a complete educational computer architecture designed to demonstrate fundamental concepts in computer organization and design.

## Architecture Overview

TUCA-5.1 is a 16-bit RISC architecture featuring:

- 16-bit data path
- 16 general-purpose registers
- Memory-mapped I/O
- Simple but complete instruction set
- 5-stage pipeline implementation
- Harvard architecture (separate instruction and data memory)

## Components

### [Assembler](Assembler/)

- Converts TUCA assembly code to machine code
- Handles labels, macros, and instruction encoding
- Outputs `.mem` files for emulation and synthesis
- Provides detailed error messages and warnings
- Supports multiple output formats

### [Emulator](Emulator/)

- Software implementation of the TUCA processor
- Supports interactive debugging and batch testing
- Verifies program behavior before hardware implementation
- Provides cycle-accurate execution
- Includes memory and register visualization

### [Processor](Processor/)

- Hardware implementation in Verilog
- Includes testbenches and simulation infrastructure
- Target for synthesis and FPGA implementation
- Implements full 5-stage pipeline
- Includes hazard detection and forwarding

## Directory Structure

```
Pipeline/
├── Assembler/         # Assembly to machine code
│   ├── src/          # Assembler source code
│   └── tests/        # Assembler tests
├── Emulator/         # Software implementation
│   ├── src/          # Emulator source code
│   └── tests/        # Emulator tests
└── Processor/        # Hardware implementation
    ├── src/          # Verilog source files
    └── testbench/    # Verilog testbenches
```

## Build and Test

Each component has its own build and test infrastructure. See the individual component READMEs for details:

- [Assembler Documentation](Assembler/README.md)
- [Emulator Documentation](Emulator/README.md)
- [Processor Documentation](Processor/README.md)

## Integration

The components work together in the TUCA toolchain:

1. **Assembly to Machine Code**

   - Assembler parses TUCA assembly programs
   - Generates memory initialization files
   - Supports both emulator and hardware targets

2. **Verification Flow**

   - Emulator directly interprets assembly code
   - Processor executes compiled machine code
   - Results are compared for correctness
   - Automated testing infrastructure

3. **Development Cycle**
   - Write and test in emulator for quick iteration
   - Verify behavior in hardware implementation
   - Use debugging tools for issue resolution
   - Automated regression testing

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on:

- Code style and formatting
- Testing requirements
- Pull request process
- Documentation standards

## License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.
