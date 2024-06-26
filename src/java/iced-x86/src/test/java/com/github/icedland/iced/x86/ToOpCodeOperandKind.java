// SPDX-License-Identifier: MIT
// Copyright (C) 2018-present iced project and contributors

// ⚠️This file was generated by GENERATOR!🦹‍♂️

package com.github.icedland.iced.x86;

import java.util.HashMap;

import com.github.icedland.iced.x86.info.OpCodeOperandKind;

public final class ToOpCodeOperandKind {
	public static Integer tryGet(String key) {
		return map.get(key);
	}

	public static int get(String key) {
		Integer value = tryGet(key);
		if (value == null)
			throw new UnsupportedOperationException(String.format("Couldn't find enum variant OpCodeOperandKind.%s", key));
		return value.intValue();
	}

	public static String[] names() {
		return map.entrySet().stream().sorted((a, b) -> Integer.compareUnsigned(a.getValue(), b.getValue())).map(a -> a.getKey()).toArray(String[]::new);
	}

	public static Iterable<Integer> values() {
		return map.values();
	}

	public static int size() {
		return map.size();
	}

	public static HashMap<String, Integer> copy() {
		return new HashMap<String, Integer>(map);
	}

	private static final HashMap<String, Integer> map = getMap();

	private static HashMap<String, Integer> getMap() {
		HashMap<String, Integer> map = new HashMap<String, Integer>(109);
		initMap0(map);
		return map;
	}

