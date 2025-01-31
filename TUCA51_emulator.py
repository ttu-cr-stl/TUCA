# Emulator for the TTU Computer Architecture #5.1 (TUCA-5.1)
# By Juan Carlos Rojas
# Released 5/29/2023

# Set verbose_mode = True to see register values after every instruction
#verbose_mode = False
verbose_mode = True

# Ask the user for the names of the program files and make sure files exist
tryagain = True;
while tryagain:
    program_filename = input("Enter name of program file: ")
    memory_filename = input("Enter name of initial memory file: ")
    try:
        prog_file = open(program_filename, "r")
        mem_file = open(memory_filename, "r")
        tryagain = False;
    except FileNotFoundError:
        print("Invalid filename")

# Initialize the register file and data memory buffer to zeros
reg = [0] * 16;
mem = [0] * 256;

# Read the initial memory map values into the memory array
for idx, val in enumerate(mem_file):
    # Convert the value to integer
    mem[idx] = int(val, 16)
mem_file.close()

# Parse the program and store into an instruction array (represents instruction memory)
# In the process, capture any labels and store them in a dictionary.
inst_mem = []
inst_idx = 0
labels = dict()
macros = dict()

for inst_line in prog_file:
    
    # Remove newline character
    inst_str = inst_line.strip()

    # Ignore empty lines
    if len(inst_str) == 0:
        continue
    
    # Ignore comment lines
    if inst_str[0] == "#":
        continue

    # See if line defines a macro
    line_tokens = inst_str.split()
    if line_tokens[0]=="def":
        line_tokens = inst_str.split()
        macros[line_tokens[1]] = line_tokens[2]
        continue

    # See if line defines a label
    if inst_str[-1] == ":":
        # Add label to dictionary, with value set to current instruction index
        labels[inst_str[:-1]] = inst_idx
        continue

    # Add instruction to instruction memory
    inst_mem.append(inst_str)
    inst_idx += 1

# Finished parsing the program text
prog_file.close()

# Print instruction memory and labels
print("\nInstruction Memory:\n")

label_values = labels.values()
label_keys = labels.keys()

for inst_idx, inst_str in enumerate(inst_mem):
    
    # If there is a label with this instruction index, print it
    if (inst_idx in label_values):
        label_idx = list(label_values).index(inst_idx)
        print("{}:".format(list(label_keys)[label_idx]))
    
    # Print the instruction
    print("{:#05x}: {}".format(inst_idx*2, inst_str))

# Print variables
print("\nMacros:")
print(macros)

# Program execution
print("\nStarting Execution\n")

# Initializations
prog_idx = 0
skip_next = False
instruction_count = 0

