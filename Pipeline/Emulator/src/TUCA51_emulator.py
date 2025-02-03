# Emulator for the TTU Computer Architecture #5.1 (TUCA-5.1)
# By Juan Carlos Rojas
# Modified by Andres Antillon
# Released 5/29/2023

class TUCAEmulator:
    def __init__(self, verbose=False, minimal=False):
        self.verbose = verbose
        self.minimal = minimal
        self.reset()

    def reset(self):
        """Reset all registers and memory to initial state"""
        self.reg = [0] * 16  # 16 registers, 8 bits each
        self.memory = {}     # 256 memory locations, 8 bits each
        self.pc = 0         # Program counter
        self.instructions = []  # List of instructions
        self.labels = {}     # Dictionary of label positions
        self.macros = {}     # Dictionary of macro definitions

    def print_registers(self, show_all=False):
        """Print current register values"""
        if show_all:
            for idx, val in enumerate(self.reg):
                print(f"{idx:02d}: 0x{val:02x}")
        else:
            print("    ", end="")
            for val in self.reg:
                print(f"0x{val:02x} ", end="")
            print()

    def load_program(self, program_file):
        """Load program from file and parse instructions"""
        try:
            with open(program_file, 'r') as prog_file:
                # Parse the program and store into an instruction array (represents instruction memory)
                # In the process, capture any labels and store them in a dictionary.
                self.instructions = []
                self.labels = {}
                self.macros = {}
                pc = 0

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
                        self.macros[line_tokens[1]] = line_tokens[2]
                        continue

                    # See if line defines a label
                    if inst_str[-1] == ":":
                        # Add label to dictionary, with value set to current instruction index
                        self.labels[inst_str[:-1]] = pc
                        continue

                    # Add instruction to instruction memory
                    self.instructions.append(inst_str)
                    pc += 2  # Each instruction is 2 bytes

                if self.verbose and not self.minimal:
                    print("\nInstruction Memory:\n")
                    for i, inst in enumerate(self.instructions):
                        # Print label if it exists
                        for label, addr in self.labels.items():
                            if addr == i*2:
                                print(f"{label}:")
                        print(f"0x{i*2:03x}: {inst}")

                    if self.macros:
                        print("\nMacros:")
                        print(self.macros)

                return True

        except FileNotFoundError:
            print(f"Error: Program file '{program_file}' not found")
            return False
        except Exception as e:
            print(f"Error loading program: {e}")
            return False

    def load_memory(self, memory_file):
        """Load initial memory state from file"""
        try:
            with open(memory_file, 'r') as mem_file:
                # Reset memory
                self.memory = {}

                # Read the initial memory map values into the memory array
                for idx, val in enumerate(mem_file):
                    val = val.strip()
                    if not val or val.startswith('#'):
                        continue
                    try:
                        # Support both 0x notation and plain hex
                        value = val.replace('0x', '')
                        self.memory[idx] = int(value, 16)
                    except ValueError:
                        print(f"Warning: Invalid memory value on line {idx+1}: {val}")
                        continue

                return True

        except FileNotFoundError:
            print(f"Error: Memory file '{memory_file}' not found")
            return False
        except Exception as e:
            print(f"Error loading memory: {e}")
            return False

    def execute_instruction(self, inst_str):
        """Execute a single instruction"""
        # Replace macros
        for tag, value in self.macros.items():
            if tag in inst_str:
                inst_str = inst_str.replace(tag, value)
                if self.verbose and not self.minimal:
                    print(f"  Replaced with: {inst_str}")

        # Parse instruction
        inst = inst_str.split()
        if not inst:
            return True

        try:
            # Handle each instruction type
            if inst[0] == "halt":
                return False

            elif inst[0] == "skipif":
                reg1_idx = int(inst[1][1:])
                self.pc += 4 if self.reg[reg1_idx] != 0 else 2

            elif inst[0] == "if":
                reg1_idx = int(inst[1][1:])
                self.pc += 4 if self.reg[reg1_idx] == 0 else 2

            elif inst[0] == "ld":
                addr_int = int(inst[1], 16)
                reg_idx = int(inst[2][1:])
                self.reg[reg_idx] = self.memory.get(addr_int, 0)
                self.pc += 2

            elif inst[0] == "ldr":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = self.memory.get(self.reg[reg1_idx], 0)
                self.pc += 2

            elif inst[0] == "ldi":
                val = int(inst[1], 16)
                reg_idx = int(inst[2][1:])
                self.reg[reg_idx] = val
                self.pc += 2

            elif inst[0] == "st":
                reg_idx = int(inst[1][1:])
                addr_int = int(inst[2], 16)
                self.memory[addr_int] = self.reg[reg_idx]
                self.pc += 2

            elif inst[0] == "str":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.memory[self.reg[reg2_idx]] = self.reg[reg1_idx]
                self.pc += 2

            elif inst[0] == "add":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] + self.reg[reg2_idx]) % 256
                self.pc += 2

            elif inst[0] == "and":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] & self.reg[reg2_idx]) % 256
                self.pc += 2

            elif inst[0] == "or":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] | self.reg[reg2_idx]) % 256
                self.pc += 2

            elif inst[0] == "not":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = (~self.reg[reg1_idx]) % 256
                self.pc += 2

            elif inst[0] == "neg":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = (-self.reg[reg1_idx]) % 256
                self.pc += 2

            elif inst[0] == "shl":
                reg1_idx = int(inst[1][1:])
                shift_amount = int(inst[2])
                reg2_idx = int(inst[3][1:])
                self.reg[reg2_idx] = (self.reg[reg1_idx] << shift_amount) % 256
                self.pc += 2

            elif inst[0] == "shr":
                reg1_idx = int(inst[1][1:])
                shift_amount = int(inst[2])
                reg2_idx = int(inst[3][1:])
                self.reg[reg2_idx] = self.reg[reg1_idx] >> shift_amount
                self.pc += 2

            elif inst[0] == "eq":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = 1 if self.reg[reg1_idx] == self.reg[reg2_idx] else 0
                self.pc += 2

            elif inst[0] == "gt":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = 1 if self.reg[reg1_idx] > self.reg[reg2_idx] else 0
                self.pc += 2

            elif inst[0] == "loadpc":
                regh_idx = int(inst[1][1:])
                regl_idx = int(inst[2][1:])
                # Get the program counter
                pc = self.pc
                # Put the lower 8 bits in reg_lo
                self.reg[regl_idx] = (pc & 0xFF)
                # Put the upper 4 bits in reg_hi
                self.reg[regh_idx] = (pc >> 8)
                self.pc += 2

            elif inst[0] == "jmp":
                key = inst[1]
                # Set the program counter to the label location
                self.pc = self.labels[key]

            elif inst[0] == "jmpr":
                regh_idx = int(inst[1][1:])
                regl_idx = int(inst[2][1:])
                target_addr = (self.reg[regh_idx] << 8) | self.reg[regl_idx]
                self.pc = target_addr

            elif inst[0] == "sub":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] - self.reg[reg2_idx]) % 256
                self.pc += 2

            else:
                print(f"Unknown instruction: {inst}")
                return False

            return True

        except Exception as e:
            print(f"Error executing instruction '{inst_str}': {e}")
            return False

    def run_program(self, program_file, memory_file=None):
        """Run a program with optional initial memory state"""
        # Reset state
        self.reset()

        # Load program
        if not self.load_program(program_file):
            return None

        # Load memory if provided
        if memory_file and not self.load_memory(memory_file):
            return None

        if self.verbose and not self.minimal:
            print("\nStarting Execution\n")

        # Execute instructions
        instruction_count = 0
        
        try:
            while self.pc < len(self.instructions) * 2:
                inst = self.instructions[self.pc // 2]
                
                if self.verbose and not self.minimal:
                    # Print label if it exists
                    for label, addr in self.labels.items():
                        if addr == self.pc:
                            print(f"{label}:")
                    print(f"0x{self.pc:03x}: {inst}")
                
                # Execute the instruction
                if not self.execute_instruction(inst):
                    break
                
                instruction_count += 1
                
                if self.verbose and not self.minimal:
                    self.print_registers()
            
            if self.verbose:
                if not self.minimal:
                    print(f"Program completed after {instruction_count} instructions")
                    print("\nRegister file:")
                    self.print_registers(show_all=True)
                print("\nFinal Memory State:")
                for addr, val in sorted(self.memory.items()):
                    print(f"0x{addr:02x}: 0x{val:02x}")
            
            # Return final state
            return EmulatorState(
                registers=self.reg.copy(),
                memory=self.memory.copy(),
                instruction_count=instruction_count
            )
            
        except Exception as e:
            print(f"Error during execution: {e}")
            return None

class EmulatorState:
    """Container for emulator final state"""
    def __init__(self, registers, memory, instruction_count):
        self.registers = registers
        self.memory = memory
        self.instruction_count = instruction_count
    