	private static void initMap0(HashMap<String, Integer> map) {
		map.put("None", OpCodeOperandKind.NONE);
		map.put("farbr2_2", OpCodeOperandKind.FARBR2_2);
		map.put("farbr4_2", OpCodeOperandKind.FARBR4_2);
		map.put("mem_offs", OpCodeOperandKind.MEM_OFFS);
		map.put("mem", OpCodeOperandKind.MEM);
		map.put("mem_mpx", OpCodeOperandKind.MEM_MPX);
		map.put("mem_mib", OpCodeOperandKind.MEM_MIB);
		map.put("mem_vsib32x", OpCodeOperandKind.MEM_VSIB32X);
		map.put("mem_vsib64x", OpCodeOperandKind.MEM_VSIB64X);
		map.put("mem_vsib32y", OpCodeOperandKind.MEM_VSIB32Y);
		map.put("mem_vsib64y", OpCodeOperandKind.MEM_VSIB64Y);
		map.put("mem_vsib32z", OpCodeOperandKind.MEM_VSIB32Z);
		map.put("mem_vsib64z", OpCodeOperandKind.MEM_VSIB64Z);
		map.put("r8_or_mem", OpCodeOperandKind.R8_OR_MEM);
		map.put("r16_or_mem", OpCodeOperandKind.R16_OR_MEM);
		map.put("r32_or_mem", OpCodeOperandKind.R32_OR_MEM);
		map.put("r32_or_mem_mpx", OpCodeOperandKind.R32_OR_MEM_MPX);
		map.put("r64_or_mem", OpCodeOperandKind.R64_OR_MEM);
		map.put("r64_or_mem_mpx", OpCodeOperandKind.R64_OR_MEM_MPX);
		map.put("mm_or_mem", OpCodeOperandKind.MM_OR_MEM);
		map.put("xmm_or_mem", OpCodeOperandKind.XMM_OR_MEM);
		map.put("ymm_or_mem", OpCodeOperandKind.YMM_OR_MEM);
		map.put("zmm_or_mem", OpCodeOperandKind.ZMM_OR_MEM);
		map.put("bnd_or_mem_mpx", OpCodeOperandKind.BND_OR_MEM_MPX);
		map.put("k_or_mem", OpCodeOperandKind.K_OR_MEM);
		map.put("r8_reg", OpCodeOperandKind.R8_REG);
		map.put("r8_opcode", OpCodeOperandKind.R8_OPCODE);
		map.put("r16_reg", OpCodeOperandKind.R16_REG);
		map.put("r16_reg_mem", OpCodeOperandKind.R16_REG_MEM);
		map.put("r16_rm", OpCodeOperandKind.R16_RM);
		map.put("r16_opcode", OpCodeOperandKind.R16_OPCODE);
		map.put("r32_reg", OpCodeOperandKind.R32_REG);
		map.put("r32_reg_mem", OpCodeOperandKind.R32_REG_MEM);
		map.put("r32_rm", OpCodeOperandKind.R32_RM);
		map.put("r32_opcode", OpCodeOperandKind.R32_OPCODE);
		map.put("r32_vvvv", OpCodeOperandKind.R32_VVVV);
		map.put("r64_reg", OpCodeOperandKind.R64_REG);
		map.put("r64_reg_mem", OpCodeOperandKind.R64_REG_MEM);
		map.put("r64_rm", OpCodeOperandKind.R64_RM);
		map.put("r64_opcode", OpCodeOperandKind.R64_OPCODE);
		map.put("r64_vvvv", OpCodeOperandKind.R64_VVVV);
		map.put("seg_reg", OpCodeOperandKind.SEG_REG);
		map.put("k_reg", OpCodeOperandKind.K_REG);
		map.put("kp1_reg", OpCodeOperandKind.KP1_REG);
		map.put("k_rm", OpCodeOperandKind.K_RM);
		map.put("k_vvvv", OpCodeOperandKind.K_VVVV);
		map.put("mm_reg", OpCodeOperandKind.MM_REG);
		map.put("mm_rm", OpCodeOperandKind.MM_RM);
		map.put("xmm_reg", OpCodeOperandKind.XMM_REG);
		map.put("xmm_rm", OpCodeOperandKind.XMM_RM);
		map.put("xmm_vvvv", OpCodeOperandKind.XMM_VVVV);
		map.put("xmmp3_vvvv", OpCodeOperandKind.XMMP3_VVVV);
		map.put("xmm_is4", OpCodeOperandKind.XMM_IS4);
		map.put("xmm_is5", OpCodeOperandKind.XMM_IS5);
		map.put("ymm_reg", OpCodeOperandKind.YMM_REG);
		map.put("ymm_rm", OpCodeOperandKind.YMM_RM);
		map.put("ymm_vvvv", OpCodeOperandKind.YMM_VVVV);
		map.put("ymm_is4", OpCodeOperandKind.YMM_IS4);
		map.put("ymm_is5", OpCodeOperandKind.YMM_IS5);
		map.put("zmm_reg", OpCodeOperandKind.ZMM_REG);
		map.put("zmm_rm", OpCodeOperandKind.ZMM_RM);
		map.put("zmm_vvvv", OpCodeOperandKind.ZMM_VVVV);
		map.put("zmmp3_vvvv", OpCodeOperandKind.ZMMP3_VVVV);
		map.put("cr_reg", OpCodeOperandKind.CR_REG);
		map.put("dr_reg", OpCodeOperandKind.DR_REG);
		map.put("tr_reg", OpCodeOperandKind.TR_REG);
		map.put("bnd_reg", OpCodeOperandKind.BND_REG);
		map.put("es", OpCodeOperandKind.ES);
		map.put("cs", OpCodeOperandKind.CS);
		map.put("ss", OpCodeOperandKind.SS);
		map.put("ds", OpCodeOperandKind.DS);
		map.put("fs", OpCodeOperandKind.FS);
		map.put("gs", OpCodeOperandKind.GS);
		map.put("al", OpCodeOperandKind.AL);
		map.put("cl", OpCodeOperandKind.CL);
		map.put("ax", OpCodeOperandKind.AX);
		map.put("dx", OpCodeOperandKind.DX);
		map.put("eax", OpCodeOperandKind.EAX);
		map.put("rax", OpCodeOperandKind.RAX);
		map.put("st0", OpCodeOperandKind.ST0);
		map.put("sti_opcode", OpCodeOperandKind.STI_OPCODE);
		map.put("imm4_m2z", OpCodeOperandKind.IMM4_M2Z);
		map.put("imm8", OpCodeOperandKind.IMM8);
		map.put("imm8_const_1", OpCodeOperandKind.IMM8_CONST_1);
		map.put("imm8sex16", OpCodeOperandKind.IMM8SEX16);
		map.put("imm8sex32", OpCodeOperandKind.IMM8SEX32);
		map.put("imm8sex64", OpCodeOperandKind.IMM8SEX64);
		map.put("imm16", OpCodeOperandKind.IMM16);
		map.put("imm32", OpCodeOperandKind.IMM32);
		map.put("imm32sex64", OpCodeOperandKind.IMM32SEX64);
		map.put("imm64", OpCodeOperandKind.IMM64);
		map.put("seg_rSI", OpCodeOperandKind.SEG_RSI);
		map.put("es_rDI", OpCodeOperandKind.ES_RDI);
		map.put("seg_rDI", OpCodeOperandKind.SEG_RDI);
		map.put("seg_rBX_al", OpCodeOperandKind.SEG_RBX_AL);
		map.put("br16_1", OpCodeOperandKind.BR16_1);
		map.put("br32_1", OpCodeOperandKind.BR32_1);
		map.put("br64_1", OpCodeOperandKind.BR64_1);
		map.put("br16_2", OpCodeOperandKind.BR16_2);
		map.put("br32_4", OpCodeOperandKind.BR32_4);
		map.put("br64_4", OpCodeOperandKind.BR64_4);
		map.put("xbegin_2", OpCodeOperandKind.XBEGIN_2);
		map.put("xbegin_4", OpCodeOperandKind.XBEGIN_4);
		map.put("brdisp_2", OpCodeOperandKind.BRDISP_2);
		map.put("brdisp_4", OpCodeOperandKind.BRDISP_4);
		map.put("sibmem", OpCodeOperandKind.SIBMEM);
		map.put("tmm_reg", OpCodeOperandKind.TMM_REG);
		map.put("tmm_rm", OpCodeOperandKind.TMM_RM);
		map.put("tmm_vvvv", OpCodeOperandKind.TMM_VVVV);
	}
}
