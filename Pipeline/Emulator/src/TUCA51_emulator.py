# Emulator for the TTU Computer Architecture #5.1 (TUCA-5.1)
# By Juan Carlos Rojas
# Modified by Andres Antillon and Claude 3.5 Sonnet
# Released 5/29/2023

# Modified: Class-based implementation to support multiple instances and testing
class TUCAEmulator:
    def __init__(self, verbose=False, minimal=False):
        # Added: minimal mode for cleaner output
        self.verbose = verbose
        self.minimal = minimal
        self.reset()

    def reset(self):
        """Reset all registers and memory to initial state"""
        self.reg = [0] * 16  # 16 registers, 8 bits each
        self.mem = [0] * 256  # 256 memory locations, 8 bits each
        self.prog_idx = 0    # Program counter (multiply by 2 for byte address)
        self.instructions = []  # List of instructions
        self.labels = {}     # Dictionary of label positions
        self.macros = {}     # Dictionary of macro definitions
        self.skip_next = False  # Skip next instruction flag

    # Modified: Only print registers in verbose non-minimal mode
    def print_registers(self):
        """Print current register values"""
        if self.verbose and not self.minimal:
            print("    ", end="")
            for val in self.reg:
                print(f"0x{val:02x} ", end="")
            print()

    def load_program(self, program_file):
        """Load program from file and parse instructions"""
        try:
            with open(program_file, 'r') as prog_file:
                # Parse the program and store into an instruction array
                self.instructions = []
                self.labels = {}
                self.macros = {}
                inst_idx = 0

                for inst_line in prog_file:
                    inst_str = inst_line.strip()
                    if not inst_str or inst_str.startswith('#'):
                        continue

                    # Handle macro definitions
                    line_tokens = inst_str.split()
                    if line_tokens[0] == "def":
                        self.macros[line_tokens[1]] = line_tokens[2]
                        continue

                    # Handle labels
                    if inst_str.endswith(':'):
                        self.labels[inst_str[:-1]] = inst_idx
                        continue

                    # Add instruction
                    self.instructions.append(inst_str)
                    inst_idx += 1

                # Modified: Only show instruction memory in verbose non-minimal mode
                if self.verbose and not self.minimal:
                    print("\nInstruction Memory:\n")
                    for i, inst in enumerate(self.instructions):
                        # Print label if it exists
                        for label, addr in self.labels.items():
                            if addr == i:
                                print(f"{label}:")
                        print(f"0x{i*2:03x}: {inst}")

                    if self.macros:
                        print("\nMacros:")
                        print(self.macros)

                return True

        except Exception as e:
            print(f"Error loading program: {e}")
            return False

    def load_memory(self, memory_file):
        """Load initial memory state from file"""
        try:
            with open(memory_file, 'r') as mem_file:
                # Reset memory
                self.mem = [0] * 256
                
                # Read the initial memory map values into the memory array
                for idx, line in enumerate(mem_file):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        value = int(line.replace('0x', ''), 16)
                        self.mem[idx] = value
                    except ValueError:
                        print(f"Warning: Invalid memory value on line {idx+1}: {line}")
                        continue
                return True

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
            # Handle skip-next condition
            if self.skip_next:
                if self.verbose and not self.minimal:
                    print("Skipped")
                self.skip_next = False
                self.prog_idx += 1
                return True

            # Handle each instruction type
            if inst[0] == "halt":
                return False

            elif inst[0] == "skipif":
                reg1_idx = int(inst[1][1:])
                self.skip_next = (self.reg[reg1_idx] != 0)
                self.prog_idx += 1

            elif inst[0] == "if":
                reg1_idx = int(inst[1][1:])
                self.skip_next = (self.reg[reg1_idx] == 0)
                self.prog_idx += 1

            elif inst[0] == "ld":
                addr_int = int(inst[1], 16)
                reg_idx = int(inst[2][1:])
                self.reg[reg_idx] = self.mem[addr_int]
                self.prog_idx += 1

            elif inst[0] == "ldr":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = self.mem[self.reg[reg1_idx]]
                self.prog_idx += 1

            elif inst[0] == "ldi":
                val = int(inst[1], 16)
                reg_idx = int(inst[2][1:])
                self.reg[reg_idx] = val
                self.prog_idx += 1

            elif inst[0] == "st":
                reg_idx = int(inst[1][1:])
                addr_int = int(inst[2], 16)
                self.mem[addr_int] = self.reg[reg_idx]
                self.prog_idx += 1

            elif inst[0] == "str":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.mem[self.reg[reg2_idx]] = self.reg[reg1_idx]
                self.prog_idx += 1

            elif inst[0] == "add":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] + self.reg[reg2_idx]) % 256
                self.prog_idx += 1

            elif inst[0] == "and":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] & self.reg[reg2_idx]) % 256
                self.prog_idx += 1

            elif inst[0] == "or":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = (self.reg[reg1_idx] | self.reg[reg2_idx]) % 256
                self.prog_idx += 1

            elif inst[0] == "not":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = (~self.reg[reg1_idx]) % 256
                self.prog_idx += 1

            elif inst[0] == "neg":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                self.reg[reg2_idx] = (-self.reg[reg1_idx]) % 256
                self.prog_idx += 1

            elif inst[0] == "shl":
                reg1_idx = int(inst[1][1:])
                shift_amount = int(inst[2])
                reg2_idx = int(inst[3][1:])
                self.reg[reg2_idx] = (self.reg[reg1_idx] << shift_amount) % 256
                self.prog_idx += 1

            elif inst[0] == "shr":
                reg1_idx = int(inst[1][1:])
                shift_amount = int(inst[2])
                reg2_idx = int(inst[3][1:])
                self.reg[reg2_idx] = self.reg[reg1_idx] >> shift_amount
                self.prog_idx += 1

            elif inst[0] == "eq":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = 1 if self.reg[reg1_idx] == self.reg[reg2_idx] else 0
                self.prog_idx += 1

            elif inst[0] == "gt":
                reg1_idx = int(inst[1][1:])
                reg2_idx = int(inst[2][1:])
                reg3_idx = int(inst[3][1:])
                self.reg[reg3_idx] = 1 if self.reg[reg1_idx] > self.reg[reg2_idx] else 0
                self.prog_idx += 1

            elif inst[0] == "loadpc":
                regh_idx = int(inst[1][1:])
                regl_idx = int(inst[2][1:])
                # Get the program counter
                pc = self.prog_idx * 2
                # Put the lower 8 bits in reg_lo
                self.reg[regl_idx] = (pc & 0xFF)
                # Put the upper 4 bits in reg_hi
                self.reg[regh_idx] = (pc >> 8)
                self.prog_idx += 1

            elif inst[0] == "jmp":
                key = inst[1]
                # Set the program index to the location of the label
                self.prog_idx = self.labels[key]

            elif inst[0] == "jmpr":
                regh_idx = int(inst[1][1:])
                regl_idx = int(inst[2][1:])
                target_addr = (self.reg[regh_idx] << 8) | self.reg[regl_idx]
                # The index is half of the instruction address
                self.prog_idx = target_addr >> 1

            else:
                print(f"Unknown instruction: {inst}")
                return False

            # Print register values if in verbose mode
            self.print_registers()
            return True

        except Exception as e:
            print(f"Error executing instruction '{inst_str}': {e}")
            return False

    # Modified: Added support for testing and verification
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
            while self.prog_idx < len(self.instructions):
                inst = self.instructions[self.prog_idx]
                
                if self.verbose and not self.minimal:
                    # Print label if it exists
                    for label, addr in self.labels.items():
                        if addr == self.prog_idx:
                            print(f"{label}:")
                    print(f"0x{self.prog_idx*2:03x}: {inst}")
                
                # Execute the instruction
                if not self.execute_instruction(inst):
                    break
                
                instruction_count += 1
            
            if self.verbose:
                if not self.minimal:
                    print(f"Program completed after {instruction_count} instructions")
                    print("\nRegister file:")
                    for idx, val in enumerate(self.reg):
                        print(f"{idx:02d}: 0x{val:02x}")
                print("\nFinal Memory State:")
                for idx, val in enumerate(self.mem):
                    if val != 0:  # Only show non-zero values
                        print(f"0x{idx:02x}: 0x{val:02x}")
            
            # Added: Convert memory array to dict for return value
            memory_dict = {
                idx: val for idx, val in enumerate(self.mem)
                if val != 0  # Only include non-zero values
            }
            
            # Added: Return final state for testing
            return EmulatorState(
                registers=self.reg.copy(),
                memory=memory_dict,
                instruction_count=instruction_count
            )
            
        except Exception as e:
            print(f"Error during execution: {e}")
            return None

# Added: Container for emulator final state to support testing
class EmulatorState:
    """Container for emulator final state"""
    def __init__(self, registers, memory, instruction_count):
        self.registers = registers
        self.memory = memory
        self.instruction_count = instruction_count
    
