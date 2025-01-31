TUCA-5.1 emulator
By Juan Carlos Rojas
5/29/2023

Description:

This is an emulator of the TUCA-5.1 computer architecture.
The assembly code should be written in a text file, one instruction per line.
The initial memory map should be written in another text file, one value per line, using 8-bit hex values.
If you provide less than 256 values, the rest of the memory positions will be filled with zeros

Usage:
- Run TUCA51_emulator.py
- When prompted, type the name of your program text file
- When prompted, type the name of your initial memory map text file
- The program will run until it reaches the end, or a halt instruction
- The final values of all the registers and memory locations will be displayed

Verbose mode:

You can set the variable verbose_mode = True in the emulator to run in verbose mode.  
In this mode, the value of all the registers will be printed after every instruction.

Example:
In the example below, the loadpc instruction is used to store the program counter.  
This is used as a base to compute a return address (PC+4), and used to jump back.
Note that instruction addresses are 12 bits, and need to be handled using two registers.

>> TUCA51_emulator.py
Enter name of program file: tuca51_ex4_prog.txt
Enter name of initial memory file: tuca51_ex4_mem.txt

Instruction Memory:

0x000: loadpc r5 r6
0x002: jmp myfunc
function_return:
0x004: halt
myfunc:
0x006: ldi 0x04 r4
0x008: ldi 0x01 r1
0x00a: add r6 r4 r7
0x00c: gt r6 r7 r8
0x00e: if r8
0x010: add r5 r1 r5
0x012: jmpr r5 r7

Starting Execution

0x000: loadpc r5 r6
    0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x002: jmp myfunc
    0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
myfunc:
0x006: ldi 0x04 r4
    0x00 0x00 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x008: ldi 0x01 r1
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x00a: add r6 r4 r7
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x00c: gt r6 r7 r8
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x00e: if r8
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x010: add r5 r1 r5
Skipped
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
0x012: jmpr r5 r7
    0x00 0x01 0x00 0x00 0x04 0x00 0x00 0x04 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 
function_return:
0x004: halt
Program completed after 10 instructions

Register file:

00: 0x00
01: 0x01
02: 0x00
03: 0x00
04: 0x04
05: 0x00
06: 0x00
07: 0x04
08: 0x00
09: 0x00
10: 0x00
11: 0x00
12: 0x00
13: 0x00
14: 0x00
15: 0x00

