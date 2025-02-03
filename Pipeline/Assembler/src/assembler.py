from typing import List, Union, TextIO
from pathlib import Path
import argparse
import sys

from .parser import Parser
from .instruction import Instruction

class Assembler:
    def __init__(self):
        self.parser = Parser()
    
    def assemble_program(self, program: str) -> List[Instruction]:
        """Assemble a program string into a list of instructions."""
        return self.parser.parse_program(program)
    
    def generate_hex(self, instructions: List[Instruction]) -> List[str]:
        """Generate hex representation of instructions."""
        return [instr.to_hex() for instr in instructions]
    
    def generate_binary(self, instructions: List[Instruction]) -> List[str]:
        """Generate binary representation of instructions."""
        return [instr.to_binary() for instr in instructions]
    
    def write_hex_file(self, instructions: List[Instruction], output_file: Union[str, Path, TextIO]) -> None:
        """Write instructions to a hex file."""
        hex_lines = self.generate_hex(instructions)
        
        if isinstance(output_file, (str, Path)):
            with open(output_file, 'w') as f:
                f.write('\n'.join(hex_lines) + '\n')
        else:
            output_file.write('\n'.join(hex_lines) + '\n')
    
    def write_binary_file(self, instructions: List[Instruction], output_file: Union[str, Path, TextIO]) -> None:
        """Write instructions to a binary file."""
        binary_lines = self.generate_binary(instructions)
        
        if isinstance(output_file, (str, Path)):
            with open(output_file, 'w') as f:
                f.write('\n'.join(binary_lines) + '\n')
        else:
            output_file.write('\n'.join(binary_lines) + '\n')
    
    def write_verilog_mem(self, instructions: List[Instruction], output_file: Union[str, Path, TextIO]) -> None:
        """Write instructions to a Verilog memory initialization file."""
        hex_lines = self.generate_hex(instructions)
        
        if isinstance(output_file, (str, Path)):
            with open(output_file, 'w') as f:
                f.write("// Memory initialization file for TUCA program\n")
                f.write("// Format: @address data\n")
                for addr, hex_instr in enumerate(hex_lines):
                    f.write(f"@{addr:04x} {hex_instr}\n")
        else:
            output_file.write("// Memory initialization file for TUCA program\n")
            output_file.write("// Format: @address data\n")
            for addr, hex_instr in enumerate(hex_lines):
                output_file.write(f"@{addr:04x} {hex_instr}\n")

def main():
    parser = argparse.ArgumentParser(description='TUCA Assembler')
    parser.add_argument('input_file', type=str, help='Input assembly file')
    parser.add_argument('output_file', type=str, help='Output file')
    parser.add_argument('--format', choices=['hex', 'bin', 'vmem'], default='hex',
                      help='Output format (hex, bin, or vmem for Verilog)')
    
    args = parser.parse_args()
    
    try:
        # Read input file
        with open(args.input_file, 'r') as f:
            program = f.read()
        
        # Assemble program
        assembler = Assembler()
        instructions = assembler.assemble_program(program)
        
        # Write output in specified format
        if args.format == 'hex':
            assembler.write_hex_file(instructions, args.output_file)
        elif args.format == 'bin':
            assembler.write_binary_file(instructions, args.output_file)
        else:  # vmem
            assembler.write_verilog_mem(instructions, args.output_file)
            
    except FileNotFoundError:
        print(f"Error: Could not open input file '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Assembly error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
