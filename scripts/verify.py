#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from Pipeline.Emulator.src.TUCA51_emulator import TUCAEmulator

def run_emulator(program: Path, memory: Path) -> Dict[int, int]:
    """Run program through emulator and return final memory state"""
    emulator = TUCAEmulator(verbose=False)
    final_state = emulator.run_program(
        program_file=program,
        memory_file=memory
    )
    return final_state.memory

def read_verilog_results(results_file: Path) -> Dict[int, int]:
    """Read memory dump from Verilog simulation"""
    memory = {}
    with open(results_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            # Expected format: addr=value (in hex)
            # Example: 02=42
            try:
                addr, value = line.split('=')
                addr = int(addr, 16)
                value = int(value, 16)
                memory[addr] = value
            except ValueError as e:
                print(f"Warning: Skipping invalid line in results file: {line}")
                continue
    return memory

def verify_results(
    prog_dir: Path,
    test_name: str,
    emulator_mem: Dict[int, int],
    verilog_mem: Dict[int, int],
    expected: Dict[str, Any]
) -> bool:
    """Compare emulator and Verilog results"""
    success = True
    report = []
    
    # First check expected memory locations from config
    if "memory" in expected:
        for addr_str, expected_val in expected["memory"].items():
            addr = int(addr_str.replace("0x", ""), 16)
            emu_val = emulator_mem.get(addr, 0)
            ver_val = verilog_mem.get(addr, 0)
            
            report.append(f"\nChecking expected memory location 0x{addr:02x}:")
            report.append(f"  Expected: 0x{expected_val:02x}")
            report.append(f"  Emulator: 0x{emu_val:02x}")
            report.append(f"  Verilog:  0x{ver_val:02x}")
            
            if emu_val != expected_val:
                report.append("  ❌ Emulator result does not match expected")
                success = False
            if ver_val != expected_val:
                report.append("  ❌ Verilog result does not match expected")
                success = False
            if emu_val == ver_val == expected_val:
                report.append("  ✅ All results match!")
    
    # Then check all memory locations for emulator vs verilog consistency
    mismatches = []
    for addr in range(256):  # Check all memory locations
        emu_val = emulator_mem.get(addr, 0)
        ver_val = verilog_mem.get(addr, 0)
        if emu_val != ver_val:
            mismatches.append(
                f"0x{addr:02x}: Emulator=0x{emu_val:02x}, Verilog=0x{ver_val:02x}"
            )
    
    if mismatches:
        report.append("\nMismatches between Emulator and Verilog:")
        report.extend(mismatches)
        success = False
    else:
        report.append("\n✅ All memory locations match between Emulator and Verilog!")
    
    # Write report
    report_file = prog_dir / "results" / "verify" / f"{test_name}.txt"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"\nVerification report written to: {report_file}")
    return success

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 verify.py <program> <test_name>")
        print("Example: python3 verify.py example1 mem1")
        sys.exit(1)
    
    program_dir = sys.argv[1]
    test_name = sys.argv[2]
    
    # Setup paths
    prog_dir = Path("Programs") / program_dir
    if not prog_dir.exists():
        print(f"Error: Program directory {prog_dir} not found")
        sys.exit(1)
    
    config_path = prog_dir / "config.json"
    if not config_path.exists():
        print(f"Error: Config file {config_path} not found")
        sys.exit(1)
    
    # Load config
    with open(config_path) as f:
        config = json.load(f)
    
    # Find test case config
    test_case = None
    for test in config["test_cases"]:
        if test["name"] == test_name:
            test_case = test
            break
    
    if test_case is None:
        print(f"Error: Test case {test_name} not found in config")
        sys.exit(1)
    
    # Setup paths for program and test files
    program = prog_dir / "build" / f"{Path(config['program']).stem}.mem"
    memory = prog_dir / test_case["memory"]
    results_dir = prog_dir / "results"
    emulator_results = results_dir / "emulator" / f"{test_name}.txt"
    verilog_results = results_dir / "verilog" / f"{test_name}.txt"
    
    if not program.exists():
        print(f"Error: Compiled program {program} not found")
        print("Did you run ./scripts/build.py build first?")
        sys.exit(1)
    if not memory.exists():
        print(f"Error: Test memory file {memory} not found")
        sys.exit(1)
    if not emulator_results.exists():
        print(f"Error: Emulator results file {emulator_results} not found")
        print("Did you run 'tuca emu' first?")
        sys.exit(1)
    if not verilog_results.exists():
        print(f"Error: Verilog results file {verilog_results} not found")
        print("Did you run the Verilog simulation first?")
        sys.exit(1)
    
    # Run verification
    print(f"\nVerifying {program_dir} {test_name}...")
    print(f"Program: {program}")
    print(f"Memory:  {memory}")
    print(f"Emulator Results: {emulator_results}")
    print(f"Verilog Results:  {verilog_results}")
    
    try:
        # Read results
        print("\nReading emulator results...")
        emulator_mem = read_verilog_results(emulator_results)
        
        print("Reading Verilog results...")
        verilog_mem = read_verilog_results(verilog_results)
        
        # Compare results
        print("Comparing results...")
        success = verify_results(
            prog_dir=prog_dir,
            test_name=test_name,
            emulator_mem=emulator_mem,
            verilog_mem=verilog_mem,
            expected=test_case["expected"]
        )
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 