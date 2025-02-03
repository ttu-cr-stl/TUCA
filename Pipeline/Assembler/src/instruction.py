from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Dict, List, Tuple

class InstructionType(Enum):
    JUMP = auto()      # Jump instructions (jmp)
    LOAD = auto()      # Load instructions (ld, ldi, ldr)
    STORE = auto()     # Store instructions (st, str)
    ALU = auto()       # ALU operations (add, sub, and, or, etc.)
    BRANCH = auto()    # Branch instructions (if, skipif)
    SPECIAL = auto()   # Special instructions (halt, readpc)

class Opcode(Enum):
    # Basic instructions (4-bit opcode)
    JMP = 0b0000      # Jump absolute
    LD = 0b0001       # Load from memory
    LDI = 0b0010      # Load immediate
    ST = 0b0011       # Store to memory
    ADD = 0b0100      # Add
    AND = 0b0101      # Bitwise AND
    OR = 0b0110       # Bitwise OR
    NOT = 0b0111      # Bitwise NOT
    NEG = 0b1000      # Two's complement negation
    SHL = 0b1001      # Shift left
    SHR = 0b1010      # Shift right
    EQ = 0b1011       # Equal comparison
    GT = 0b1100       # Greater than comparison
    IF = 0b1101       # Conditional execution
    SKIPIF = 0b1110   # Conditional skip
    HALT = 0b1111     # Halt execution

@dataclass
class Instruction:
    """Represents a TUCA instruction with all its fields."""
    opcode: Opcode
    rd: Optional[int] = None      # Destination register
    rs1: Optional[int] = None     # Source register 1
    rs2: Optional[int] = None     # Source register 2
    imm: Optional[int] = None     # Immediate value
    addr: Optional[int] = None    # Memory address
    shift_amount: Optional[int] = None  # For shift instructions
    
    # Instruction format specifications
    OPCODE_WIDTH: int = 4
    REG_WIDTH: int = 4
    IMM_WIDTH: int = 8
    ADDR_WIDTH: int = 8
    INSTRUCTION_WIDTH: int = 16
    
    @classmethod
    def from_parts(cls, opcode: str, parts: List[str]) -> 'Instruction':
        """Create an instruction from assembly parts."""
        op = Opcode[opcode.upper()]
        
        try:
            # Extract register numbers, removing 'r' prefix
            def parse_reg(reg_str: str) -> int:
                if not reg_str.startswith('r'):
                    raise ValueError(f"Invalid register format: {reg_str}")
                reg_num = int(reg_str[1:])
                if not (0 <= reg_num < 16):
                    raise ValueError("Register number must be between 0 and 15")
                return reg_num
            
            if op == Opcode.JMP:
                # jmp addr
                addr = int(parts[0], 0) if '0x' in parts[0] else int(parts[0])
                return cls(op, addr=addr)
                
            elif op == Opcode.LD:
                # ld addr reg
                addr = int(parts[0], 0) if '0x' in parts[0] else int(parts[0])
                rd = parse_reg(parts[1])
                return cls(op, rd=rd, addr=addr)
                
            elif op == Opcode.LDI:
                # ldi val reg
                imm = int(parts[0], 0) if '0x' in parts[0] else int(parts[0])
                rd = parse_reg(parts[1])
                return cls(op, rd=rd, imm=imm)
                
            elif op == Opcode.ST:
                # st reg addr
                rs1 = parse_reg(parts[0])
                addr = int(parts[1], 0) if '0x' in parts[1] else int(parts[1])
                return cls(op, rs1=rs1, addr=addr)
                
            elif op in [Opcode.ADD, Opcode.AND, Opcode.OR, Opcode.EQ, Opcode.GT]:
                # op reg1 reg2 reg3
                rs1 = parse_reg(parts[0])
                rs2 = parse_reg(parts[1])
                rd = parse_reg(parts[2])
                return cls(op, rd=rd, rs1=rs1, rs2=rs2)
                
            elif op in [Opcode.NOT, Opcode.NEG]:
                # op reg1 reg2
                rs1 = parse_reg(parts[0])
                rd = parse_reg(parts[1])
                return cls(op, rd=rd, rs1=rs1)
                
            elif op in [Opcode.SHL, Opcode.SHR]:
                # op reg1 n reg2
                rs1 = parse_reg(parts[0])
                shift_amount = int(parts[1])
                rd = parse_reg(parts[2])
                if not (1 <= shift_amount <= 7):
                    raise ValueError("Shift amount must be between 1 and 7")
                return cls(op, rd=rd, rs1=rs1, shift_amount=shift_amount)
                
            elif op in [Opcode.IF, Opcode.SKIPIF]:
                # if/skipif reg1
                rs1 = parse_reg(parts[0])
                return cls(op, rs1=rs1)
                
            elif op == Opcode.HALT:
                # halt
                return cls(op)
                
            raise ValueError(f"Invalid instruction format for {opcode}")
            
        except (IndexError, ValueError) as e:
            raise ValueError(f"Error parsing instruction parts: {str(e)}")
    
    def encode(self) -> int:
        """Encode the instruction into its binary representation."""
        encoded = self.opcode.value << 12  # 4-bit opcode
        
        if self.opcode == Opcode.JMP:
            # Format: opcode(4) | address(12)
            encoded |= self.addr & 0xFFF
            
        elif self.opcode == Opcode.LD:
            # Format: opcode(4) | address(8) | reg(4)
            encoded |= ((self.addr & 0xFF) << 4) | (self.rd & 0xF)
            
        elif self.opcode == Opcode.LDI:
            # Format: opcode(4) | value(8) | reg(4)
            encoded |= ((self.imm & 0xFF) << 4) | (self.rd & 0xF)
            
        elif self.opcode == Opcode.ST:
            # Format: opcode(4) | reg(4) | address(8)
            encoded |= ((self.rs1 & 0xF) << 8) | (self.addr & 0xFF)
            
        elif self.opcode in [Opcode.ADD, Opcode.AND, Opcode.OR, Opcode.EQ, Opcode.GT]:
            # Format: opcode(4) | reg1(4) | reg2(4) | reg3(4)
            encoded |= ((self.rs1 & 0xF) << 8) | ((self.rs2 & 0xF) << 4) | (self.rd & 0xF)
            
        elif self.opcode in [Opcode.NOT, Opcode.NEG]:
            # Format: opcode(4) | reg1(4) | reg2(4)
            encoded |= ((self.rs1 & 0xF) << 8) | ((self.rd & 0xF) << 4)
            
        elif self.opcode in [Opcode.SHL, Opcode.SHR]:
            # Format: opcode(4) | reg1(4) | n(4) | reg2(4)
            encoded |= ((self.rs1 & 0xF) << 8) | ((self.shift_amount & 0xF) << 4) | (self.rd & 0xF)
            
        elif self.opcode in [Opcode.IF, Opcode.SKIPIF]:
            # Format: opcode(4) | reg1(4)
            encoded |= (self.rs1 & 0xF) << 8
            
        elif self.opcode == Opcode.HALT:
            # Format: opcode(4) | 0000 0000 0000
            pass
            
        return encoded
    
    def to_hex(self) -> str:
        """Convert the encoded instruction to a hex string."""
        return f"{self.encode():04x}"
    
    def to_binary(self) -> str:
        """Convert the encoded instruction to a binary string."""
        return f"{self.encode():016b}"
