# SPDX-License-Identifier: MIT
# Copyright (C) 2018-present iced project and contributors

import pytest
from iced_x86 import *
from typing import Any, Callable, Union

@pytest.mark.parametrize("bitness, data, options, created_instr", [
	(64, b"\x90", DecoderOptions.NONE, Instruction.create(Code.NOPD)),
	(64, b"\x48\xB9\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", DecoderOptions.NONE, Instruction.create_reg_i64(Code.MOV_R64_IMM64, Register.RCX, -1)),
	(64, b"\x48\xB9\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", DecoderOptions.NONE, Instruction.create_reg_i32(Code.MOV_R64_IMM64, Register.RCX, -1)),
	(64, b"\x48\xB9\x12\x34\x56\x78\x9A\xBC\xDE\x31", DecoderOptions.NONE, Instruction.create_reg_u64(Code.MOV_R64_IMM64, Register.RCX, 0x31DE_BC9A_7856_3412)),
	(64, b"\x48\xB9\xFF\xFF\xFF\xFF\x00\x00\x00\x00", DecoderOptions.NONE, Instruction.create_reg_u32(Code.MOV_R64_IMM64, Register.RCX, 0xFFFF_FFFF)),
	(64, b"\x8F\xC1", DecoderOptions.NONE, Instruction.create_reg(Code.POP_RM64, Register.RCX)),
	(64, b"\x64\x8F\x84\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_mem(Code.POP_RM64, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS))),
	(64, b"\xC6\xF8\x5A", DecoderOptions.NONE, Instruction.create_u32(Code.XABORT_IMM8, 0x5A)),
	(64, b"\x66\x68\x5A\xA5", DecoderOptions.NONE, Instruction.create_i32(Code.PUSH_IMM16, 0xA55A)),
	(32, b"\x68\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_i32(Code.PUSHD_IMM32, 0x3412_A55A)),
	(64, b"\x66\x6A\x5A", DecoderOptions.NONE, Instruction.create_i32(Code.PUSHW_IMM8, 0x5A)),
	(32, b"\x6A\x5A", DecoderOptions.NONE, Instruction.create_i32(Code.PUSHD_IMM8, 0x5A)),
	(64, b"\x6A\x5A", DecoderOptions.NONE, Instruction.create_i32(Code.PUSHQ_IMM8, 0x5A)),
	(64, b"\x68\x5A\xA5\x12\xA4", DecoderOptions.NONE, Instruction.create_i32(Code.PUSHQ_IMM32, -0x5BED_5AA6)),
	(32, b"\x66\x70\x5A", DecoderOptions.NONE, Instruction.create_branch(Code.JO_REL8_16, 0x4D)),
	(32, b"\x70\x5A", DecoderOptions.NONE, Instruction.create_branch(Code.JO_REL8_32, 0x8000_004C)),
	(64, b"\x70\x5A", DecoderOptions.NONE, Instruction.create_branch(Code.JO_REL8_64, 0x8000_0000_0000_004C)),
	(32, b"\x66\x9A\x12\x34\x56\x78", DecoderOptions.NONE, Instruction.create_far_branch(Code.CALL_PTR1616, 0x7856, 0x3412)),
	(32, b"\x9A\x12\x34\x56\x78\x9A\xBC", DecoderOptions.NONE, Instruction.create_far_branch(Code.CALL_PTR1632, 0xBC9A, 0x7856_3412)),
	(16, b"\xC7\xF8\x5A\xA5", DecoderOptions.NONE, Instruction.create_xbegin(16, 0x254E)),
	(32, b"\xC7\xF8\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_xbegin(32, 0xB412_A550)),
	(64, b"\xC7\xF8\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_xbegin(64, 0x8000_0000_3412_A550)),
	(64, b"\x00\xD1", DecoderOptions.NONE, Instruction.create_reg_reg(Code.ADD_RM8_R8, Register.CL, Register.DL)),
	(64, b"\x64\x02\x8C\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_reg_mem(Code.ADD_R8_RM8, Register.CL, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS))),
	(64, b"\x80\xC1\x5A", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM8_IMM8, Register.CL, 0x5A)),
	(64, b"\x66\x81\xC1\x5A\xA5", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM16_IMM16, Register.CX, 0xA55A)),
	(64, b"\x81\xC1\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM32_IMM32, Register.ECX, 0x3412_A55A)),
	(64, b"\x48\xB9\x04\x15\x26\x37\xA5\x5A\x56\x78", DecoderOptions.NONE, Instruction.create_reg_u64(Code.MOV_R64_IMM64, Register.RCX, 0x7856_5AA5_3726_1504)),
	(64, b"\x66\x83\xC1\x5A", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM16_IMM8, Register.CX, 0x5A)),
	(64, b"\x83\xC1\x5A", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM32_IMM8, Register.ECX, 0x5A)),
	(64, b"\x48\x83\xC1\x5A", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM64_IMM8, Register.RCX, 0x5A)),
	(64, b"\x48\x81\xC1\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_reg_i32(Code.ADD_RM64_IMM32, Register.RCX, 0x3412_A55A)),
	(64, b"\x64\xA0\x12\x34\x56\x78\x9A\xBC\xDE\xF0", DecoderOptions.NONE, Instruction.create_reg_mem(Code.MOV_AL_MOFFS8, Register.AL, MemoryOperand(Register.NONE, Register.NONE, 1, -0x0F21_4365_87A9_CBEE, 8, False, Register.FS))),
	(64, b"\x64\x00\x94\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_mem_reg(Code.ADD_RM8_R8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DL)),
	(64, b"\x64\x80\x84\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM8_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x66\x81\x84\x75\x01\xEF\xCD\xAB\x5A\xA5", DecoderOptions.NONE, Instruction.create_mem_u32(Code.ADD_RM16_IMM16, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA55A)),
	(64, b"\x64\x81\x84\x75\x01\xEF\xCD\xAB\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM32_IMM32, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A)),
	(64, b"\x64\x66\x83\x84\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM16_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x83\x84\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM32_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x48\x83\x84\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM64_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x48\x81\x84\x75\x01\xEF\xCD\xAB\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_mem_i32(Code.ADD_RM64_IMM32, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A)),
	(64, b"\xE6\x5A", DecoderOptions.NONE, Instruction.create_i32_reg(Code.OUT_IMM8_AL, 0x5A, Register.AL)),
	(64, b"\xE6\x5A", DecoderOptions.NONE, Instruction.create_u32_reg(Code.OUT_IMM8_AL, 0x5A, Register.AL)),
	(64, b"\x66\xC8\x5A\xA5\xA6", DecoderOptions.NONE, Instruction.create_i32_i32(Code.ENTERW_IMM16_IMM8, 0xA55A, 0xA6)),
	(64, b"\x66\xC8\x5A\xA5\xA6", DecoderOptions.NONE, Instruction.create_u32_u32(Code.ENTERW_IMM16_IMM8, 0xA55A, 0xA6)),
	(64, b"\x64\xA2\x12\x34\x56\x78\x9A\xBC\xDE\xF0", DecoderOptions.NONE, Instruction.create_mem_reg(Code.MOV_MOFFS8_AL, MemoryOperand(Register.NONE, Register.NONE, 1, -0x0F21_4365_87A9_CBEE, 8, False, Register.FS), Register.AL)),
	(64, b"\x66\x69\xCA\xA5\x5A", DecoderOptions.NONE, Instruction.create_reg_reg_u32(Code.IMUL_R16_RM16_IMM16, Register.CX, Register.DX, 0x5AA5)),
	(64, b"\x69\xCA\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM32, Register.ECX, Register.EDX, 0x3412_A55A)),
	(64, b"\x66\x6B\xCA\x5A", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.IMUL_R16_RM16_IMM8, Register.CX, Register.DX, 0x5A)),
	(64, b"\x6B\xCA\x5A", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM8, Register.ECX, Register.EDX, 0x5A)),
	(64, b"\x48\x6B\xCA\x5A", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM8, Register.RCX, Register.RDX, 0x5A)),
	(64, b"\x48\x69\xCA\x5A\xA5\x12\xA4", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM32, Register.RCX, Register.RDX, -0x5BED_5AA6)),
	(64, b"\x64\x66\x69\x8C\x75\x01\xEF\xCD\xAB\x5A\xA5", DecoderOptions.NONE, Instruction.create_reg_mem_u32(Code.IMUL_R16_RM16_IMM16, Register.CX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA55A)),
	(64, b"\x64\x69\x8C\x75\x01\xEF\xCD\xAB\x5A\xA5\x12\x34", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.IMUL_R32_RM32_IMM32, Register.ECX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A)),
	(64, b"\x64\x66\x6B\x8C\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.IMUL_R16_RM16_IMM8, Register.CX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x6B\x8C\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.IMUL_R32_RM32_IMM8, Register.ECX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x48\x6B\x8C\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.IMUL_R64_RM64_IMM8, Register.RCX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A)),
	(64, b"\x64\x48\x69\x8C\x75\x01\xEF\xCD\xAB\x5A\xA5\x12\xA4", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.IMUL_R64_RM64_IMM32, Register.RCX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), -0x5BED_5AA6)),
	(64, b"\x66\x0F\x78\xC1\xA5\xFD", DecoderOptions.NONE, Instruction.create_reg_i32_i32(Code.EXTRQ_XMM_IMM8_IMM8, Register.XMM1, 0xA5, 0xFD)),
	(64, b"\x66\x0F\x78\xC1\xA5\xFD", DecoderOptions.NONE, Instruction.create_reg_u32_u32(Code.EXTRQ_XMM_IMM8_IMM8, Register.XMM1, 0xA5, 0xFD)),
	(64, b"\x64\x66\x0F\xA4\x94\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_reg_i32(Code.SHLD_RM16_R16_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DX, 0x5A)),
	(64, b"\x64\x66\x0F\xA4\x94\x75\x01\xEF\xCD\xAB\x5A", DecoderOptions.NONE, Instruction.create_mem_reg_u32(Code.SHLD_RM16_R16_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DX, 0x5A)),
	(64, b"\xF2\x0F\x78\xCA\xA5\xFD", DecoderOptions.NONE, Instruction.create_reg_reg_i32_i32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, Register.XMM1, Register.XMM2, 0xA5, 0xFD)),
	(64, b"\xF2\x0F\x78\xCA\xA5\xFD", DecoderOptions.NONE, Instruction.create_reg_reg_u32_u32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, Register.XMM1, Register.XMM2, 0xA5, 0xFD)),
	(16, b"\x0F\xB8\x55\xAA", DecoderOptions.JMPE, Instruction.create_branch(Code.JMPE_DISP16, 0xAA55)),
	(32, b"\x0F\xB8\x12\x34\x55\xAA", DecoderOptions.JMPE, Instruction.create_branch(Code.JMPE_DISP32, 0xAA55_3412)),
	(32, b"\x64\x67\x6E", DecoderOptions.NONE, Instruction.create_outsb(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\x6E", DecoderOptions.NONE, Instruction.create_outsb(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x6E", DecoderOptions.NONE, Instruction.create_outsb(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x66\x67\x6F", DecoderOptions.NONE, Instruction.create_outsw(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\x67\x6F", DecoderOptions.NONE, Instruction.create_outsw(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\x6F", DecoderOptions.NONE, Instruction.create_outsw(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\x6F", DecoderOptions.NONE, Instruction.create_outsd(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\x6F", DecoderOptions.NONE, Instruction.create_outsd(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x6F", DecoderOptions.NONE, Instruction.create_outsd(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x67\xAE", DecoderOptions.NONE, Instruction.create_scasb(16, RepPrefixKind.NONE)),
	(64, b"\x67\xAE", DecoderOptions.NONE, Instruction.create_scasb(32, RepPrefixKind.NONE)),
	(64, b"\xAE", DecoderOptions.NONE, Instruction.create_scasb(64, RepPrefixKind.NONE)),
	(32, b"\x66\x67\xAF", DecoderOptions.NONE, Instruction.create_scasw(16, RepPrefixKind.NONE)),
	(64, b"\x66\x67\xAF", DecoderOptions.NONE, Instruction.create_scasw(32, RepPrefixKind.NONE)),
	(64, b"\x66\xAF", DecoderOptions.NONE, Instruction.create_scasw(64, RepPrefixKind.NONE)),
	(32, b"\x67\xAF", DecoderOptions.NONE, Instruction.create_scasd(16, RepPrefixKind.NONE)),
	(64, b"\x67\xAF", DecoderOptions.NONE, Instruction.create_scasd(32, RepPrefixKind.NONE)),
	(64, b"\xAF", DecoderOptions.NONE, Instruction.create_scasd(64, RepPrefixKind.NONE)),
	(64, b"\x67\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(32, RepPrefixKind.NONE)),
	(64, b"\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(64, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xAC", DecoderOptions.NONE, Instruction.create_lodsb(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xAC", DecoderOptions.NONE, Instruction.create_lodsb(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xAC", DecoderOptions.NONE, Instruction.create_lodsb(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x66\x67\xAD", DecoderOptions.NONE, Instruction.create_lodsw(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\x67\xAD", DecoderOptions.NONE, Instruction.create_lodsw(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\xAD", DecoderOptions.NONE, Instruction.create_lodsw(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xAD", DecoderOptions.NONE, Instruction.create_lodsd(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xAD", DecoderOptions.NONE, Instruction.create_lodsd(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xAD", DecoderOptions.NONE, Instruction.create_lodsd(64, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x67\x6C", DecoderOptions.NONE, Instruction.create_insb(16, RepPrefixKind.NONE)),
	(64, b"\x67\x6C", DecoderOptions.NONE, Instruction.create_insb(32, RepPrefixKind.NONE)),
	(64, b"\x6C", DecoderOptions.NONE, Instruction.create_insb(64, RepPrefixKind.NONE)),
	(32, b"\x66\x67\x6D", DecoderOptions.NONE, Instruction.create_insw(16, RepPrefixKind.NONE)),
	(64, b"\x66\x67\x6D", DecoderOptions.NONE, Instruction.create_insw(32, RepPrefixKind.NONE)),
	(64, b"\x66\x6D", DecoderOptions.NONE, Instruction.create_insw(64, RepPrefixKind.NONE)),
	(32, b"\x67\x6D", DecoderOptions.NONE, Instruction.create_insd(16, RepPrefixKind.NONE)),
	(64, b"\x67\x6D", DecoderOptions.NONE, Instruction.create_insd(32, RepPrefixKind.NONE)),
	(64, b"\x6D", DecoderOptions.NONE, Instruction.create_insd(64, RepPrefixKind.NONE)),
	(32, b"\x67\xAA", DecoderOptions.NONE, Instruction.create_stosb(16, RepPrefixKind.NONE)),
	(64, b"\x67\xAA", DecoderOptions.NONE, Instruction.create_stosb(32, RepPrefixKind.NONE)),
	(64, b"\xAA", DecoderOptions.NONE, Instruction.create_stosb(64, RepPrefixKind.NONE)),
	(32, b"\x66\x67\xAB", DecoderOptions.NONE, Instruction.create_stosw(16, RepPrefixKind.NONE)),
	(64, b"\x66\x67\xAB", DecoderOptions.NONE, Instruction.create_stosw(32, RepPrefixKind.NONE)),
	(64, b"\x66\xAB", DecoderOptions.NONE, Instruction.create_stosw(64, RepPrefixKind.NONE)),
	(32, b"\x67\xAB", DecoderOptions.NONE, Instruction.create_stosd(16, RepPrefixKind.NONE)),
	(64, b"\x67\xAB", DecoderOptions.NONE, Instruction.create_stosd(32, RepPrefixKind.NONE)),
	(64, b"\xAB", DecoderOptions.NONE, Instruction.create_stosd(64, RepPrefixKind.NONE)),
	(64, b"\x67\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(32, RepPrefixKind.NONE)),
	(64, b"\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(64, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x66\x67\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\x67\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(64, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xA4", DecoderOptions.NONE, Instruction.create_movsb(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xA4", DecoderOptions.NONE, Instruction.create_movsb(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xA4", DecoderOptions.NONE, Instruction.create_movsb(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x66\x67\xA5", DecoderOptions.NONE, Instruction.create_movsw(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\x67\xA5", DecoderOptions.NONE, Instruction.create_movsw(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x66\xA5", DecoderOptions.NONE, Instruction.create_movsw(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\xA5", DecoderOptions.NONE, Instruction.create_movsd(16, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\xA5", DecoderOptions.NONE, Instruction.create_movsd(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\xA5", DecoderOptions.NONE, Instruction.create_movsd(64, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x67\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(32, Register.FS, RepPrefixKind.NONE)),
	(64, b"\x64\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(64, Register.FS, RepPrefixKind.NONE)),
	(32, b"\x64\x67\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovq(16, Register.MM2, Register.MM3, Register.FS)),
	(64, b"\x64\x67\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovq(32, Register.MM2, Register.MM3, Register.FS)),
	(64, b"\x64\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovq(64, Register.MM2, Register.MM3, Register.FS)),
	(32, b"\x64\x67\x66\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovdqu(16, Register.XMM2, Register.XMM3, Register.FS)),
	(64, b"\x64\x67\x66\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovdqu(32, Register.XMM2, Register.XMM3, Register.FS)),
	(64, b"\x64\x66\x0F\xF7\xD3", DecoderOptions.NONE, Instruction.create_maskmovdqu(64, Register.XMM2, Register.XMM3, Register.FS)),

	(32, b"\x64\x67\xF3\x6E", DecoderOptions.NONE, Instruction.create_outsb(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\x6E", DecoderOptions.NONE, Instruction.create_outsb(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\x6E", DecoderOptions.NONE, Instruction.create_outsb(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x66\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsw(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsw(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsw(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsd(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsd(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\x6F", DecoderOptions.NONE, Instruction.create_outsd(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\xAE", DecoderOptions.NONE, Instruction.create_scasb(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\xAE", DecoderOptions.NONE, Instruction.create_scasb(32, RepPrefixKind.REPE)),
	(64, b"\xF3\xAE", DecoderOptions.NONE, Instruction.create_scasb(64, RepPrefixKind.REPE)),
	(32, b"\x66\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasw(16, RepPrefixKind.REPE)),
	(64, b"\x66\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasw(32, RepPrefixKind.REPE)),
	(64, b"\x66\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasw(64, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasd(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasd(32, RepPrefixKind.REPE)),
	(64, b"\xF3\xAF", DecoderOptions.NONE, Instruction.create_scasd(64, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(32, RepPrefixKind.REPE)),
	(64, b"\xF3\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(64, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xAC", DecoderOptions.NONE, Instruction.create_lodsb(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xAC", DecoderOptions.NONE, Instruction.create_lodsb(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xAC", DecoderOptions.NONE, Instruction.create_lodsb(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x66\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsw(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsw(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsw(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsd(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsd(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xAD", DecoderOptions.NONE, Instruction.create_lodsd(64, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\x6C", DecoderOptions.NONE, Instruction.create_insb(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\x6C", DecoderOptions.NONE, Instruction.create_insb(32, RepPrefixKind.REPE)),
	(64, b"\xF3\x6C", DecoderOptions.NONE, Instruction.create_insb(64, RepPrefixKind.REPE)),
	(32, b"\x66\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_insw(16, RepPrefixKind.REPE)),
	(64, b"\x66\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_insw(32, RepPrefixKind.REPE)),
	(64, b"\x66\xF3\x6D", DecoderOptions.NONE, Instruction.create_insw(64, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_insd(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_insd(32, RepPrefixKind.REPE)),
	(64, b"\xF3\x6D", DecoderOptions.NONE, Instruction.create_insd(64, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\xAA", DecoderOptions.NONE, Instruction.create_stosb(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\xAA", DecoderOptions.NONE, Instruction.create_stosb(32, RepPrefixKind.REPE)),
	(64, b"\xF3\xAA", DecoderOptions.NONE, Instruction.create_stosb(64, RepPrefixKind.REPE)),
	(32, b"\x66\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosw(16, RepPrefixKind.REPE)),
	(64, b"\x66\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosw(32, RepPrefixKind.REPE)),
	(64, b"\x66\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosw(64, RepPrefixKind.REPE)),
	(32, b"\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosd(16, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosd(32, RepPrefixKind.REPE)),
	(64, b"\xF3\xAB", DecoderOptions.NONE, Instruction.create_stosd(64, RepPrefixKind.REPE)),
	(64, b"\x67\xF3\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(32, RepPrefixKind.REPE)),
	(64, b"\xF3\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(64, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x66\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(64, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xA4", DecoderOptions.NONE, Instruction.create_movsb(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xA4", DecoderOptions.NONE, Instruction.create_movsb(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xA4", DecoderOptions.NONE, Instruction.create_movsb(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x66\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsw(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsw(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x66\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsw(64, Register.FS, RepPrefixKind.REPE)),
	(32, b"\x64\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsd(16, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsd(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\xA5", DecoderOptions.NONE, Instruction.create_movsd(64, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\x67\xF3\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(32, Register.FS, RepPrefixKind.REPE)),
	(64, b"\x64\xF3\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(64, Register.FS, RepPrefixKind.REPE)),

	(32, b"\x64\x67\xF2\x6E", DecoderOptions.NONE, Instruction.create_outsb(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\x6E", DecoderOptions.NONE, Instruction.create_outsb(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\x6E", DecoderOptions.NONE, Instruction.create_outsb(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x66\x67\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsw(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\x67\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsw(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsw(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsd(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsd(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\x6F", DecoderOptions.NONE, Instruction.create_outsd(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\xAE", DecoderOptions.NONE, Instruction.create_scasb(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\xAE", DecoderOptions.NONE, Instruction.create_scasb(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\xAE", DecoderOptions.NONE, Instruction.create_scasb(64, RepPrefixKind.REPNE)),
	(32, b"\x66\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasw(16, RepPrefixKind.REPNE)),
	(64, b"\x66\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasw(32, RepPrefixKind.REPNE)),
	(64, b"\x66\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasw(64, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasd(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasd(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\xAF", DecoderOptions.NONE, Instruction.create_scasd(64, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\x48\xAF", DecoderOptions.NONE, Instruction.create_scasq(64, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xAC", DecoderOptions.NONE, Instruction.create_lodsb(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xAC", DecoderOptions.NONE, Instruction.create_lodsb(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xAC", DecoderOptions.NONE, Instruction.create_lodsb(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x66\x67\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsw(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\x67\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsw(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsw(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsd(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsd(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xAD", DecoderOptions.NONE, Instruction.create_lodsd(64, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\x48\xAD", DecoderOptions.NONE, Instruction.create_lodsq(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\x6C", DecoderOptions.NONE, Instruction.create_insb(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\x6C", DecoderOptions.NONE, Instruction.create_insb(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\x6C", DecoderOptions.NONE, Instruction.create_insb(64, RepPrefixKind.REPNE)),
	(32, b"\x66\x67\xF2\x6D", DecoderOptions.NONE, Instruction.create_insw(16, RepPrefixKind.REPNE)),
	(64, b"\x66\x67\xF2\x6D", DecoderOptions.NONE, Instruction.create_insw(32, RepPrefixKind.REPNE)),
	(64, b"\x66\xF2\x6D", DecoderOptions.NONE, Instruction.create_insw(64, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\x6D", DecoderOptions.NONE, Instruction.create_insd(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\x6D", DecoderOptions.NONE, Instruction.create_insd(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\x6D", DecoderOptions.NONE, Instruction.create_insd(64, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\xAA", DecoderOptions.NONE, Instruction.create_stosb(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\xAA", DecoderOptions.NONE, Instruction.create_stosb(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\xAA", DecoderOptions.NONE, Instruction.create_stosb(64, RepPrefixKind.REPNE)),
	(32, b"\x66\x67\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosw(16, RepPrefixKind.REPNE)),
	(64, b"\x66\x67\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosw(32, RepPrefixKind.REPNE)),
	(64, b"\x66\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosw(64, RepPrefixKind.REPNE)),
	(32, b"\x67\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosd(16, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosd(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\xAB", DecoderOptions.NONE, Instruction.create_stosd(64, RepPrefixKind.REPNE)),
	(64, b"\x67\xF2\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(32, RepPrefixKind.REPNE)),
	(64, b"\xF2\x48\xAB", DecoderOptions.NONE, Instruction.create_stosq(64, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xA6", DecoderOptions.NONE, Instruction.create_cmpsb(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x66\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsw(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xA7", DecoderOptions.NONE, Instruction.create_cmpsd(64, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\x48\xA7", DecoderOptions.NONE, Instruction.create_cmpsq(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xA4", DecoderOptions.NONE, Instruction.create_movsb(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xA4", DecoderOptions.NONE, Instruction.create_movsb(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xA4", DecoderOptions.NONE, Instruction.create_movsb(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x66\x67\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsw(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\x67\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsw(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x66\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsw(64, Register.FS, RepPrefixKind.REPNE)),
	(32, b"\x64\x67\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsd(16, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsd(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\xA5", DecoderOptions.NONE, Instruction.create_movsd(64, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\x67\xF2\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(32, Register.FS, RepPrefixKind.REPNE)),
	(64, b"\x64\xF2\x48\xA5", DecoderOptions.NONE, Instruction.create_movsq(64, Register.FS, RepPrefixKind.REPNE)),

	(32, b"\x67\xF3\x6E", DecoderOptions.NONE, Instruction.create_rep_outsb(16)),
	(64, b"\x67\xF3\x6E", DecoderOptions.NONE, Instruction.create_rep_outsb(32)),
	(64, b"\xF3\x6E", DecoderOptions.NONE, Instruction.create_rep_outsb(64)),
	(32, b"\x66\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsw(16)),
	(64, b"\x66\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsw(32)),
	(64, b"\x66\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsw(64)),
	(32, b"\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsd(16)),
	(64, b"\x67\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsd(32)),
	(64, b"\xF3\x6F", DecoderOptions.NONE, Instruction.create_rep_outsd(64)),
	(32, b"\x67\xF3\xAE", DecoderOptions.NONE, Instruction.create_repe_scasb(16)),
	(64, b"\x67\xF3\xAE", DecoderOptions.NONE, Instruction.create_repe_scasb(32)),
	(64, b"\xF3\xAE", DecoderOptions.NONE, Instruction.create_repe_scasb(64)),
	(32, b"\x66\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasw(16)),
	(64, b"\x66\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasw(32)),
	(64, b"\x66\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasw(64)),
	(32, b"\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasd(16)),
	(64, b"\x67\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasd(32)),
	(64, b"\xF3\xAF", DecoderOptions.NONE, Instruction.create_repe_scasd(64)),
	(64, b"\x67\xF3\x48\xAF", DecoderOptions.NONE, Instruction.create_repe_scasq(32)),
	(64, b"\xF3\x48\xAF", DecoderOptions.NONE, Instruction.create_repe_scasq(64)),
	(32, b"\x67\xF2\xAE", DecoderOptions.NONE, Instruction.create_repne_scasb(16)),
	(64, b"\x67\xF2\xAE", DecoderOptions.NONE, Instruction.create_repne_scasb(32)),
	(64, b"\xF2\xAE", DecoderOptions.NONE, Instruction.create_repne_scasb(64)),
	(32, b"\x66\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasw(16)),
	(64, b"\x66\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasw(32)),
	(64, b"\x66\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasw(64)),
	(32, b"\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasd(16)),
	(64, b"\x67\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasd(32)),
	(64, b"\xF2\xAF", DecoderOptions.NONE, Instruction.create_repne_scasd(64)),
	(64, b"\x67\xF2\x48\xAF", DecoderOptions.NONE, Instruction.create_repne_scasq(32)),
	(64, b"\xF2\x48\xAF", DecoderOptions.NONE, Instruction.create_repne_scasq(64)),
	(32, b"\x67\xF3\xAC", DecoderOptions.NONE, Instruction.create_rep_lodsb(16)),
	(64, b"\x67\xF3\xAC", DecoderOptions.NONE, Instruction.create_rep_lodsb(32)),
	(64, b"\xF3\xAC", DecoderOptions.NONE, Instruction.create_rep_lodsb(64)),
	(32, b"\x66\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsw(16)),
	(64, b"\x66\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsw(32)),
	(64, b"\x66\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsw(64)),
	(32, b"\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsd(16)),
	(64, b"\x67\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsd(32)),
	(64, b"\xF3\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsd(64)),
	(64, b"\x67\xF3\x48\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsq(32)),
	(64, b"\xF3\x48\xAD", DecoderOptions.NONE, Instruction.create_rep_lodsq(64)),
	(32, b"\x67\xF3\x6C", DecoderOptions.NONE, Instruction.create_rep_insb(16)),
	(64, b"\x67\xF3\x6C", DecoderOptions.NONE, Instruction.create_rep_insb(32)),
	(64, b"\xF3\x6C", DecoderOptions.NONE, Instruction.create_rep_insb(64)),
	(32, b"\x66\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insw(16)),
	(64, b"\x66\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insw(32)),
	(64, b"\x66\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insw(64)),
	(32, b"\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insd(16)),
	(64, b"\x67\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insd(32)),
	(64, b"\xF3\x6D", DecoderOptions.NONE, Instruction.create_rep_insd(64)),
	(32, b"\x67\xF3\xAA", DecoderOptions.NONE, Instruction.create_rep_stosb(16)),
	(64, b"\x67\xF3\xAA", DecoderOptions.NONE, Instruction.create_rep_stosb(32)),
	(64, b"\xF3\xAA", DecoderOptions.NONE, Instruction.create_rep_stosb(64)),
	(32, b"\x66\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosw(16)),
	(64, b"\x66\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosw(32)),
	(64, b"\x66\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosw(64)),
	(32, b"\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosd(16)),
	(64, b"\x67\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosd(32)),
	(64, b"\xF3\xAB", DecoderOptions.NONE, Instruction.create_rep_stosd(64)),
	(64, b"\x67\xF3\x48\xAB", DecoderOptions.NONE, Instruction.create_rep_stosq(32)),
	(64, b"\xF3\x48\xAB", DecoderOptions.NONE, Instruction.create_rep_stosq(64)),
	(32, b"\x67\xF3\xA6", DecoderOptions.NONE, Instruction.create_repe_cmpsb(16)),
	(64, b"\x67\xF3\xA6", DecoderOptions.NONE, Instruction.create_repe_cmpsb(32)),
	(64, b"\xF3\xA6", DecoderOptions.NONE, Instruction.create_repe_cmpsb(64)),
	(32, b"\x66\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsw(16)),
	(64, b"\x66\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsw(32)),
	(64, b"\x66\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsw(64)),
	(32, b"\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsd(16)),
	(64, b"\x67\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsd(32)),
	(64, b"\xF3\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsd(64)),
	(64, b"\x67\xF3\x48\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsq(32)),
	(64, b"\xF3\x48\xA7", DecoderOptions.NONE, Instruction.create_repe_cmpsq(64)),
	(32, b"\x67\xF2\xA6", DecoderOptions.NONE, Instruction.create_repne_cmpsb(16)),
	(64, b"\x67\xF2\xA6", DecoderOptions.NONE, Instruction.create_repne_cmpsb(32)),
	(64, b"\xF2\xA6", DecoderOptions.NONE, Instruction.create_repne_cmpsb(64)),
	(32, b"\x66\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsw(16)),
	(64, b"\x66\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsw(32)),
	(64, b"\x66\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsw(64)),
	(32, b"\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsd(16)),
	(64, b"\x67\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsd(32)),
	(64, b"\xF2\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsd(64)),
	(64, b"\x67\xF2\x48\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsq(32)),
	(64, b"\xF2\x48\xA7", DecoderOptions.NONE, Instruction.create_repne_cmpsq(64)),
	(32, b"\x67\xF3\xA4", DecoderOptions.NONE, Instruction.create_rep_movsb(16)),
	(64, b"\x67\xF3\xA4", DecoderOptions.NONE, Instruction.create_rep_movsb(32)),
	(64, b"\xF3\xA4", DecoderOptions.NONE, Instruction.create_rep_movsb(64)),
	(32, b"\x66\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsw(16)),
	(64, b"\x66\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsw(32)),
	(64, b"\x66\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsw(64)),
	(32, b"\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsd(16)),
	(64, b"\x67\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsd(32)),
	(64, b"\xF3\xA5", DecoderOptions.NONE, Instruction.create_rep_movsd(64)),
	(64, b"\x67\xF3\x48\xA5", DecoderOptions.NONE, Instruction.create_rep_movsq(32)),
	(64, b"\xF3\x48\xA5", DecoderOptions.NONE, Instruction.create_rep_movsq(64)),

	(64, b"\xC5\xE8\x14\xCB", DecoderOptions.NONE, Instruction.create_reg_reg_reg(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, Register.XMM1, Register.XMM2, Register.XMM3)),
	(64, b"\x64\xC5\xE8\x14\x8C\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_reg_reg_mem(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS))),
	(64, b"\x64\xC4\xE2\x61\x90\x8C\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_reg_mem_reg(Code.VEX_VPGATHERDD_XMM_VM32X_XMM, Register.XMM1, MemoryOperand(Register.RBP, Register.XMM6, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM3)),
	(64, b"\x64\xC4\xE2\x69\x2E\x9C\x75\x01\xEF\xCD\xAB", DecoderOptions.NONE, Instruction.create_mem_reg_reg(Code.VEX_VMASKMOVPS_M128_XMM_XMM, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM2, Register.XMM3)),
	(64, b"\xC4\xE3\x69\x4A\xCB\x40", DecoderOptions.NONE, Instruction.create_reg_reg_reg_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4)),
	(64, b"\x64\xC4\xE3\xE9\x5C\x8C\x75\x01\xEF\xCD\xAB\x30", DecoderOptions.NONE, Instruction.create_reg_reg_reg_mem(Code.VEX_VFMADDSUBPS_XMM_XMM_XMM_XMMM128, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS))),
	(64, b"\x64\xC4\xE3\x69\x4A\x8C\x75\x01\xEF\xCD\xAB\x40", DecoderOptions.NONE, Instruction.create_reg_reg_mem_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4)),
	(64, b"\xC4\xE3\x69\x48\xCB\x40", DecoderOptions.NONE, Instruction.create_reg_reg_reg_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4, 0x0)),
	(64, b"\xC4\xE3\x69\x48\xCB\x40", DecoderOptions.NONE, Instruction.create_reg_reg_reg_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4, 0x0)),
	(64, b"\x64\xC4\xE3\xE9\x48\x8C\x75\x01\xEF\xCD\xAB\x31", DecoderOptions.NONE, Instruction.create_reg_reg_reg_mem_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1)),
	(64, b"\x64\xC4\xE3\xE9\x48\x8C\x75\x01\xEF\xCD\xAB\x31", DecoderOptions.NONE, Instruction.create_reg_reg_reg_mem_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1)),
	(64, b"\x64\xC4\xE3\x69\x48\x8C\x75\x01\xEF\xCD\xAB\x41", DecoderOptions.NONE, Instruction.create_reg_reg_mem_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1)),
	(64, b"\x64\xC4\xE3\x69\x48\x8C\x75\x01\xEF\xCD\xAB\x41", DecoderOptions.NONE, Instruction.create_reg_reg_mem_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1)),
	(32, b"\x64\x67\xC5\xF9\xF7\xD3", DecoderOptions.NONE, Instruction.create_vmaskmovdqu(16, Register.XMM2, Register.XMM3, Register.FS)),
	(64, b"\x64\x67\xC5\xF9\xF7\xD3", DecoderOptions.NONE, Instruction.create_vmaskmovdqu(32, Register.XMM2, Register.XMM3, Register.FS)),
	(64, b"\x64\xC5\xF9\xF7\xD3", DecoderOptions.NONE, Instruction.create_vmaskmovdqu(64, Register.XMM2, Register.XMM3, Register.FS)),

	(64, b"\x62\xF1\xF5\x08\x73\xD2\xA5", DecoderOptions.NONE, Instruction.create_reg_reg_i32(Code.EVEX_VPSRLQ_XMM_K1Z_XMMM128B64_IMM8, Register.XMM1, Register.XMM2, 0xA5)),
	(64, b"\x64\x62\xF1\xF5\x08\x73\x94\x75\x01\xEF\xCD\xAB\xA5", DecoderOptions.NONE, Instruction.create_reg_mem_i32(Code.EVEX_VPSRLQ_XMM_K1Z_XMMM128B64_IMM8, Register.XMM1, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5)),
	(64, b"\x62\xF1\x6D\x08\xC4\xCB\xA5", DecoderOptions.NONE, Instruction.create_reg_reg_reg_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, Register.EBX, 0xA5)),
	(64, b"\x62\xF1\x6D\x08\xC4\xCB\xA5", DecoderOptions.NONE, Instruction.create_reg_reg_reg_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, Register.EBX, 0xA5)),
	(64, b"\x64\x62\xF1\x6D\x08\xC4\x8C\x75\x01\xEF\xCD\xAB\xA5", DecoderOptions.NONE, Instruction.create_reg_reg_mem_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5)),
	(64, b"\x64\x62\xF1\x6D\x08\xC4\x8C\x75\x01\xEF\xCD\xAB\xA5", DecoderOptions.NONE, Instruction.create_reg_reg_mem_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5)),
])
def test_create(bitness: int, data: bytes, options: DecoderOptions_, created_instr: Instruction) -> None:
	if bitness == 64:
		ip = 0x7FFF_FFFF_FFFF_FFF0
	elif bitness == 32:
		ip = 0x0000_0000_7FFF_FFF0
	elif bitness == 16:
		ip = 0x0000_0000_0000_7FF0
	else:
		raise ValueError("Invalid bitness")
	decoder = Decoder(bitness, data, options, ip=ip)
	orig_rip = decoder.ip
	decoded_instr = decoder.decode()
	decoded_instr.code_size = CodeSize.UNKNOWN
	decoded_instr.len = 0
	decoded_instr.next_ip = 0
	assert decoded_instr.eq_all_bits(created_instr)

	encoder = Encoder(decoder.bitness)
	encoder.encode(created_instr, orig_rip)
	assert data == encoder.take_buffer()

@pytest.mark.parametrize("instr, data", [
	(Instruction.create_declare_byte_1(0x77), b"\x77"),
	(Instruction.create_declare_byte_2(0x77, 0xA9), b"\x77\xA9"),
	(Instruction.create_declare_byte_3(0x77, 0xA9, 0xCE), b"\x77\xA9\xCE"),
	(Instruction.create_declare_byte_4(0x77, 0xA9, 0xCE, 0x9D), b"\x77\xA9\xCE\x9D"),
	(Instruction.create_declare_byte_5(0x77, 0xA9, 0xCE, 0x9D, 0x55), b"\x77\xA9\xCE\x9D\x55"),
	(Instruction.create_declare_byte_6(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05), b"\x77\xA9\xCE\x9D\x55\x05"),
	(Instruction.create_declare_byte_7(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42), b"\x77\xA9\xCE\x9D\x55\x05\x42"),
	(Instruction.create_declare_byte_8(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C"),
	(Instruction.create_declare_byte_9(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86"),
	(Instruction.create_declare_byte_10(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32"),
	(Instruction.create_declare_byte_11(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE"),
	(Instruction.create_declare_byte_12(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE, 0x4F), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE\x4F"),
	(Instruction.create_declare_byte_13(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE, 0x4F, 0x34), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE\x4F\x34"),
	(Instruction.create_declare_byte_14(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE, 0x4F, 0x34, 0x27), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE\x4F\x34\x27"),
	(Instruction.create_declare_byte_15(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE, 0x4F, 0x34, 0x27, 0xAA), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE\x4F\x34\x27\xAA"),
	(Instruction.create_declare_byte_16(0x77, 0xA9, 0xCE, 0x9D, 0x55, 0x05, 0x42, 0x6C, 0x86, 0x32, 0xFE, 0x4F, 0x34, 0x27, 0xAA, 0x08), b"\x77\xA9\xCE\x9D\x55\x05\x42\x6C\x86\x32\xFE\x4F\x34\x27\xAA\x08"),
])
def test_db(instr: Instruction, data: bytes) -> None:
	assert instr.code == Code.DECLAREBYTE
	assert instr.declare_data_len == len(data)
	for i, d in enumerate(data):
		assert instr.get_declare_byte_value(i) == d
	db_slice = Instruction.create_declare_byte(data)
	assert instr.eq_all_bits(db_slice)

@pytest.mark.parametrize("instr, data", [
	(Instruction.create_declare_word_1(0x77A9), [0x77A9]),
	(Instruction.create_declare_word_2(0x77A9, 0xCE9D), [0x77A9, 0xCE9D]),
	(Instruction.create_declare_word_3(0x77A9, 0xCE9D, 0x5505), [0x77A9, 0xCE9D, 0x5505]),
	(Instruction.create_declare_word_4(0x77A9, 0xCE9D, 0x5505, 0x426C), [0x77A9, 0xCE9D, 0x5505, 0x426C]),
	(Instruction.create_declare_word_5(0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632), [0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632]),
	(Instruction.create_declare_word_6(0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F), [0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F]),
	(Instruction.create_declare_word_7(0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F, 0x3427), [0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F, 0x3427]),
	(Instruction.create_declare_word_8(0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F, 0x3427, 0xAA08), [0x77A9, 0xCE9D, 0x5505, 0x426C, 0x8632, 0xFE4F, 0x3427, 0xAA08]),
])
def test_dw(instr: Instruction, data: bytes) -> None:
	assert instr.code == Code.DECLAREWORD
	assert instr.declare_data_len == len(data)
	for i, d in enumerate(data):
		assert instr.get_declare_word_value(i) == d

@pytest.mark.parametrize("instr, data", [
	(Instruction.create_declare_dword_1(0x77A9_CE9D), [0x77A9_CE9D]),
	(Instruction.create_declare_dword_2(0x77A9_CE9D, 0x5505_426C), [0x77A9_CE9D, 0x5505_426C]),
	(Instruction.create_declare_dword_3(0x77A9_CE9D, 0x5505_426C, 0x8632_FE4F), [0x77A9_CE9D, 0x5505_426C, 0x8632_FE4F]),
	(Instruction.create_declare_dword_4(0x77A9_CE9D, 0x5505_426C, 0x8632_FE4F, 0x3427_AA08), [0x77A9_CE9D, 0x5505_426C, 0x8632_FE4F, 0x3427_AA08]),
])
def test_dd(instr: Instruction, data: bytes) -> None:
	assert instr.code == Code.DECLAREDWORD
	assert instr.declare_data_len == len(data)
	for i, d in enumerate(data):
		assert instr.get_declare_dword_value(i) == d

@pytest.mark.parametrize("instr, data", [
	(Instruction.create_declare_qword_1(0x77A9_CE9D_5505_426C), [0x77A9_CE9D_5505_426C]),
	(Instruction.create_declare_qword_2(0x77A9_CE9D_5505_426C, 0x8632_FE4F_3427_AA08), [0x77A9_CE9D_5505_426C, 0x8632_FE4F_3427_AA08]),
])
def test_dq(instr: Instruction, data: bytes) -> None:
	assert instr.code == Code.DECLAREQWORD
	assert instr.declare_data_len == len(data)
	for i, d in enumerate(data):
		assert instr.get_declare_qword_value(i) == d

@pytest.mark.parametrize("data", [
	b"",
	b"A" * 17,
	bytearray(b""),
	bytearray(b"A" * 17),
])
def test_invalid_db_slice_len(data: Union[bytes, bytearray]) -> None:
	with pytest.raises(ValueError):
		Instruction.create_declare_byte(data)

@pytest.mark.parametrize("data, is_valid", [
	(b"\x90", True),
	(bytearray(b"\x90"), True),
	(memoryview(b"\x90"), False),
	(memoryview(bytearray(b"\x90")), False),
	(None, False),
	(123, False),
	("Hello", False),
])
def test_invalid_db_slice_type(data: Any, is_valid: bool) -> None:
	if is_valid:
		db = Instruction.create_declare_byte(data)
		assert db.declare_data_len == len(data)
		for i, d in enumerate(data):
			assert db.get_declare_qword_value(i) == d
	else:
		with pytest.raises(TypeError):
			Instruction.create_declare_byte(data)

@pytest.mark.parametrize("create", [
	lambda: Instruction.create(12345), # type: ignore
	lambda: Instruction.create_reg_i64(12345, Register.RCX, -1), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.RCX, -1), # type: ignore
	lambda: Instruction.create_reg_u64(12345, Register.RCX, 0x31DE_BC9A_7856_3412), # type: ignore
	lambda: Instruction.create_reg_u32(12345, Register.RCX, 0xFFFF_FFFF), # type: ignore
	lambda: Instruction.create_reg(12345, Register.RCX), # type: ignore
	lambda: Instruction.create_mem(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_u32(12345, 0x5A), # type: ignore
	lambda: Instruction.create_i32(12345, 0xA55A), # type: ignore
	lambda: Instruction.create_i32(12345, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_i32(12345, 0x5A), # type: ignore
	lambda: Instruction.create_i32(12345, 0x5A), # type: ignore
	lambda: Instruction.create_i32(12345, 0x5A), # type: ignore
	lambda: Instruction.create_i32(12345, -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_branch(12345, 0x4D), # type: ignore
	lambda: Instruction.create_branch(12345, 0x8000_004C), # type: ignore
	lambda: Instruction.create_branch(12345, 0x8000_0000_0000_004C), # type: ignore
	lambda: Instruction.create_far_branch(12345, 0x7856, 0x3412), # type: ignore
	lambda: Instruction.create_far_branch(12345, 0xBC9A, 0x7856_3412), # type: ignore
	lambda: Instruction.create_reg_reg(12345, Register.CL, Register.DL), # type: ignore
	lambda: Instruction.create_reg_mem(12345, Register.CL, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.CL, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.CX, 0xA55A), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.ECX, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_u64(12345, Register.RCX, 0x7856_5AA5_3726_1504), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.CX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.ECX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.RCX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(12345, Register.RCX, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_mem_reg(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DL), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_mem_u32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA55A), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_mem_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A), # type: ignore
	lambda: Instruction.create_i32_reg(12345, 0x5A, Register.AL), # type: ignore
	lambda: Instruction.create_u32_reg(12345, 0x5A, Register.AL), # type: ignore
	lambda: Instruction.create_i32_i32(12345, 0xA55A, 0xA6), # type: ignore
	lambda: Instruction.create_u32_u32(12345, 0xA55A, 0xA6), # type: ignore
	lambda: Instruction.create_reg_reg_u32(12345, Register.CX, Register.DX, 0x5AA5), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.ECX, Register.EDX, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.CX, Register.DX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.ECX, Register.EDX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.RCX, Register.RDX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.RCX, Register.RDX, -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_reg_mem_u32(12345, Register.CX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA55A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.ECX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.CX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.ECX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.RCX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.RCX, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_reg_i32_i32(12345, Register.XMM1, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_u32_u32(12345, Register.XMM1, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_mem_reg_i32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DX, 0x5A), # type: ignore
	lambda: Instruction.create_mem_reg_u32(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.DX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32_i32(12345, Register.XMM1, Register.XMM2, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_reg_u32_u32(12345, Register.XMM1, Register.XMM2, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_branch(12345, 0xAA55), # type: ignore
	lambda: Instruction.create_branch(12345, 0xAA55_3412), # type: ignore
	lambda: Instruction.create_reg_reg_reg(12345, Register.XMM1, Register.XMM2, Register.XMM3), # type: ignore
	lambda: Instruction.create_reg_reg_mem(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_mem_reg(12345, Register.XMM1, MemoryOperand(Register.RBP, Register.XMM6, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM3), # type: ignore
	lambda: Instruction.create_mem_reg_reg(12345, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM2, Register.XMM3), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg(12345, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem(12345, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_i32(12345, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_u32(12345, Register.XMM1, Register.XMM2, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_i32(12345, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_u32(12345, Register.XMM1, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_i32(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_u32(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_i32(12345, Register.XMM1, Register.XMM2, 0xA5), # type: ignore
	lambda: Instruction.create_reg_mem_i32(12345, Register.XMM1, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_i32(12345, Register.XMM1, Register.XMM2, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_u32(12345, Register.XMM1, Register.XMM2, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_i32(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_u32(12345, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
])
def test_invalid_code_arg(create: Callable[[], Instruction]) -> None:
	with pytest.raises(ValueError):
		create()

@pytest.mark.parametrize("create", [
	lambda: Instruction.create_xbegin(1234, 0x8000_0000_3412_A550),
	lambda: Instruction.create_outsb(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_outsw(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_outsd(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_scasb(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_scasw(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_scasd(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_scasq(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_lodsb(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_lodsw(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_lodsd(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_lodsq(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_insb(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_insw(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_insd(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_stosb(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_stosw(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_stosd(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_stosq(1234, RepPrefixKind.NONE),
	lambda: Instruction.create_cmpsb(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_cmpsw(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_cmpsd(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_cmpsq(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_movsb(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_movsw(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_movsd(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_movsq(1234, Register.FS, RepPrefixKind.NONE),
	lambda: Instruction.create_maskmovq(1234, Register.MM2, Register.MM3, Register.FS),
	lambda: Instruction.create_maskmovdqu(1234, Register.XMM2, Register.XMM3, Register.FS),
	lambda: Instruction.create_outsb(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_outsw(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_outsd(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_scasb(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_scasw(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_scasd(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_scasq(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_lodsb(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_lodsw(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_lodsd(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_lodsq(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_insb(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_insw(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_insd(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_stosb(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_stosw(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_stosd(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_stosq(1234, RepPrefixKind.REPE),
	lambda: Instruction.create_cmpsb(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_cmpsw(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_cmpsd(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_cmpsq(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_movsb(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_movsw(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_movsd(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_movsq(1234, Register.FS, RepPrefixKind.REPE),
	lambda: Instruction.create_outsb(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_outsw(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_outsd(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_scasb(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_scasw(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_scasd(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_scasq(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_lodsb(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_lodsw(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_lodsd(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_lodsq(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_insb(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_insw(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_insd(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_stosb(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_stosw(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_stosd(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_stosq(1234, RepPrefixKind.REPNE),
	lambda: Instruction.create_cmpsb(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_cmpsw(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_cmpsd(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_cmpsq(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_movsb(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_movsw(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_movsd(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_movsq(1234, Register.FS, RepPrefixKind.REPNE),
	lambda: Instruction.create_rep_outsb(1234),
	lambda: Instruction.create_rep_outsw(1234),
	lambda: Instruction.create_rep_outsd(1234),
	lambda: Instruction.create_repe_scasb(1234),
	lambda: Instruction.create_repe_scasw(1234),
	lambda: Instruction.create_repe_scasd(1234),
	lambda: Instruction.create_repe_scasq(1234),
	lambda: Instruction.create_repne_scasb(1234),
	lambda: Instruction.create_repne_scasw(1234),
	lambda: Instruction.create_repne_scasd(1234),
	lambda: Instruction.create_repne_scasq(1234),
	lambda: Instruction.create_rep_lodsb(1234),
	lambda: Instruction.create_rep_lodsw(1234),
	lambda: Instruction.create_rep_lodsd(1234),
	lambda: Instruction.create_rep_lodsq(1234),
	lambda: Instruction.create_rep_insb(1234),
	lambda: Instruction.create_rep_insw(1234),
	lambda: Instruction.create_rep_insd(1234),
	lambda: Instruction.create_rep_stosb(1234),
	lambda: Instruction.create_rep_stosw(1234),
	lambda: Instruction.create_rep_stosd(1234),
	lambda: Instruction.create_rep_stosq(1234),
	lambda: Instruction.create_repe_cmpsb(1234),
	lambda: Instruction.create_repe_cmpsw(1234),
	lambda: Instruction.create_repe_cmpsd(1234),
	lambda: Instruction.create_repe_cmpsq(1234),
	lambda: Instruction.create_repne_cmpsb(1234),
	lambda: Instruction.create_repne_cmpsw(1234),
	lambda: Instruction.create_repne_cmpsd(1234),
	lambda: Instruction.create_repne_cmpsq(1234),
	lambda: Instruction.create_rep_movsb(1234),
	lambda: Instruction.create_rep_movsw(1234),
	lambda: Instruction.create_rep_movsd(1234),
	lambda: Instruction.create_rep_movsq(1234),
	lambda: Instruction.create_vmaskmovdqu(1234, Register.XMM2, Register.XMM3, Register.FS),
])
def test_invalid_bitness_arg(create: Callable[[], Instruction]) -> None:
	with pytest.raises(ValueError):
		create()

@pytest.mark.parametrize("create", [
	lambda: Instruction.create_cmpsb(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_cmpsd(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_cmpsq(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_cmpsw(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_insb(64, 123), # type: ignore
	lambda: Instruction.create_insd(64, 123), # type: ignore
	lambda: Instruction.create_insw(64, 123), # type: ignore
	lambda: Instruction.create_lodsb(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_lodsd(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_lodsq(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_lodsw(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_movsb(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_movsd(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_movsq(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_movsw(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_outsb(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_outsd(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_outsw(64, Register.FS, 123), # type: ignore
	lambda: Instruction.create_scasb(64, 123), # type: ignore
	lambda: Instruction.create_scasd(64, 123), # type: ignore
	lambda: Instruction.create_scasq(64, 123), # type: ignore
	lambda: Instruction.create_scasw(64, 123), # type: ignore
	lambda: Instruction.create_stosb(64, 123), # type: ignore
	lambda: Instruction.create_stosd(64, 123), # type: ignore
	lambda: Instruction.create_stosq(64, 123), # type: ignore
	lambda: Instruction.create_stosw(64, 123), # type: ignore
])
def test_invalid_rep_enum_arg(create: Callable[[], Instruction]) -> None:
	with pytest.raises(ValueError):
		create()

@pytest.mark.parametrize("create", [
	lambda: Instruction.create_reg_i64(Code.MOV_R64_IMM64, 1234, -1), # type: ignore
	lambda: Instruction.create_reg_i32(Code.MOV_R64_IMM64, 1234, -1), # type: ignore
	lambda: Instruction.create_reg_u64(Code.MOV_R64_IMM64, 1234, 0x31DE_BC9A_7856_3412), # type: ignore
	lambda: Instruction.create_reg_u32(Code.MOV_R64_IMM64, 1234, 0xFFFF_FFFF), # type: ignore
	lambda: Instruction.create_reg(Code.POP_RM64, 1234), # type: ignore
	lambda: Instruction.create_reg_reg(Code.ADD_RM8_R8, 1234, Register.DL), # type: ignore
	lambda: Instruction.create_reg_reg(Code.ADD_RM8_R8, Register.CL, 1234), # type: ignore
	lambda: Instruction.create_reg_mem(Code.ADD_R8_RM8, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM8_IMM8, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM16_IMM16, 1234, 0xA55A), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM32_IMM32, 1234, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_u64(Code.MOV_R64_IMM64, 1234, 0x7856_5AA5_3726_1504), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM16_IMM8, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM32_IMM8, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM64_IMM8, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_i32(Code.ADD_RM64_IMM32, 1234, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_mem_reg(Code.ADD_RM8_R8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234), # type: ignore
	lambda: Instruction.create_i32_reg(Code.OUT_IMM8_AL, 0x5A, 1234), # type: ignore
	lambda: Instruction.create_u32_reg(Code.OUT_IMM8_AL, 0x5A, 1234), # type: ignore
	lambda: Instruction.create_reg_reg_u32(Code.IMUL_R16_RM16_IMM16, 1234, Register.DX, 0x5AA5), # type: ignore
	lambda: Instruction.create_reg_reg_u32(Code.IMUL_R16_RM16_IMM16, Register.CX, 1234, 0x5AA5), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM32, 1234, Register.EDX, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM32, Register.ECX, 1234, 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R16_RM16_IMM8, 1234, Register.DX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R16_RM16_IMM8, Register.CX, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM8, 1234, Register.EDX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R32_RM32_IMM8, Register.ECX, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM8, 1234, Register.RDX, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM8, Register.RCX, 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM32, 1234, Register.RDX, -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.IMUL_R64_RM64_IMM32, Register.RCX, 1234, -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_reg_mem_u32(Code.IMUL_R16_RM16_IMM16, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA55A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.IMUL_R32_RM32_IMM32, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x3412_A55A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.IMUL_R16_RM16_IMM8, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.IMUL_R32_RM32_IMM8, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.IMUL_R64_RM64_IMM8, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x5A), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.IMUL_R64_RM64_IMM32, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), -0x5BED_5AA6), # type: ignore
	lambda: Instruction.create_reg_i32_i32(Code.EXTRQ_XMM_IMM8_IMM8, 1234, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_u32_u32(Code.EXTRQ_XMM_IMM8_IMM8, 1234, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_mem_reg_i32(Code.SHLD_RM16_R16_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234, 0x5A), # type: ignore
	lambda: Instruction.create_mem_reg_u32(Code.SHLD_RM16_R16_IMM8, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234, 0x5A), # type: ignore
	lambda: Instruction.create_reg_reg_i32_i32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, 1234, Register.XMM2, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_reg_i32_i32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, Register.XMM1, 1234, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_reg_u32_u32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, 1234, Register.XMM2, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_reg_reg_u32_u32(Code.INSERTQ_XMM_XMM_IMM8_IMM8, Register.XMM1, 1234, 0xA5, 0xFD), # type: ignore
	lambda: Instruction.create_outsb(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_outsw(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_outsd(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_lodsb(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_lodsw(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_lodsd(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_lodsq(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_cmpsb(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_cmpsw(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_cmpsd(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_cmpsq(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_movsb(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_movsw(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_movsd(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_movsq(64, 1234, RepPrefixKind.NONE), # type: ignore
	lambda: Instruction.create_maskmovq(64, 1234, Register.MM3, Register.FS), # type: ignore
	lambda: Instruction.create_maskmovq(64, Register.MM2, 1234, Register.FS), # type: ignore
	lambda: Instruction.create_maskmovq(64, Register.MM2, Register.MM3, 1234), # type: ignore
	lambda: Instruction.create_maskmovdqu(64, 1234, Register.XMM3, Register.FS), # type: ignore
	lambda: Instruction.create_maskmovdqu(64, Register.XMM2, 1234, Register.FS), # type: ignore
	lambda: Instruction.create_maskmovdqu(64, Register.XMM2, Register.XMM3, 1234), # type: ignore
	lambda: Instruction.create_outsb(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_outsw(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_outsd(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_lodsb(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_lodsw(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_lodsd(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_lodsq(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_cmpsb(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_cmpsw(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_cmpsd(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_cmpsq(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_movsb(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_movsw(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_movsd(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_movsq(64, 1234, RepPrefixKind.REPE), # type: ignore
	lambda: Instruction.create_outsb(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_outsw(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_outsd(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_lodsb(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_lodsw(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_lodsd(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_lodsq(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_cmpsb(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_cmpsw(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_cmpsd(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_cmpsq(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_movsb(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_movsw(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_movsd(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_movsq(64, 1234, RepPrefixKind.REPNE), # type: ignore
	lambda: Instruction.create_reg_reg_reg(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, 1234, Register.XMM2, Register.XMM3), # type: ignore
	lambda: Instruction.create_reg_reg_reg(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, Register.XMM1, 1234, Register.XMM3), # type: ignore
	lambda: Instruction.create_reg_reg_reg(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, Register.XMM1, Register.XMM2, 1234), # type: ignore
	lambda: Instruction.create_reg_reg_mem(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_reg_mem(Code.VEX_VUNPCKLPS_XMM_XMM_XMMM128, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_mem_reg(Code.VEX_VPGATHERDD_XMM_VM32X_XMM, 1234, MemoryOperand(Register.RBP, Register.XMM6, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM3), # type: ignore
	lambda: Instruction.create_reg_mem_reg(Code.VEX_VPGATHERDD_XMM_VM32X_XMM, Register.XMM1, MemoryOperand(Register.RBP, Register.XMM6, 2, -0x5432_10FF, 8, False, Register.FS), 1234), # type: ignore
	lambda: Instruction.create_mem_reg_reg(Code.VEX_VMASKMOVPS_M128_XMM_XMM, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234, Register.XMM3), # type: ignore
	lambda: Instruction.create_mem_reg_reg(Code.VEX_VMASKMOVPS_M128_XMM_XMM, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM2, 1234), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, 1234, Register.XMM2, Register.XMM3, Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, 1234, Register.XMM3, Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, Register.XMM2, 1234, Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, Register.XMM2, Register.XMM3, 1234), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem(Code.VEX_VFMADDSUBPS_XMM_XMM_XMM_XMMM128, 1234, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem(Code.VEX_VFMADDSUBPS_XMM_XMM_XMM_XMMM128, Register.XMM1, 1234, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem(Code.VEX_VFMADDSUBPS_XMM_XMM_XMM_XMMM128, Register.XMM1, Register.XMM2, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS)), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg(Code.VEX_VBLENDVPS_XMM_XMM_XMMM128_XMM, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, 1234, Register.XMM2, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, 1234, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, 1234, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, 1234, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, 1234, Register.XMM2, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, 1234, Register.XMM3, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, 1234, Register.XMM4, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, Register.XMM3, 1234, 0x0), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, 1234, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, 1234, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, Register.XMM2, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, 1234, Register.XMM2, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, 1234, Register.XMM3, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_reg_mem_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMM_XMMM128_IMM4, Register.XMM1, Register.XMM2, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_i32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), Register.XMM4, 0x1), # type: ignore
	lambda: Instruction.create_reg_reg_mem_reg_u32(Code.VEX_VPERMIL2PS_XMM_XMM_XMMM128_XMM_IMM4, Register.XMM1, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 1234, 0x1), # type: ignore
	lambda: Instruction.create_vmaskmovdqu(64, 1234, Register.XMM3, Register.FS), # type: ignore
	lambda: Instruction.create_vmaskmovdqu(64, Register.XMM2, 1234, Register.FS), # type: ignore
	lambda: Instruction.create_vmaskmovdqu(64, Register.XMM2, Register.XMM3, 1234), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.EVEX_VPSRLQ_XMM_K1Z_XMMM128B64_IMM8, 1234, Register.XMM2, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_i32(Code.EVEX_VPSRLQ_XMM_K1Z_XMMM128B64_IMM8, Register.XMM1, 1234, 0xA5), # type: ignore
	lambda: Instruction.create_reg_mem_i32(Code.EVEX_VPSRLQ_XMM_K1Z_XMMM128B64_IMM8, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, 1234, Register.XMM2, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, 1234, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, 1234, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, 1234, Register.XMM2, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, 1234, Register.EBX, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_reg_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, Register.XMM2, 1234, 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_i32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, 1234, Register.XMM2, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
	lambda: Instruction.create_reg_reg_mem_u32(Code.EVEX_VPINSRW_XMM_XMM_R32M16_IMM8, Register.XMM1, 1234, MemoryOperand(Register.RBP, Register.RSI, 2, -0x5432_10FF, 8, False, Register.FS), 0xA5), # type: ignore
])
def test_invalid_register_enum_arg(create: Callable[[], Instruction]) -> None:
	with pytest.raises(ValueError):
		create()
