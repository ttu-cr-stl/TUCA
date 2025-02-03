#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the root directory to Python path so we can import the assembler module
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from assembler.src.assembler import Assembler

def compile_program(prog_path: str, output_dir: str = None):
    """
    Compile a TUCA assembly program to a .mem file.
    Args:
        prog_path: Path to the assembly program
        output_dir: Optional output directory for the .mem file. If not specified,
                   creates a build/ directory next to the program file.
    """
    prog_path = Path(prog_path)
    if not prog_path.exists():
        print(f"Error: Program file {prog_path} not found")
        return False
        
    # Create output directory if it doesn't exist
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = prog_path.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output filename
    out_file = out_dir / f"{prog_path.stem}.mem"
    
    # Read the program
    with open(prog_path) as f:
        program = f.read()
    
    # Compile the program
    try:
        assembler = Assembler()
        instructions = assembler.assemble_program(program)
        
        # Write the memory file
        with open(out_file, 'w') as f:
            assembler.write_verilog_mem(instructions, f)
            
        print(f"Successfully compiled {prog_path} to {out_file}")
        return True
    except Exception as e:
        print(f"Error compiling {prog_path}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 compile.py <program.txt> [output_dir]")
        print("Example: python3 compile.py Programs/example1/prog.txt")
        print("         python3 compile.py Examples/example1.txt Examples/build")
        sys.exit(1)
    
    prog_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = compile_program(prog_path, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 