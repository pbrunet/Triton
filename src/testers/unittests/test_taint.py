#!/usr/bin/env python2
# coding: utf-8
"""Test Taint."""

import unittest

from triton import ARCH, REG, Instruction, MemoryAccess, TritonContext


class TestTaint(unittest.TestCase):

    """Testing the taint engine."""

    def test_known_issues(self):
        """Check tainting result after processing."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86)

        Triton.taintRegister(REG.EAX)
        inst = Instruction()
        # lea eax,[esi+eax*1]
        inst.setOpcodes("\x8D\x04\x06")
        Triton.processing(inst)

        self.assertTrue(Triton.isRegisterTainted(REG.EAX))
        self.assertFalse(Triton.isRegisterTainted(REG.EBX))

    def test_taint_memory(self):
        """Check tainting memory."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isMemoryTainted(0x1000))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintMemory(0x1000)
        Triton.taintMemory(MemoryAccess(0x2000, 4))

        self.assertTrue(Triton.isMemoryTainted(0x1000))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 2)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2002, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2003, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2002, 2)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2003, 2)))

        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x1fff, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2004, 1)))
        self.assertFalse(Triton.isMemoryTainted(0x1001))
        self.assertFalse(Triton.isMemoryTainted(0x0fff))

        Triton.untaintMemory(0x1000)
        Triton.untaintMemory(MemoryAccess(0x2000, 4))

        self.assertFalse(Triton.isMemoryTainted(0x1000))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 2)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2002, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2003, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2002, 2)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2003, 2)))

    def test_taint_register(self):
        """Check over tainting register."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        Triton.untaintRegister(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.taintRegister(REG.AH)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertTrue(Triton.isRegisterTainted(REG.EAX))
        self.assertTrue(Triton.isRegisterTainted(REG.AX))

        Triton.untaintRegister(REG.AH)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        self.assertFalse(Triton.isRegisterTainted(REG.EAX))
        self.assertFalse(Triton.isRegisterTainted(REG.AX))

    def test_taint_assignement_memory_immediate(self):
        """Check tainting assignment memory <- immediate."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(0x1000)
        self.assertTrue(Triton.isMemoryTainted(0x1000))

        Triton.taintAssignmentMemoryImmediate(MemoryAccess(0x1000, 1))
        self.assertFalse(Triton.isMemoryTainted(0x1000))

        Triton.taintMemory(0x1000)
        self.assertTrue(Triton.isMemoryTainted(0x1000))

        Triton.taintAssignmentMemoryImmediate(MemoryAccess(0x0fff, 2))
        self.assertFalse(Triton.isMemoryTainted(0x1000))

        Triton.taintMemory(0x1000)
        self.assertTrue(Triton.isMemoryTainted(0x1000))

        Triton.taintAssignmentMemoryImmediate(MemoryAccess(0x0ffe, 2))
        self.assertTrue(Triton.isMemoryTainted(0x1000))

        Triton.taintMemory(MemoryAccess(0x1000, 4))
        self.assertTrue(Triton.isMemoryTainted(0x1000))
        self.assertTrue(Triton.isMemoryTainted(0x1001))
        self.assertTrue(Triton.isMemoryTainted(0x1002))
        self.assertTrue(Triton.isMemoryTainted(0x1003))
        self.assertFalse(Triton.isMemoryTainted(0x1004))

        Triton.taintAssignmentMemoryImmediate(MemoryAccess(0x1001, 1))
        self.assertTrue(Triton.isMemoryTainted(0x1000))
        self.assertFalse(Triton.isMemoryTainted(0x1001))
        self.assertTrue(Triton.isMemoryTainted(0x1002))
        self.assertTrue(Triton.isMemoryTainted(0x1003))

        Triton.taintAssignmentMemoryImmediate(MemoryAccess(0x1000, 4))
        self.assertFalse(Triton.isMemoryTainted(0x1000))
        self.assertFalse(Triton.isMemoryTainted(0x1001))
        self.assertFalse(Triton.isMemoryTainted(0x1002))
        self.assertFalse(Triton.isMemoryTainted(0x1003))

    def test_taint_assignement_memory_memory(self):
        """Check tainting assignment memory <- memory."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(MemoryAccess(0x2000, 1))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))

        Triton.taintAssignmentMemoryMemory(MemoryAccess(0x1000, 1), MemoryAccess(0x2000, 1))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x1000, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))

        Triton.taintAssignmentMemoryMemory(MemoryAccess(0x1000, 1), MemoryAccess(0x3000, 1))
        Triton.taintAssignmentMemoryMemory(MemoryAccess(0x2000, 1), MemoryAccess(0x3000, 1))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x1000, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))

        Triton.taintMemory(MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintAssignmentMemoryMemory(MemoryAccess(0x2001, 2), MemoryAccess(0x3000, 1))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))

    def test_taint_assignement_memory_register(self):
        """Check tainting assignment memory <- register."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(MemoryAccess(0x2000, 8))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 8)))

        Triton.taintAssignmentMemoryRegister(MemoryAccess(0x2002, 2), REG.AX)
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2002, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2003, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2004, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2005, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2006, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2007, 1)))

        Triton.taintMemory(MemoryAccess(0x2000, 8))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 8)))

        Triton.taintAssignmentMemoryRegister(MemoryAccess(0x1fff, 8), REG.RAX)
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x1fff, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2001, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2002, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2003, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2004, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2005, 1)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2006, 1)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2007, 1)))

    def test_taint_assignement_register_immediate(self):
        """Check tainting assignment register <- immediate."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintAssignmentRegisterImmediate(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

    def test_taint_assignement_register_memory(self):
        """Check tainting assignment register <- memory."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintAssignmentRegisterMemory(REG.RAX, MemoryAccess(0x2000, 8))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.taintMemory(MemoryAccess(0x2000, 8))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 8)))

        Triton.taintAssignmentRegisterMemory(REG.RAX, MemoryAccess(0x2000, 8))
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintAssignmentRegisterMemory(REG.RAX, MemoryAccess(0x3000, 8))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

    def test_taint_assignement_register_register(self):
        """Check tainting assignment register <- register."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintAssignmentRegisterRegister(REG.RAX, REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.untaintRegister(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintAssignmentRegisterRegister(REG.RAX, REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        self.assertFalse(Triton.isRegisterTainted(REG.RBX))
        Triton.taintRegister(REG.RBX)
        self.assertTrue(Triton.isRegisterTainted(REG.RBX))

        Triton.taintAssignmentRegisterRegister(REG.RAX, REG.RBX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

    def test_taint_union_memory_immediate(self):
        """Check tainting union memory U immediate."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintUnionMemoryImmediate(MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.untaintMemory(MemoryAccess(0x2000, 4))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

    def test_taint_union_memory_memory(self):
        """Check tainting union memory U memory."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintUnionMemoryMemory(MemoryAccess(0x2000, 4), MemoryAccess(0x3000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x3000, 4)))

        Triton.untaintMemory(MemoryAccess(0x2000, 4))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintUnionMemoryMemory(MemoryAccess(0x2000, 4), MemoryAccess(0x3000, 4))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x3000, 4)))

        Triton.taintMemory(MemoryAccess(0x3000, 4))
        Triton.taintUnionMemoryMemory(MemoryAccess(0x2000, 4), MemoryAccess(0x3000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x3000, 4)))

    def test_taint_union_memory_register(self):
        """Check tainting union memory U register."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        Triton.taintMemory(MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.taintUnionMemoryRegister(MemoryAccess(0x2000, 4), REG.RAX)
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.untaintMemory(MemoryAccess(0x2000, 4))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.taintUnionMemoryRegister(MemoryAccess(0x2000, 4), REG.RAX)
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.taintRegister(REG.RAX)
        Triton.taintUnionMemoryRegister(MemoryAccess(0x2000, 4), REG.RAX)
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

    def test_taint_union_register_immediate(self):
        """Check tainting union register U immediate."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintUnionRegisterImmediate(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.untaintRegister(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintUnionRegisterImmediate(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

    def test_taint_union_register_memory(self):
        """Check tainting union register U memory."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintUnionRegisterMemory(REG.RAX, MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        Triton.untaintRegister(REG.RAX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))

        Triton.taintUnionRegisterMemory(REG.RAX, MemoryAccess(0x2000, 4))
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        self.assertFalse(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        # !T U T
        Triton.untaintRegister(REG.RAX)
        Triton.taintMemory(MemoryAccess(0x2000, 4))
        Triton.taintUnionRegisterMemory(REG.RAX, MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

        # T U T
        Triton.taintRegister(REG.RAX)
        Triton.taintMemory(MemoryAccess(0x2000, 4))
        Triton.taintUnionRegisterMemory(REG.RAX, MemoryAccess(0x2000, 4))
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertTrue(Triton.isMemoryTainted(MemoryAccess(0x2000, 4)))

    def test_taint_union_register_register(self):
        """Check tainting union register U register."""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        Triton.taintRegister(REG.RAX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))

        Triton.taintUnionRegisterRegister(REG.RAX, REG.RBX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertFalse(Triton.isRegisterTainted(REG.RBX))

        Triton.taintRegister(REG.RBX)
        Triton.taintUnionRegisterRegister(REG.RAX, REG.RBX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertTrue(Triton.isRegisterTainted(REG.RBX))

        Triton.untaintRegister(REG.RAX)
        Triton.taintRegister(REG.RBX)
        Triton.taintUnionRegisterRegister(REG.RAX, REG.RBX)
        self.assertTrue(Triton.isRegisterTainted(REG.RAX))
        self.assertTrue(Triton.isRegisterTainted(REG.RBX))

        Triton.untaintRegister(REG.RAX)
        Triton.untaintRegister(REG.RBX)
        Triton.taintUnionRegisterRegister(REG.RAX, REG.RBX)
        self.assertFalse(Triton.isRegisterTainted(REG.RAX))
        self.assertFalse(Triton.isRegisterTainted(REG.RBX))

    def test_taint_get_tainted_registers(self):
        """Get tainted registers"""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        r = Triton.getTaintedRegisters()
        self.assertTrue(len(r) == 0)

        Triton.taintRegister(REG.EAX)
        Triton.taintRegister(REG.AX)
        Triton.taintRegister(REG.RBX)
        Triton.taintRegister(REG.CL)
        Triton.taintRegister(REG.DI)

        r = Triton.getTaintedRegisters()
        self.assertTrue(REG.RAX in r)
        self.assertTrue(REG.RBX in r)
        self.assertTrue(REG.RCX in r)
        self.assertTrue(REG.RDI in r)

    def test_taint_get_tainted_memory(self):
        """Get tainted memory"""
        Triton = TritonContext()
        Triton.setArchitecture(ARCH.X86_64)

        m = Triton.getTaintedMemory()
        self.assertTrue(len(m) == 0)

        Triton.taintMemory(0x1000)
        Triton.taintMemory(0x2000)
        Triton.taintMemory(0x3000)
        Triton.taintMemory(MemoryAccess(0x4000, 4))

        m = Triton.getTaintedMemory()
        self.assertTrue(0x1000 in m)
        self.assertTrue(0x2000 in m)
        self.assertTrue(0x3000 in m)
        self.assertTrue(0x4000 in m)
        self.assertTrue(0x4001 in m)
        self.assertTrue(0x4002 in m)
        self.assertTrue(0x4003 in m)
        self.assertFalse(0x5000 in m)

