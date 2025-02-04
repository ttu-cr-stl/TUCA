# Changelog

All notable changes to the TUCA-5.1 project are documented in this file.

## [1.0.0] - 2024-02-04

### Added

#### Project Structure

- Organized repository into a structured pipeline architecture
- Added comprehensive project documentation and README files
- Introduced requirements.txt for dependency management
- Added .gitignore and .gitattributes for better repository management

#### Pipeline Components

- Created modular pipeline architecture in `/Pipeline` directory
  - Enhanced Emulator with class-based implementation, testing support, and improved output modes
  - Added Assembler component for TUCA assembly processing
  - Added Processor component with 5-stage pipeline hardware implementation
  - Comprehensive documentation for all components

#### Build System

- Added unified build system with cross-platform support:
  - build.py for program compilation
  - compile.py for assembly processing
  - verify.py for result verification
  - tuca and tuca.bat shell scripts for unified command interface

### Modified

- Enhanced the original TUCA51 emulator with:
  - Class-based architecture for better testing and reuse
  - Support for multiple emulator instances
  - Configurable output modes (verbose/minimal)
  - Improved error handling and state management
- Standardized program organization with configuration files and test structures

### Base Reference (Original Components)

The project evolved from these original components:

- Original TUCA51_emulator.py script
- Example TUCA programs in `/Programs/examples/`:
  - addTwoNums
  - multiplyTwoNums
  - storeLargest
- TUCA Reference documentation:
  - TUCA-5.1 Assembly Language Reference Manual
  - TUCA-5.1 Architecture Specification

This changelog represents the transition from the original emulator script to a full-featured TUCA development environment.
