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
    """Read memory values from a file. Supports two formats:
    1. addr=value format: '0x00=0x99'
    2. Sequential values: '0x99' (address starts at 0 and increments)
    """
    memory = {}
    try:
        with open(memory_file) as f:
            addr = 0  # Start address for sequential format
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                if '=' in line:
                    # Format 1: addr=value
                    addr_str, value_str = line.split('=')
                    addr = int(addr_str.replace('0x', ''), 16)
                    value = int(value_str.replace('0x', ''), 16)
                else:
                    # Format 2: sequential values
                    value = int(line.replace('0x', ''), 16)
                    
                memory[addr] = value
                addr += 1  # Increment address for next value
                
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
    
    # Only check addresses that are explicitly specified in expected values
    for addr, expected_value in expected_memory.items():
        actual_value = actual.get(addr, 0)
        if actual_value != expected_value:
            print(f"Mismatch at address 0x{addr:02x}:")
            print(f"  Expected: 0x{expected_value:02x}")
            print(f"  Actual:   0x{actual_value:02x}")
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

def print_memory_map(memory: dict, expected_memory: dict = None, instruction_count: int = None):
    """Print the final memory map in a readable format"""
    if instruction_count is not None:
        print(f"\nProgram completed in {instruction_count} cycles")
        
    print("\nFinal Memory Map:")
    print("----------------")
    if expected_memory:
        print("Address: Actual -> Expected")
        # Show all memory locations between min and max used addresses
        min_addr = min(memory.keys())
        max_addr = max(memory.keys())
        for addr in range(min_addr, max_addr + 1):
            actual = memory.get(addr, 0)  # Get value or 0 if not written
            # Only show expected if it's specified in config
            if addr in expected_memory:
                expected = expected_memory[addr]
                match = "✅" if actual == expected else "❌"
                print(f"0x{addr:02x}: 0x{actual:02x} -> 0x{expected:02x} {match}")
            else:
                # Don't care about this address
                print(f"0x{addr:02x}: 0x{actual:02x} -> don't care")
    else:
        # Original format when no expected values
        for addr, value in sorted(memory.items()):
            print(f"0x{addr:02x}: 0x{value:02x}")
    print("----------------")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py <program.txt> [memory.txt] [output_file] [--verbose]")
        print("Examples:")
        print("  python3 run.py Programs/example1/prog.txt                                # Run all tests")
        print("  python3 run.py Programs/example1/prog.txt test_mems/mem1.txt            # Run specific test")
        print("  python3 run.py Programs/example1/prog.txt test_mems/mem1.txt results/emulator/mem1.txt")
        print("  python3 run.py Programs/example1/prog.txt test_mems/mem1.txt results/emulator/mem1.txt --verbose")
        sys.exit(1)
    
    # Get root directory (where the Programs directory is)
    root_dir = Path(__file__).parent.parent.parent.parent
    
    # Convert program path to be relative to root directory
    program_file = Path(sys.argv[1])
    
    # Check for verbose flag
    verbose = '--verbose' in sys.argv
    
    # Load test configuration
    config_file = root_dir / program_file.parent / 'config.json'
    if not config_file.exists():
        print(f"Error: No config.json found in {program_file.parent}")
        sys.exit(1)
        
    config = load_config(config_file)
    if not config:
        sys.exit(1)
    
    # If no specific test is provided, run all tests from config
    if len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2] == '--verbose'):
        all_passed = True
        for test_case in config['test_cases']:
            memory_file = program_file.parent / test_case['memory']
            output_file = program_file.parent / 'results' / 'emulator' / Path(test_case['memory']).name
            
            if verbose:
                print(f"\nRunning test: {test_case['name']}")
                print(f"Memory file: {memory_file}")
                print(f"Output file: {output_file}")
                print("----------------------------------------")
            else:
                print(f"\nTest: {test_case['name']}")
            
            # Run emulator for this test
            emulator = TUCAEmulator(verbose=verbose, minimal=not verbose)
            try:
                final_state = emulator.run_program(
                    program_file=program_file,
                    memory_file=memory_file
                )
                
                if final_state is None:
                    all_passed = False
                    continue
                
                # Convert expected memory to integers
                expected_memory = {
                    int(addr.replace('0x', ''), 16): int(value.replace('0x', ''), 16)
                    for addr, value in test_case['expected']['memory'].items()
                }
                
                # Show memory map and save results
                print_memory_map(final_state.memory, expected_memory, final_state.instruction_count)
                write_results(final_state.memory, output_file)
                
                if not verify_results(output_file, test_case['expected']):
                    all_passed = False
                    
            except Exception as e:
                print(f"Error running test {test_case['name']}: {e}")
                all_passed = False
                
        # Final summary
        if all_passed:
            print("\n✅ All tests passed")
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
            
    else:
        # Run specific test
        memory_file = Path(sys.argv[2])
        output_file = None
        if len(sys.argv) > 3 and not sys.argv[3].startswith('--'):
            output_file = Path(sys.argv[3])
        
        # Find matching test case
        test_case = next(
            (test for test in config['test_cases'] 
             if test['memory'].endswith(memory_file.name)),
            None
        )
        
        if test_case:
            expected_memory = {
                int(addr.replace('0x', ''), 16): int(value.replace('0x', ''), 16)
                for addr, value in test_case['expected']['memory'].items()
            }
        else:
            expected_memory = None
        
        # Run emulator
        emulator = TUCAEmulator(verbose=verbose, minimal=not verbose)
        try:
            if verbose:
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
            
            # Always show the final memory map with expected values if available
            print_memory_map(final_state.memory, expected_memory, final_state.instruction_count)
            
            # Save results if output file specified
            if output_file:
                write_results(final_state.memory, output_file)
                if verbose:
                    print(f"\nResults written to: {output_file}")
                
                # If this is a test case, verify against expected output
                if expected_memory:
                    if verify_results(output_file, test_case['expected']):
                        print("✅ All results match expected values")
                    else:
                        print("❌ Some results do not match expected values")
                        sys.exit(1)
                
        except Exception as e:
            print(f"Error running program: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 