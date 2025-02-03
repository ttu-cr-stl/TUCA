#!/usr/bin/env python3
import json
import sys
import shutil
from pathlib import Path
from typing import Dict, Any, Union, List

# Add the root directory to Python path so we can import the assembler module
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from Pipeline.Assembler.src.assembler import Assembler

PROGRAMS_DIR = Path("Programs")

def clean(target: Union[str, Path, List[str]] = None) -> bool:
    """
    Clean build artifacts.
    Args:
        target: Optional target to clean. Can be:
               - None: clean all build directories
               - str/Path: clean specific directory
               - List[str]: clean multiple specific directories
    Returns:
        bool: True if cleaning succeeded
    """
    if target is None:
        # Clean all build directories in Programs
        targets = [d for d in PROGRAMS_DIR.iterdir() if d.is_dir()]
    elif isinstance(target, (str, Path)):
        targets = [Path(target)]
    else:
        targets = [Path(t) for t in target]
    
    success = True
    for target_dir in targets:
        build_dir = target_dir / "build"
        if build_dir.exists():
            try:
                shutil.rmtree(build_dir)
                print(f"Cleaned {build_dir}")
            except Exception as e:
                print(f"Error cleaning {build_dir}: {e}")
                success = False
    
    return success

def compile_program(prog_path: Path, output_dir: Path) -> bool:
    """
    Compile a TUCA assembly program to a .mem file.
    Args:
        prog_path: Path to the assembly program
        output_dir: Output directory for the .mem file
    Returns:
        bool: True if compilation succeeded
    """
    if not prog_path.exists():
        print(f"Error: Program file {prog_path} not found")
        return False
        
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate output filename
    out_file = output_dir / f"{prog_path.stem}.mem"
    
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

def build_program(program_dir: str) -> bool:
    """
    Build a TUCA program.
    Args:
        program_dir: Name of the program directory
    Returns:
        bool: True if compilation succeeded
    """
    prog_dir = PROGRAMS_DIR / program_dir
    if not prog_dir.exists():
        print(f"No program directory found at {prog_dir}")
        return False
        
    config_path = prog_dir / "config.json"
    if not config_path.exists():
        print(f"No config file found in {prog_dir}")
        return False
        
    with open(config_path) as f:
        config = json.load(f)
    
    # Compile the program
    prog_path = prog_dir / config["program"]
    output_dir = prog_dir / "build"  # Build directory inside program directory
    
    return compile_program(prog_path, output_dir)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 build.py <command> [target]")
        print("Commands:")
        print("  build <program>    Build a TUCA program")
        print("    Example: python3 build.py build example1")
        print("  clean [target]     Clean build artifacts")
        print("    Example: python3 build.py clean         # Clean all")
        print("            python3 build.py clean example1 # Clean specific program")
        print("            python3 build.py clean p1 p2    # Clean multiple programs")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "clean":
        if len(sys.argv) == 2:
            # Clean all
            success = clean()
        else:
            # Clean specific targets
            targets = sys.argv[2:]
            success = clean([PROGRAMS_DIR / t for t in targets])
    elif command == "build":
        if len(sys.argv) != 3:
            print("Error: build command requires a program name")
            sys.exit(1)
        program_dir = sys.argv[2]
        success = build_program(program_dir)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 