# Execute the program
while True:
    # Read instruction at the program index
    inst_str = inst_mem[prog_idx]

    # Advance program counter
    prog_idx += 1
    
    # Count instructions executed
    instruction_count += 1

    # Print instruction if in verbose mode
    if verbose_mode:
        # If there is a label with this instruction index, print it
        if ((prog_idx-1) in label_values):
            label_idx = list(label_values).index((prog_idx-1))
            print("{}:".format(list(label_keys)[label_idx]))
        # Print instruction
        print("{:#05x}: {}".format((prog_idx-1)*2, inst_str))

    # Replace macros with their respective values
    for tag in macros:
        if tag in inst_str:
            inst_str = inst_str.replace(tag, macros[tag])
            if verbose_mode:
                print("  Replaced with: {}".format(inst_str))
        
    # Parse the instruction into words (separated by spaces)
    inst = inst_str.split()

    # Handle skip-next condition
    if skip_next:
        if verbose_mode:
            print("Skipped")
        skip_next = False

    # Handle: skipif
    elif inst[0]=="skipif":
        reg1_idx = int(inst[1][1:])
        skip_next = (reg[reg1_idx] != 0)

    # Handle: if
    elif inst[0]=="if":
        reg1_idx = int(inst[1][1:])
        skip_next = (reg[reg1_idx] == 0)
        
    # Handle: ld reg addr
    elif inst[0]=="ld":
        addr_int = int(inst[1], 16)
        reg_idx = int(inst[2][1:])
        reg[reg_idx] = mem[addr_int]

    # Handle: ldr reg1 reg2
    elif inst[0]=="ldr":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg[reg2_idx] = mem[reg[reg1_idx]]

    # Handle: ldi reg val
    elif inst[0]=="ldi":
        val = int(inst[1], 16)
        reg_idx = int(inst[2][1:])
        reg[reg_idx] = val

    # Handle: st reg addr
    elif inst[0]=="st":
        addr_int = int(inst[2], 16)
        reg_idx = int(inst[1][1:])
        mem[addr_int] = reg[reg_idx]

    # Handle: str reg1 reg2
    elif inst[0]=="str":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        mem[reg[reg2_idx]] = reg[reg1_idx]

    # Handle: add reg1 reg2 reg3
    elif inst[0]=="add":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg3_idx = int(inst[3][1:])
        reg[reg3_idx] = (reg[reg1_idx] + reg[reg2_idx]) % 256

    # Handle: and reg1 reg2 reg3
    elif inst[0]=="and":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg3_idx = int(inst[3][1:])
        reg[reg3_idx] = (reg[reg1_idx] & reg[reg2_idx]) % 256

    # Handle: or reg1 reg2 reg3
    elif inst[0]=="or":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg3_idx = int(inst[3][1:])
        reg[reg3_idx] = (reg[reg1_idx] | reg[reg2_idx]) % 256

    # Handle: not reg1 reg2
    elif inst[0]=="not":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg[reg2_idx] = (~reg[reg1_idx]) % 256

    # Handle: neg reg1 reg2
    elif inst[0]=="neg":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg[reg2_idx] = (-reg[reg1_idx]) % 256

    # Handle: shl reg1 reg2
    elif inst[0]=="shl":
        reg1_idx = int(inst[1][1:])
        shift_amount = int(inst[2])
        reg2_idx = int(inst[3][1:])
        reg[reg2_idx] = (reg[reg1_idx] << shift_amount) % 256

    # Handle: shr reg1 reg2
    elif inst[0]=="shr":
        reg1_idx = int(inst[1][1:])
        shift_amount = int(inst[2])
        reg2_idx = int(inst[3][1:])
        reg[reg2_idx] = reg[reg1_idx] >> shift_amount

    # Handle: eq reg1 reg2 reg3
    elif inst[0]=="eq":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg3_idx = int(inst[3][1:])
        reg[reg3_idx] = 1 if reg[reg1_idx] == reg[reg2_idx] else 0

    # Handle: gt reg1 reg2 reg3
    elif inst[0]=="gt":
        reg1_idx = int(inst[1][1:])
        reg2_idx = int(inst[2][1:])
        reg3_idx = int(inst[3][1:])
        reg[reg3_idx] = 1 if reg[reg1_idx] > reg[reg2_idx] else 0

    # Handle: loadpc reg_hi reg_lo 
    elif inst[0]=="loadpc":
        regh_idx = int(inst[1][1:])
        regl_idx = int(inst[2][1:])
        # Get the program counter
        pc = (prog_idx-1)*2
        # Put the lower 8 bits in reg_lo
        reg[regl_idx] = (pc & 0xFF)
        # Put thee upper 4 bits in reg_hi
        reg[regh_idx] = (pc >> 8)

    # Handle: jmp addr  (addr is expected to be a label)
    elif inst[0]=="jmp":
        key = inst[1]
        # Set the program index to the location of the label
        prog_idx = labels[key]

    # Handle: jmpr reg_hi reg_lo
    elif inst[0]=="jmpr":
        regh_idx = int(inst[1][1:])
        regl_idx = int(inst[2][1:])
        target_addr = (reg[regh_idx] << 8) | reg[regl_idx]
        # The index is half of the instruction address
        prog_idx = target_addr >> 1

    # Handle: halt
    elif inst[0]=="halt":
        break
        
    else:
        print("Unknown instruction:", inst)

    # Print register values if in verbose mode
    if verbose_mode:
        print("    ", end="")
        for idx, val in enumerate(reg):
            print("0x{:02x} ".format(val), end="")
        print()

# Program complete
print("Program completed after {} instructions".format(instruction_count))

# Print the register file
print("\nRegister file:\n")
for idx, val in enumerate(reg):
    print("{:02d}: 0x{:02x}".format(idx,val))

# Print the memory map
print("\nMemory map:")
for idx, val in enumerate(mem):
    if idx % 8 == 0:
        print("\n0x{:02x}: ".format(idx), end="")
    print("0x{:02x} ".format(val), end="")
    
