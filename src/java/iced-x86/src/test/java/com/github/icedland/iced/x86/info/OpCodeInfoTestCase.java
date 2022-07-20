// SPDX-License-Identifier: MIT
// Copyright (C) 2018-present iced project and contributors

package com.github.icedland.iced.x86.info;

import com.github.icedland.iced.x86.Code;
import com.github.icedland.iced.x86.EncodingKind;
import com.github.icedland.iced.x86.MemorySize;
import com.github.icedland.iced.x86.Mnemonic;
import com.github.icedland.iced.x86.TupleType;
import com.github.icedland.iced.x86.dec.DecoderOptions;

final class OpCodeInfoTestCase {
	public int lineNumber = -1;
	public int code = Code.INVALID;
	public int mnemonic = Mnemonic.INVALID;
	public String opCodeString = "";
	public String instructionString = "";
	public int encoding = EncodingKind.LEGACY;
	public boolean isInstruction;
	public boolean mode16;
	public boolean mode32;
	public boolean mode64;
	public boolean fwait;
	public int operandSize;
	public int addressSize;
	public int l;
	public int w;
	public boolean isLIG;
	public boolean isWIG;
	public boolean isWIG32;
	public int tupleType = TupleType.N1;
	public int memorySize = MemorySize.UNKNOWN;
	public int broadcastMemorySize = MemorySize.UNKNOWN;
	public int decoderOption = DecoderOptions.NONE;
	public boolean canBroadcast;
	public boolean canUseRoundingControl;
	public boolean canSuppressAllExceptions;
	public boolean canUseOpMaskRegister;
	public boolean requireOpMaskRegister;
	public boolean canUseZeroingMasking;
	public boolean canUseLockPrefix;
	public boolean canUseXacquirePrefix;
	public boolean canUseXreleasePrefix;
	public boolean canUseRepPrefix;
	public boolean canUseRepnePrefix;
	public boolean canUseBndPrefix;
	public boolean canUseHintTakenPrefix;
	public boolean canUseNotrackPrefix;
	public boolean ignoresRoundingControl;
	public boolean amdLockRegBit;
	public boolean defaultOpSize64;
	public boolean forceOpSize64;
	public boolean intelForceOpSize64;
	public boolean cpl0;
	public boolean cpl1;
	public boolean cpl2;
	public boolean cpl3;
	public boolean isInputOutput;
	public boolean isNop;
	public boolean isReservedNop;
	public boolean isSerializingIntel;
	public boolean isSerializingAmd;
	public boolean mayRequireCpl0;
	public boolean isCetTracked;
	public boolean isNonTemporal;
	public boolean isFpuNoWait;
	public boolean ignoresModBits;
	public boolean no66;
	public boolean nFx;
	public boolean requiresUniqueRegNums;
	public boolean requiresUniqueDestRegNum;
	public boolean isPrivileged;
	public boolean isSaveRestore;
	public boolean isStackInstruction;
	public boolean ignoresSegment;
	public boolean isOpMaskReadWrite;
	public boolean realMode;
	public boolean protectedMode;
	public boolean virtual8086Mode;
	public boolean compatibilityMode;
	public boolean longMode;
	public boolean useOutsideSmm;
	public boolean useInSmm;
	public boolean useOutsideEnclaveSgx;
	public boolean useInEnclaveSgx1;
	public boolean useInEnclaveSgx2;
	public boolean useOutsideVmxOp;
	public boolean useInVmxRootOp;
	public boolean useInVmxNonRootOp;
	public boolean useOutsideSeam;
	public boolean useInSeam;
	public boolean tdxNonRootGenUd;
	public boolean tdxNonRootGenVe;
	public boolean tdxNonRootMayGenEx;
	public boolean intelVmExit;
	public boolean intelMayVmExit;
	public boolean intelSmmVmExit;
	public boolean amdVmExit;
	public boolean amdMayVmExit;
	public boolean tsxAbort;
	public boolean tsxImplAbort;
	public boolean tsxMayAbort;
	public boolean intelDecoder16;
	public boolean intelDecoder32;
	public boolean intelDecoder64;
	public boolean amdDecoder16;
	public boolean amdDecoder32;
	public boolean amdDecoder64;
	public int table = OpCodeTableKind.NORMAL;
	public int mandatoryPrefix = MandatoryPrefix.NONE;
	public int opCode = 0;
	public int opCodeLength = 0;
	public boolean isGroup = false;
	public int groupIndex = -1;
	public boolean isRmGroup = false;
	public int rmGroupIndex = -1;
	public int opCount = 0;
	public int op0Kind = OpCodeOperandKind.NONE;
	public int op1Kind = OpCodeOperandKind.NONE;
	public int op2Kind = OpCodeOperandKind.NONE;
	public int op3Kind = OpCodeOperandKind.NONE;
	public int op4Kind = OpCodeOperandKind.NONE;
	public int mvexEHBit;
	public boolean mvexCanUseEvictionHint;
	public boolean mvexCanUseImmRoundingControl;
	public boolean mvexIgnoresOpMaskRegister;
	public boolean mvexNoSaeRc;
	public int mvexTupleTypeLutKind;
	public int mvexConversionFunc;
	public byte mvexValidConversionFuncsMask;
	public byte mvexValidSwizzleFuncsMask;
}