# TUCA Processor Implementation

This directory contains the Verilog implementation of the TUCA processor.

## Directory Structure

```
Processor/
├── src/              # Verilog source files
├── testbench/        # Testbench files
└── build/            # Build artifacts
```

## Integration with Build System

The Verilog implementation integrates with the TUCA build system by:

1. Reading compiled programs (`.mem` files) from `Programs/hw*/build/`
2. Running simulations with test memory files
3. Outputting results to `Programs/hw*/build/results/verilog/*.txt`

### Memory File Format

The testbench reads initial memory states from text files where:

- Each line number corresponds to its memory address (line 1 = address 0x00, line 2 = address 0x01, etc.)
- Values should be in hex format (with or without 0x prefix)
- Empty lines and lines starting with # are ignored
- If you provide less than 256 values, the rest of the memory positions will be filled with zeros

Example memory file:

```
# Initial memory state
42    # mem[0x00] = 0x42 (line 1)
24    # mem[0x01] = 0x24 (line 2)
66    # mem[0x02] = 0x66 (line 3)
```

### Result Format

The simulation must output memory dumps in the following format for compatibility with the verification system:

```
# build/results/verilog/test1.txt
0x02=0x42  # memory[0x02] = 0x42
0x03=0xFF  # memory[0x03] = 0xFF
```

Note: Both addresses and values must include the `0x` prefix for proper verification.

## Running Simulations

[TODO: Add instructions for running Verilog simulations]

## Implementation Details

[TODO: Add processor architecture and implementation details]

## Testing

[TODO: Add testing documentation]
