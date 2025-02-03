#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
from TUCA51_emulator import TUCAEmulator

def load_config(config_file: Path) -> dict:
    """Load test configuration from JSON file"""
    try:
        with open(config_file) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

def read_memory_file(memory_file: Path) -> dict:
    """Read memory values from a file"""
    memory = {}
    try:
        with open(memory_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                addr, value = line.split('=')
                # Remove 0x prefix if present
                addr = int(addr.replace('0x', ''), 16)
                value = int(value.replace('0x', ''), 16)
                memory[addr] = value
        return memory
    except Exception as e:
        print(f"Error reading memory file {memory_file}: {e}")
        return None

def verify_results(actual_file: Path, expected: dict) -> bool:
    """Verify emulator results match expected values"""
    actual = read_memory_file(actual_file)
    if actual is None:
        return False
        
    # Convert expected memory addresses and values to integers for comparison
    expected_memory = {
        int(addr.replace('0x', ''), 16): int(value.replace('0x', ''), 16)
        for addr, value in expected['memory'].items()
    }
    
    # Check each expected memory value
    for addr, expected_value in expected_memory.items():
        actual_value = actual.get(addr)
        if actual_value != expected_value:
            print(f"Mismatch at address 0x{addr:02x}:")
            print(f"  Expected: 0x{expected_value:02x}")
            print(f"  Actual:   0x{actual_value:02x if actual_value is not None else 0:02x}")
            return False
            
    return True

def write_results(memory: dict, output_file: Path):
    """Write memory state to file in same format as Verilog results"""
    # Ensure emulator results directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        # Write with 0x prefix for both address and value
        for addr, value in sorted(memory.items()):
            f.write(f"0x{addr:02x}=0x{value:02x}\n")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python3 run.py <program.txt> <memory.txt> [output_file]")
        print("Examples:")
        print("  python3 run.py Programs/example1/prog.txt Programs/example1/test_mems/mem1.txt")
        print("  python3 run.py Programs/example1/prog.txt Programs/example1/test_mems/mem1.txt Programs/example1/results/emulator/mem1.txt")
        sys.exit(1)
    
    # Get root directory (where the Programs directory is)
    root_dir = Path(__file__).parent.parent.parent.parent
    
    # Convert paths to be relative to root directory
    program_file = Path(sys.argv[1])
    memory_file = Path(sys.argv[2])
    
    # Optional output file
    output_file = None
    if len(sys.argv) == 4:
        output_file = Path(sys.argv[3])
    
    # Run the program through emulator
    # Use minimal mode when writing to output file (likely running as part of test)
    minimal_mode = output_file is not None
    emulator = TUCAEmulator(verbose=not minimal_mode, minimal=minimal_mode)
    
    try:
        if not minimal_mode:
            print(f"\nRunning emulator with memory file: {memory_file}")
            if output_file:
                print(f"Results will be saved to: {output_file}")
            print("----------------------------------------")
            
        final_state = emulator.run_program(
            program_file=program_file,
            memory_file=memory_file
        )
        
        if final_state is None:
            sys.exit(1)
        
        # Save results if output file specified
        if output_file:
            write_results(final_state.memory, output_file)
            if not minimal_mode:
                print(f"\nResults written to: {output_file}")
            
            # If this is a test case, verify against expected output
            config_file = root_dir / Path(sys.argv[1]).parent / 'config.json'
            if config_file.exists():
                config = load_config(config_file)
                if config:
                    # Find the test case for this memory file
                    memory_name = Path(sys.argv[2]).name
                    test_case = next(
                        (test for test in config['test_cases'] 
                         if test['memory'].endswith(memory_name)),
                        None
                    )
                    if test_case:
                        if not minimal_mode:
                            print("\nVerifying results...")
                        if verify_results(output_file, test_case['expected']):
                            print("✅ Results match expected values")
                        else:
                            print("❌ Results do not match expected values")
                            sys.exit(1)
            
    except Exception as e:
        print(f"Error running program: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 