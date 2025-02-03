# TUCA Programs

This directory contains TUCA assembly programs and their associated test cases. Each program is organized in its own directory (e.g., `hw1/`, `hw2/`, etc.) with a standardized structure.

## Directory Structure

Each program directory should follow this structure:

```
hw1/                    # Program directory
├── prog.txt           # Main assembly program
├── config.json        # Test configuration
├── test_mems/         # Test memory files
│   ├── mem1.txt       # Initial memory state for test 1
│   ├── mem2.txt       # Initial memory state for test 2
│   └── ...
└── build/             # Build artifacts (auto-generated)
    ├── prog.mem       # Compiled program
    └── results/       # Test results
        ├── emulator/  # Emulator output
        │   ├── mem1.txt
        │   └── mem2.txt
        ├── verilog/   # Verilog simulation output
        │   ├── mem1.txt
        │   └── mem2.txt
        └── verify/    # Verification reports
            ├── mem1.txt
            └── mem2.txt
```

## File Formats

### Assembly Program (`prog.txt`)

- One instruction per line
- Comments start with `#`
- Labels end with `:`
- Example:
  ```assembly
  # Program to add two numbers
  ld 0x00 r0      # Load first number
  ld 0x01 r1      # Load second number
  add r0 r1 r2    # Add them
  st r2 0x02      # Store result
  halt            # Stop execution
  ```

### Test Memory Files (`test_mems/*.txt`)

- Each line number corresponds to its memory address (line 1 = address 0x00, line 2 = address 0x01, etc.)
- Values are in hex format (with or without 0x prefix)
- Empty lines or lines starting with # are ignored
- If you provide less than 256 values, the rest of the memory positions will be filled with zeros
- Example:
  ```
  # Memory initialization
  42    # mem[0x00] = 0x42 (line 1)
  24    # mem[0x01] = 0x24 (line 2)
  66    # mem[0x02] = 0x66 (line 3)
  ```
  This initializes:
  - Memory address 0x00 with value 0x42
  - Memory address 0x01 with value 0x24
  - Memory address 0x02 with value 0x66
  - All remaining memory positions are filled with zeros

### Configuration File (`config.json`)

```json
{
  "program": "prog.txt",
  "test_cases": [
    {
      "name": "test_mem1",
      "memory": "test_mems/mem1.txt",
      "expected": {
        "memory": {
          "0x02": "0x66"  # Expected result at address 0x02
        }
      }
    }
  ]
}
```

### Result Files (auto-generated)

1. **Emulator Results** (`build/results/emulator/*.txt`):

   ```
   0x02=0x66  # memory[0x02] = 0x66
   ```

2. **Verilog Results** (`build/results/verilog/*.txt`):

   ```
   0x02=0x66  # memory[0x02] = 0x66
   ```

3. **Verification Reports** (`build/results/verify/*.txt`):
   ```
   Checking expected memory location 0x02:
     Expected: 0x66
     Emulator: 0x66
     Verilog:  0x66
     ✅ All results match!
   ```

## Running Tests

Use the `tuca` command-line tool to run tests:

```bash
# Run a single test
tuca emu hw1 mem1

# Run all tests in a program
tuca emu hw1 all

# Verify against Verilog
tuca verify hw1 mem1
```

## Test Modes

1. **Interactive Mode** (Default):

   ```bash
   # Shows full execution details
   tuca emu hw1 mem1
   ```

2. **Minimal Mode** (Automated Testing):
   ```bash
   # Only shows final state and verification
   tuca emu hw1 all
   ```
