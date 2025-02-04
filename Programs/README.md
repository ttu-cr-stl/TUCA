# TUCA Programs

This directory contains TUCA assembly programs and their associated test cases. Each program is organized in its own directory (e.g., `prog1/`, `prog2/`, etc.) with a standardized structure.

## Directory Structure

Each program directory should follow this structure:

```
prog1/                    # Program directory
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

- Each line represents a sequential memory address starting from 0x00
- Values must be either:
  - Binary format (all 1s and 0s), or
  - Hex format with 0x prefix (e.g., `0x42`)
- Values must come first in the file, before any comments
- Comments (starting with #) and empty lines are only allowed AFTER all memory values
- If a comment or empty line appears before values, it will be treated as a memory location with value 0x00

Example:

```
0x42    # This will be at memory[0x00]
0x24    # This will be at memory[0x01]
0x66    # This will be at memory[0x02]
# Any comments after values are fine
# They won't affect memory initialization
```

❗ Important: Never put comments or empty lines before your memory values. This:

```
# This comment will be treated as memory[0x00] = 0x00
0x42    # Now this will be at memory[0x01] instead of 0x00!
0x24    # This will be at memory[0x02]
```

The rest of memory (addresses not specified) will be initialized to 0x00.

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
