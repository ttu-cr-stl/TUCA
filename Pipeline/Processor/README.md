# TUCA Processor Implementation

![Version](https://img.shields.io/badge/version-5.1-blue)
![Verilog](https://img.shields.io/badge/verilog-2005-blue)
![Status](https://img.shields.io/badge/status-stable-green)

A complete hardware implementation of the TUCA-5.1 processor in Verilog, featuring a 5-stage pipeline, hazard detection, and forwarding logic.

## Features

- **Pipeline Architecture**

  - 5-stage pipeline (Fetch, Decode, Execute, Memory, Writeback)
  - Hazard detection and resolution
  - Data forwarding for pipeline optimization
  - Branch prediction

- **Memory System**

  - Harvard architecture
  - Separate instruction and data memory
  - Memory-mapped I/O support
  - Configurable memory sizes

- **Verification Infrastructure**
  - Testbench infrastructure
  - Self-checking test cases
  - Integration with build system

## Directory Structure

```
Processor/
├── src/              # RTL source files
├── testbench/        # Verification files
└── tests/            # Test programs and data
```

## RTL Implementation

### Pipeline Stages

1. **Fetch Stage**

   - Program counter management
   - Instruction memory interface
   - Branch target calculation

2. **Decode Stage**

   - Instruction decoding
   - Register file access
   - Immediate value generation
   - Branch condition evaluation

3. **Execute Stage**

   - ALU operations
   - Address calculation
   - Branch resolution
   - Forwarding mux control

4. **Memory Stage**

   - Data memory access
   - Memory-mapped I/O
   - Write-back data selection

5. **Writeback Stage**
   - Register file write back
   - Result forwarding
   - Pipeline control

### Key Components

#### Register File

```verilog
module register_file (
    input  wire        clk,
    input  wire        rst_n,
    input  wire [3:0]  rd_addr1,
    input  wire [3:0]  rd_addr2,
    input  wire [3:0]  wr_addr,
    input  wire [15:0] wr_data,
    input  wire        wr_en,
    output wire [15:0] rd_data1,
    output wire [15:0] rd_data2
);
```

#### ALU

```verilog
module alu (
    input  wire [15:0] a,
    input  wire [15:0] b,
    input  wire [3:0]  op,
    output wire [15:0] result,
    output wire        zero
);
```

## Integration with Build System

### Memory File Format

The processor reads memory initialization files in hex format:

```
// prog.mem
@000 // Address 0x000
42   // Data 0x42
24   // Data 0x24
66   // Data 0x66
```

### Result Format

Simulation results are written in a standardized format:

```
// results.txt
0x02=0x42  # memory[0x02] = 0x42
0x03=0xFF  # memory[0x03] = 0xFF
```

## Development

### Tool Requirements

- Verilog simulator (e.g., Icarus Verilog)
- Waveform viewer (e.g., GTKWave)
- Python for test automation

### Coding Guidelines

- Follow Verilog-2005 standard
- Use synchronous design practices
- Document all module interfaces
- Include assertions for verification

## Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines on:

- RTL coding style
- Verification requirements
- Pull request process

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
