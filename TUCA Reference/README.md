# TUCA-5.1 Assembly Language Reference Manual

This document describes the assembly language syntax for TTU Computer Architecture, version 5.1 (TUCA-5.1).

## General Description

The TUCA-5.1 architecture is an 8-bit machine that follows a GPR load-store architecture. It has 16 general purpose registers labeled r0 to r15, an 8-bit ALU, and a 256-byte programmable 8-bit data memory with addresses from 0 to 0xFF.

It also has an instruction memory of up to 4096 bytes, with a fixed-length encoding of 2 bytes per instruction.

### Key Features

- Written in plain text, one instruction per line
- Instructions followed by operands, separated by spaces
- Operand order matches TUCA-5 Computer Architecture Specification
- Registers specified as "r0" to "r15"
- Memory addresses specified in hexadecimal with "0x" prefix

## Instruction Set

### Load/Store Instructions

| Instruction     | Description                                                                                |
| --------------- | ------------------------------------------------------------------------------------------ |
| `ld addr reg`   | Loads the 8-bit value from memory at location `addr` into the register `reg`               |
| `ldr reg1 reg2` | Loads the 8-bit value from memory at a location stored in `reg1`, into the register `reg2` |
| `ldi val reg`   | Loads the 8-bit value `val` into the register `reg`                                        |
| `st reg addr`   | Stores the 8-bit value in register `reg` into the memory at location `addr`                |
| `str reg1 reg2` | Stores the 8-bit value in `reg1` into the memory at a location stored in `reg2`            |

### Arithmetic & Logic Instructions

| Instruction          | Description                                                                      |
| -------------------- | -------------------------------------------------------------------------------- |
| `add reg1 reg2 reg3` | Adds the values in `reg1` and `reg2` and puts the result in `reg3`               |
| `and reg1 reg2 reg3` | Performs bitwise AND between `reg1` and `reg2` and puts the result in `reg3`     |
| `or reg1 reg2 reg3`  | Performs bitwise OR between `reg1` and `reg2` and puts the result in `reg3`      |
| `not reg1 reg2`      | Performs bitwise NOT on `reg1` and puts the result in `reg2`                     |
| `neg reg1 reg2`      | Negates the value in `reg1` using two's complement and puts the result in `reg2` |

### Bit Manipulation Instructions

| Instruction       | Description                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------ |
| `shl reg1 n reg2` | Left-shifts the value in `reg1` by `n` bits and puts the result in `reg2`. `n` is a value from 1 to 7  |
| `shr reg1 n reg2` | Right-shifts the value in `reg1` by `n` bits and puts the result in `reg2`. `n` is a value from 1 to 7 |

### Comparison and Conditional Execution Instructions

| Instruction         | Description                                                                                                                         |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `eq reg1 reg2 reg3` | Puts a 1 in `reg3` if the value of `reg1` is equal to that of `reg2`. Otherwise puts 0                                              |
| `gt reg1 reg2 reg3` | Puts a 1 in `reg3` if the value of `reg1` is greater than that of `reg2`. Otherwise puts 0. Note: interprets all values as unsigned |
| `if reg1`           | Execute the next instruction if the value of `reg1` is non-zero. Otherwise skip it                                                  |
| `skipif reg1`       | Skip the next instruction if the value of `reg1` is non-zero                                                                        |

### Branch and Program Control Instructions

| Instruction            | Description                                                                                                                                                                                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `jmp addr`             | Jumps and continues execution starting with the instruction stored at location `addr` of the instruction memory                                                                                                                                                          |
| `jmpr reg_hi reg_lo`   | Jumps and continues execution starting with instructions stored at a location of instruction memory stored in `reg_hi` & `reg_lo`. Instruction addresses are 12 bits. The 4 most significant bits are read from `reg_hi`, and the 8 least significant bits from `reg_lo` |
| `loadpc reg_hi reg_lo` | Saves the contents of the current program counter (PC) into registers `reg_hi` & `reg_lo`. The PC is a 12-bit address, whose most significant 4 bits will be stored in `reg_hi`, and the least significant 8 bits in `reg_lo`                                            |
| `halt`                 | Terminates the program                                                                                                                                                                                                                                                   |

