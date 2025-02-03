# TUCA (TTU Computer Architecture)

TUCA is a computer architecture developed at Texas Tech University for educational purposes. This repository contains the assembler, emulator, and Verilog implementation, along with a comprehensive build and testing system.

## Project Structure

```
TUCA/
├── Pipeline/          # Core TUCA implementation
│   ├── Assembler/    # Assembly to machine code
│   │   └── src/      # Assembler source code
│   ├── Emulator/     # Software implementation
│   │   └── src/      # Emulator source code
│   └── Processor/    # Hardware implementation
│       ├── src/      # Verilog source files
│       └── testbench/# Verilog testbenches
├── Programs/          # Assembly programs and tests
│   └── example1/     # Example program
│       ├── prog.txt      # Assembly program
│       ├── config.json   # Test configuration
│       ├── test_mems/    # Test memory files
│       │   ├── test1.txt
│       │   └── test2.txt
│       ├── build/        # Build artifacts
│       │   └── prog.mem      # Compiled program
│       └── results/      # Test results
│           ├── emulator/     # Emulator results
│           │   └── test1.txt
│           ├── verilog/      # Verilog results
│           │   └── test1.txt
│           └── verify/       # Verification reports
│               └── test1.txt
├── Examples/         # Example programs
├── Docs/            # Documentation
└── scripts/         # Build and test tools
    ├── build.py     # Build system
    ├── verify.py    # Result verification
    └── tuca         # Command-line interface
```

## Quick Start

1. **Create a New Program**:

   ```bash
   # Create program directory
   mkdir -p Programs/example1/test_mems

   # Write your assembly program
   vim Programs/example1/prog.txt

   # Create test memory files
   vim Programs/example1/test_mems/test1.txt
   ```

2. **Configure Tests**:
   Create `Programs/example1/config.json`:

   ```json
   {
     "program": "prog.txt",
     "test_cases": [
       {
         "name": "test1",
         "memory": "test_mems/test1.txt",
         "expected": {
           "memory": {
             "0x02": "0x10"
           }
         }
       }
     ]
   }
   ```

3. **Build and Test**:

   ```bash
   # Build program
   tuca build example1

   # Run emulator tests
   tuca emu example1 test1     # Run single test
   tuca emu example1 all       # Run all tests

   # Verify against Verilog
   tuca verify example1 test1
   ```

## Build System

The `tuca` command provides a unified interface for all development tasks:

### Building Programs

```bash
tuca build example1          # Build program
```

### Running Tests

```bash
tuca emu example1 test1      # Run specific test
tuca emu example1 all        # Run all tests
```

The emulator supports two operating modes:

1. **Interactive Mode** (Default):

   - Shows full instruction execution details
   - Perfect for debugging and understanding program flow

2. **Minimal Mode** (Test Mode):
   - Only shows final memory state and verification results
   - Used automatically when running tests

### Verifying Results

```bash
tuca verify example1 test1   # Compare emulator vs Verilog
```

### Cleaning Build Artifacts

```bash
tuca clean              # Clean all
tuca clean example1     # Clean specific program
```

## Test Results

The build system generates three types of results:

1. **Emulator Results** (`results/emulator/`):

   - Output from running program through emulator
   - Format: `0xAA=0xBB` (hex addresses and values)

   ```
   0x02=0x42  # memory[0x02] = 0x42
   0x03=0xFF  # memory[0x03] = 0xFF
   ```

2. **Verilog Results** (`results/verilog/`):

   - Output from Verilog simulation
   - Same format as emulator for easy comparison

3. **Verification Reports** (`results/verify/`):
   - Detailed comparison of emulator vs Verilog
   - Shows expected values from config.json
   - Highlights any mismatches with ❌
   - Shows ✅ when all values match

## Documentation

- [Assembler Documentation](Pipeline/Assembler/README.md)
- [Emulator Documentation](Pipeline/Emulator/README.md)
- [Processor Documentation](Pipeline/Processor/README.md)

## Contributing

[Add contribution guidelines here]

## License

[Add license information here]
