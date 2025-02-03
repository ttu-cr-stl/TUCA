# TUCA Pipeline

This directory contains the core implementation components of the TUCA architecture:

## Components

### [Assembler](Assembler/)

- Converts TUCA assembly code to machine code
- Handles labels, macros, and instruction encoding
- Outputs `.mem` files for emulation and synthesis

### [Emulator](Emulator/)

- Software implementation of the TUCA processor
- Supports interactive debugging and batch testing
- Verifies program behavior before hardware implementation

### [Processor](Processor/)

- Hardware implementation in Verilog
- Includes testbenches and simulation infrastructure
- Target for synthesis and FPGA implementation

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

1. Assembler converts programs to machine code
2. Both Emulator and Processor execute the same machine code
3. Results are compared to verify correctness
