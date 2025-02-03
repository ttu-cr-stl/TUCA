import re
from typing import List, Tuple, Dict, Optional
from .instruction import Instruction, Opcode

class Parser:
    def __init__(self):
        self.labels: Dict[str, int] = {}
        self.current_address: int = 0
        self.macros: Dict[str, str] = {}
        
        # Regular expressions for parsing
        self.label_regex = re.compile(r'^([a-zA-Z_][a-zA-Z0-9_]*):')
        self.instruction_regex = re.compile(r'^\s*([a-zA-Z]+)\s*(.*?)(?:\s*#.*)?$')
        self.comment_regex = re.compile(r'#.*$')
        self.def_regex = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+(.+)$')
    
    def clean_line(self, line: str) -> str:
        """Remove comments and whitespace from a line."""
        line = self.comment_regex.sub('', line)
        return line.strip()
    
    def parse_operands(self, operands_str: str) -> List[str]:
        """Parse operands string into a list of operands."""
        if not operands_str:
            return []
        # Replace any macros in the operands
        for macro, value in self.macros.items():
            operands_str = operands_str.replace(macro, value)
        # Split by comma and clean each operand
        operands = [op.strip() for op in operands_str.split(',')]
        # Further split any operands that might have spaces (for instructions without commas)
        if len(operands) == 1 and ' ' in operands[0]:
            operands = [op.strip() for op in operands[0].split()]
        return operands
    
    def first_pass(self, lines: List[str]) -> None:
        """First pass: collect all labels and macros and their values."""
        self.current_address = 0
        self.labels.clear()
        self.macros.clear()
        
        for line in lines:
            line = self.clean_line(line)
            if not line:
                continue
                
            # Check for macro definition
            def_match = self.def_regex.match(line)
            if def_match:
                macro_name = def_match.group(1)
                macro_value = def_match.group(2).strip()
                self.macros[macro_name] = macro_value
                continue
                
            # Check for label
            label_match = self.label_regex.match(line)
            if label_match:
                label = label_match.group(1)
                self.labels[label] = self.current_address
                # Remove label from line for instruction processing
                line = line[label_match.end():].strip()
                
            # If there's still content after removing label, it's an instruction
            if line and not line.startswith('#') and not line.startswith('def'):
                self.current_address += 1
    
    def parse_instruction(self, line: str, line_num: int) -> Optional[Instruction]:
        """Parse a single instruction line."""
        line = self.clean_line(line)
        if not line:
            return None
            
        # Skip macro definitions
        if line.startswith('def'):
            return None
            
        # Remove label if present
        label_match = self.label_regex.match(line)
        if label_match:
            line = line[label_match.end():].strip()
            if not line:
                return None
        
        # Parse instruction
        instr_match = self.instruction_regex.match(line)
        if not instr_match:
            raise SyntaxError(f"Invalid instruction format at line {line_num}: {line}")
            
        opcode, operands_str = instr_match.groups()
        operands = self.parse_operands(operands_str)
        
        try:
            # Handle label references in jump instructions
            if opcode.upper() == 'JMP' and operands[0] in self.labels:
                operands[0] = str(self.labels[operands[0]])
            
            # Handle label references in branch/jump instructions
            if opcode.upper() in ['BEQ', 'JAL']:
                if len(operands) == 3 and operands[2] in self.labels:
                    # Calculate relative offset
                    target_addr = self.labels[operands[2]]
                    current_addr = self.current_address
                    offset = target_addr - current_addr
                    operands[2] = str(offset)
            
            return Instruction.from_parts(opcode, operands)
            
        except KeyError as e:
            raise SyntaxError(f"Error parsing instruction at line {line_num}: {str(e)}")
    
    def parse_program(self, program: str) -> List[Instruction]:
        """Parse a complete assembly program."""
        lines = program.split('\n')
        
        # First pass: collect labels and macros
        self.first_pass(lines)
        
        # Second pass: parse instructions
        instructions = []
        self.current_address = 0
        
        for line_num, line in enumerate(lines, 1):
            try:
                instruction = self.parse_instruction(line, line_num)
                if instruction:
                    instructions.append(instruction)
                    self.current_address += 1
            except SyntaxError as e:
                raise SyntaxError(f"Line {line_num}: {str(e)}")
            except ValueError as e:
                raise ValueError(str(e))
        
        return instructions