## Comments and Whitespace

- Any line beginning with the "#" character will be considered a comment line and ignored
- Empty lines will be ignored

## Pre-processor Macro Definitions

- Macro definitions are supported for replacing any part of an instruction with a more meaningful name
- Can be used to replace register names, memory addresses, etc.
- Format: `def name value`
  - Example: `def counter r5`

## Variables

Named variables are supported in the form of macro definitions that can be used instead of a fixed memory address.

### Example:

| Instruction    | Description                                                                  |
| -------------- | ---------------------------------------------------------------------------- |
| `def src 0x01` | Defines variables "src" and "dst" to point to memory addresses 0x01 and 0x02 |
| `def dst 0x02` | respectively                                                                 |
| `ld src r1`    | Loads from memory location 0x01 into register r1                             |
| `add r0 r1 r2` | Adds the values from registers r0 and r1 into r2                             |
| `st r2 dst`    | Stores the value in register r2 into memory address 0x02                     |

## Address Labels and Jumps

Symbolic address labels can be added into a line by using the syntax: `label:` starting at the beginning of a line. Nothing else should follow on the same line.

### Example:

```assembly
loop1:              # Defines the label "loop1"
add r0 r1 r0       # Adds the values from registers r0 and r1 into r0
skipif r2          # Skip the next instruction if r2 is non-zero
jmp loop1          # Jump to the instruction starting immediately following the "loop1" label
```

## Dynamic Jumps

The `jmpr` instruction allows making jumps to addresses computed by the program. These are generally paired with the use of the `loadpc` instruction, to read the program counter.

### Example:

| Instruction Address | Instruction  | Description                                                  |
| ------------------- | ------------ | ------------------------------------------------------------ |
| 0x000               | loadpc r5 r6 | Store the current instruction address into r5 (hi) & r6 (lo) |
| 0x002               | jmp myfunc   | Jump to label "myfunc"                                       |
| 0x004               | halt         |                                                              |
| 0x006               | myfunc:      |                                                              |
| 0x008               | ldi 0x04 r4  | Store the number 4 into r4                                   |
| 0x00A               | ldi 0x01 r1  | Store the number 1 into r1                                   |

## Instruction Encoding

The following instruction encoding is envisioned for this architecture. In practice it is not used for programming or simulation.

| Instruction          | Nibble 1 (4 bits) | Nibble 2 (4 bits) | Nibble 3 (4 bits) | Nibble 4 (4 bits) |
| -------------------- | ----------------- | ----------------- | ----------------- | ----------------- |
| `jmp addr`           | 0000              |                   | address           |                   |
| `ld addr reg`        | 0001              |                   | address           | reg               |
| `ldi reg val`        | 0010              | value             | reg               |                   |
| `st reg addr`        | 0011              | reg               | address           |                   |
| `add reg1 reg2 reg3` | 0100              | reg1              | reg2              | reg3              |
| `and reg1 reg2 reg3` | 0101              | reg1              | reg2              | reg3              |
| `or reg1 reg2 reg3`  | 0110              | reg1              | reg2              | reg3              |
| `not reg1 reg2`      | 0111              | reg1              | reg2              |                   |
| `neg reg1 reg2`      | 1000              | reg1              | reg2              |                   |
| `shl reg1 n reg2`    | 1001              | reg1              | n                 | reg2              |
| `shr reg1 n reg2`    | 1010              | reg1              | n                 | reg2              |
| `eq reg1 reg2 reg3`  | 1011              | reg1              | reg2              | reg3              |
| `gt reg1 reg2 reg3`  | 1100              | reg1              | reg2              | reg3              |
| `if reg1`            | 1101              | reg1              |                   |                   |
| `skipif reg1`        | 1110              | reg1              |                   |                   |
| `halt`               | 1111              | 0000              |                   |                   |
| `ldr reg1 reg2`      | 1111              | 0001              | reg1              | reg2              |
| `str reg1 reg2`      | 1111              | 0010              | reg1              | reg2              |
| `jmpr reg1 reg2`     | 1111              | 0011              | reg1              | reg2              |
| `loadpc reg1 reg2`   | 1111              | 0100              | reg1              | reg2              |

```

```
