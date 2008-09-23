from Mipper.mipper import *
from Mipper.gnrl_ops import *
from Mipper.math_ops import *
from Mipper.bool_ops import *
from Mipper.pseudo_ops import *

def append_or_extend(lines, addend):
    if type(addend) is list:
       lines.extend(addend)
    else:
       lines.append(addend)


# Begin -- grammar generated by Yapps
import sys, re
import yapps.yappsrt as yappsrt

class MipsParserScanner(yappsrt.Scanner):
    patterns = [
        ('"sw"', re.compile('sw')),
        ('"lw"', re.compile('lw')),
        ('"mflo"', re.compile('mflo')),
        ('"mfhi"', re.compile('mfhi')),
        ('"jr"', re.compile('jr')),
        ('"jal"', re.compile('jal')),
        ('"j"', re.compile('j')),
        ('"sltiu"', re.compile('sltiu')),
        ('"sltu"', re.compile('sltu')),
        ('"slti"', re.compile('slti')),
        ('"slt"', re.compile('slt')),
        ('"bne"', re.compile('bne')),
        ('"beq"', re.compile('beq')),
        ('"ori"', re.compile('ori')),
        ('"andi"', re.compile('andi')),
        ('"or"', re.compile('or')),
        ('"and"', re.compile('and')),
        ('"mult"', re.compile('mult')),
        ('"divu"', re.compile('divu')),
        ('"div"', re.compile('div')),
        ('"subu"', re.compile('subu')),
        ('"addiu"', re.compile('addiu')),
        ('"addi"', re.compile('addi')),
        ('"addu"', re.compile('addu')),
        ('"sub"', re.compile('sub')),
        ('"add"', re.compile('add')),
        ('"bgtz"', re.compile('bgtz')),
        ('"bgtu"', re.compile('bgtu')),
        ('"ble"', re.compile('ble')),
        ('"bge"', re.compile('bge')),
        ('"blt"', re.compile('blt')),
        ('"bgt"', re.compile('bgt')),
        ('"move"', re.compile('move')),
        ('"li"', re.compile('li')),
        ('","', re.compile(',')),
        ('"la"', re.compile('la')),
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('".space"', re.compile('.space')),
        ('".asciiz"', re.compile('.asciiz')),
        ('".text\\n"', re.compile('.text\n')),
        ('".data\\n"', re.compile('.data\n')),
        ('"\\n"', re.compile('\n')),
        (' ', re.compile(' ')),
        ('END', re.compile('$')),
        ('NUM', re.compile('-?[0-9]+')),
        ('HEX', re.compile('0x[0-9]+')),
        ('REGISTER', re.compile('\\$(gp|sp|fp|ra|v[0-1]|a[0-3]|t[0-9]|s[0-7]|k[0-1]|zero|[0-9]+)')),
        ('LABEL', re.compile('\\w+:')),
        ('LABEL_REF', re.compile('\\w+')),
        ('SYSTEM_CALL', re.compile('syscall')),
        ('STRING', re.compile('"[^"]*"')),
        ('COMMENT', re.compile('#[^\n]*\n')),
        ('BREAK', re.compile('BREAK')),
    ]
    def __init__(self, str):
        yappsrt.Scanner.__init__(self,None,[' '],str)

class MipsParser(yappsrt.Parser):
    Context = yappsrt.Context
    def end_line(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'end_line', [])
        _token = self._peek('"\\n"', 'COMMENT')
        if _token == '"\\n"':
            self._scan('"\\n"')
        else: # == 'COMMENT'
            COMMENT = self._scan('COMMENT')

    def empty_line(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'empty_line', [])
        end_line = self.end_line(_context)

    def program(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'program', [])
        while self._peek('"\\n"', 'COMMENT', '".data\\n"', '".text\\n"', 'LABEL', 'SYSTEM_CALL', 'BREAK', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END') in ['"\\n"', 'COMMENT']:
            empty_line = self.empty_line(_context)
        if self._peek() not in ['"\\n"', 'COMMENT', '".data\\n"', '".text\\n"', 'LABEL', 'SYSTEM_CALL', 'BREAK', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END']:
            raise yappsrt.SyntaxError(charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['"\\n"', 'COMMENT', '".data\\n"', '".text\\n"', 'LABEL', 'SYSTEM_CALL', 'BREAK', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END']))
        _token = self._peek('".data\\n"', '".text\\n"')
        if _token == '".data\\n"':
            data = self.data(_context)
            ret = data
        else: # == '".text\\n"'
            text = self.text(_context)
            ret = text
        END = self._scan('END')
        return ret

    def data(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'data', [])
        self._scan('".data\\n"')
        allocations = []
        instructions = []
        while self._peek('"\\n"', 'COMMENT', '".text\\n"', 'LABEL', 'SYSTEM_CALL', 'BREAK', '".data\\n"', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END') in ['"\\n"', 'COMMENT', 'LABEL']:
            _token = self._peek('"\\n"', 'COMMENT', 'LABEL')
            if _token == 'LABEL':
                allocation = self.allocation(_context)
                allocations.append(allocation)
            else: # in ['"\\n"', 'COMMENT']
                empty_line = self.empty_line(_context)
        if self._peek() not in ['"\\n"', 'COMMENT', '".text\\n"', 'LABEL', 'SYSTEM_CALL', 'BREAK', '".data\\n"', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END']:
            raise yappsrt.SyntaxError(charpos=self._scanner.get_prev_char_pos(), context=_context, msg='Need one of ' + ', '.join(['"\\n"', 'COMMENT', 'LABEL', '".text\\n"', 'SYSTEM_CALL', 'BREAK', '".data\\n"', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', 'END']))
        if self._peek('".text\\n"', 'END') == '".text\\n"':
            text = self.text(_context)
            instructions = text[1]
        return allocations, instructions

    def text(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'text', [])
        self._scan('".text\\n"')
        instructions = []
        allocations = []
        while 1:
            _token = self._peek('LABEL', 'SYSTEM_CALL', 'BREAK', '"\\n"', 'COMMENT', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"')
            if _token not in ['LABEL', 'SYSTEM_CALL', 'BREAK', '"\\n"', 'COMMENT']:
                statement = self.statement(_context)
                append_or_extend(instructions, statement)
            elif _token == 'LABEL':
                LABEL = self._scan('LABEL')
                end_line = self.end_line(_context)
                instructions.append(LABEL.strip(':'))
            elif _token == 'SYSTEM_CALL':
                SYSTEM_CALL = self._scan('SYSTEM_CALL')
                end_line = self.end_line(_context)
                instructions.append(SYSCALL())
            elif _token == 'BREAK':
                BREAK = self._scan('BREAK')
                self._scan('"\\n"')
                instructions.append(BREAK)
            else: # in ['"\\n"', 'COMMENT']
                empty_line = self.empty_line(_context)
            if self._peek('LABEL', 'SYSTEM_CALL', 'BREAK', '"\\n"', 'COMMENT', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"', '".data\\n"', '".text\\n"', 'END') not in ['LABEL', 'SYSTEM_CALL', 'BREAK', '"\\n"', 'COMMENT', '"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"']: break
        if self._peek('".data\\n"', 'END') == '".data\\n"':
            data = self.data(_context)
            allocations = data[0]
        return allocations, instructions

    def allocation(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'allocation', [])
        LABEL = self._scan('LABEL')
        _token = self._peek('".asciiz"', '".space"')
        if _token == '".asciiz"':
            allocate_asciiz = self.allocate_asciiz(_context)
            f = allocate_asciiz
        else: # == '".space"'
            allocate_space = self.allocate_space(_context)
            f = allocate_space
        end_line = self.end_line(_context)
        return f(LABEL.strip(':'))

    def allocate_asciiz(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'allocate_asciiz', [])
        self._scan('".asciiz"')
        STRING = self._scan('STRING')
        str_val = STRING
        return lambda lbl : CREATE_STRING(lbl, str_val)

    def allocate_space(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'allocate_space', [])
        self._scan('".space"')
        NUM = self._scan('NUM')
        nsize = int(NUM)
        return lambda lbl : CREATE_SPACE(lbl, nsize)

    def immediate(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'immediate', [])
        _token = self._peek('NUM', 'HEX')
        if _token == 'NUM':
            NUM = self._scan('NUM')
            return int(NUM, 10)
        else: # == 'HEX'
            HEX = self._scan('HEX')
            return int(HEX, 16)

    def num_or_register(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'num_or_register', [])
        _token = self._peek('NUM', 'REGISTER')
        if _token == 'NUM':
            NUM = self._scan('NUM')
        else: # == 'REGISTER'
            REGISTER = self._scan('REGISTER')

    def indirect_address(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'indirect_address', [])
        offset = 0
        if self._peek('NUM', 'LABEL_REF', '"\\\\("') != '"\\\\("':
            _token = self._peek('NUM', 'LABEL_REF')
            if _token == 'NUM':
                NUM = self._scan('NUM')
                offset = NUM
            else: # == 'LABEL_REF'
                LABEL_REF = self._scan('LABEL_REF')
                offset = LABEL_REF
        self._scan('"\\\\("')
        REGISTER = self._scan('REGISTER')
        reg = REGISTER
        self._scan('"\\\\)"')
        return (offset, reg)

    def statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'statement', [])
        _token = self._peek('"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"', '"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"', '"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"', '"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"')
        if _token in ['"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"']:
            gnrl_op = self.gnrl_op(_context)
            ret = gnrl_op
        elif _token in ['"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"']:
            math_op = self.math_op(_context)
            ret = math_op
        elif _token not in ['"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"']:
            bool_op = self.bool_op(_context)
            ret = bool_op
        else:
            pseudo_op = self.pseudo_op(_context)
            ret = pseudo_op
        end_line = self.end_line(_context)
        return ret

    def gnrl_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'gnrl_op', [])
        _token = self._peek('"j"', '"jal"', '"jr"', '"mfhi"', '"mflo"', '"lw"', '"sw"')
        if _token == '"j"':
            jump_op = self.jump_op(_context)
            ret = jump_op
        elif _token == '"jal"':
            jal_op = self.jal_op(_context)
            ret = jal_op
        elif _token == '"jr"':
            jr_op = self.jr_op(_context)
            ret = jr_op
        elif _token == '"mfhi"':
            mfhi_op = self.mfhi_op(_context)
            ret = mfhi_op
        elif _token == '"mflo"':
            mflo_op = self.mflo_op(_context)
            ret = mflo_op
        elif _token == '"lw"':
            lw_op = self.lw_op(_context)
            ret = lw_op
        else: # == '"sw"'
            sw_op = self.sw_op(_context)
            ret = sw_op
        return ret

    def math_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'math_op', [])
        _token = self._peek('"add"', '"sub"', '"addu"', '"addi"', '"addiu"', '"subu"', '"div"', '"divu"', '"mult"')
        if _token == '"add"':
            add_op = self.add_op(_context)
            ret = add_op
        elif _token == '"sub"':
            sub_op = self.sub_op(_context)
            ret = sub_op
        elif _token == '"addu"':
            addu_op = self.addu_op(_context)
            ret = addu_op
        elif _token == '"addi"':
            addi_op = self.addi_op(_context)
            ret = addi_op
        elif _token == '"addiu"':
            addiu_op = self.addiu_op(_context)
            ret = addiu_op
        elif _token == '"subu"':
            subu_op = self.subu_op(_context)
            ret = subu_op
        elif _token == '"div"':
            div_op = self.div_op(_context)
            ret = div_op
        elif _token == '"divu"':
            divu_op = self.divu_op(_context)
            ret = divu_op
        else: # == '"mult"'
            mult_op = self.mult_op(_context)
            ret = mult_op
        return ret

    def bool_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bool_op', [])
        _token = self._peek('"and"', '"or"', '"andi"', '"ori"', '"beq"', '"bne"', '"slt"', '"slti"', '"sltu"', '"sltiu"')
        if _token == '"and"':
            and_op = self.and_op(_context)
            ret = and_op
        elif _token == '"or"':
            or_op = self.or_op(_context)
            ret = or_op
        elif _token == '"andi"':
            andi_op = self.andi_op(_context)
            ret = andi_op
        elif _token == '"ori"':
            ori_op = self.ori_op(_context)
            ret = ori_op
        elif _token == '"beq"':
            beq_op = self.beq_op(_context)
            ret = beq_op
        elif _token == '"bne"':
            bne_op = self.bne_op(_context)
            ret = bne_op
        elif _token == '"slt"':
            slt_op = self.slt_op(_context)
            ret = slt_op
        elif _token == '"slti"':
            slti_op = self.slti_op(_context)
            ret = slti_op
        elif _token == '"sltu"':
            sltu_op = self.sltu_op(_context)
            ret = sltu_op
        else: # == '"sltiu"'
            sltiu_op = self.sltiu_op(_context)
            ret = sltiu_op
        return ret

    def pseudo_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'pseudo_op', [])
        _token = self._peek('"la"', '"li"', '"move"', '"bgt"', '"blt"', '"bge"', '"ble"', '"bgtu"', '"bgtz"')
        if _token == '"la"':
            la_op = self.la_op(_context)
            ret = la_op
        elif _token == '"li"':
            li_op = self.li_op(_context)
            ret = li_op
        elif _token == '"move"':
            move_op = self.move_op(_context)
            ret = move_op
        elif _token == '"bgt"':
            bgt_op = self.bgt_op(_context)
            ret = bgt_op
        elif _token == '"blt"':
            blt_op = self.blt_op(_context)
            ret = blt_op
        elif _token == '"bge"':
            bge_op = self.bge_op(_context)
            ret = bge_op
        elif _token == '"ble"':
            ble_op = self.ble_op(_context)
            ret = ble_op
        elif _token == '"bgtu"':
            bgtu_op = self.bgtu_op(_context)
            ret = bgtu_op
        else: # == '"bgtz"'
            bgtz_op = self.bgtz_op(_context)
            ret = bgtz_op
        return ret

    def la_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'la_op', [])
        self._scan('"la"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return LA(dst, ref)

    def li_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'li_op', [])
        self._scan('"li"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        im = immediate
        return LI(dst, im)

    def move_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'move_op', [])
        self._scan('"move"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        src = REGISTER
        return MOVE(dst, src)

    def bgt_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bgt_op', [])
        self._scan('"bgt"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BGT(reg1, reg2, ref)

    def blt_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'blt_op', [])
        self._scan('"blt"')
        ret = []
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        _token = self._peek('REGISTER', 'NUM', 'HEX')
        if _token == 'REGISTER':
            REGISTER = self._scan('REGISTER')
            reg2 = REGISTER
        else: # in ['NUM', 'HEX']
            immediate = self.immediate(_context)
            reg2 = "$at"
            ret = [LI(reg2, immediate)]
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        ret.append(BLT(reg1, reg2, ref))
        return ret

    def bge_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bge_op', [])
        self._scan('"bge"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BGE(reg1, reg2, ref)

    def ble_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'ble_op', [])
        self._scan('"ble"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BLE(reg1, reg2, ref)

    def bgtu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bgtu_op', [])
        self._scan('"bgtu"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BGTU(reg1, reg2, ref)

    def bgtz_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bgtz_op', [])
        self._scan('"bgtz"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BGTZ(reg1, ref)

    def add_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'add_op', [])
        self._scan('"add"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return ADD(dst, reg1, reg2)

    def sub_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'sub_op', [])
        self._scan('"sub"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return SUB(dst, reg1, reg2)

    def addu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'addu_op', [])
        self._scan('"addu"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return ADDU(dst, reg1, reg2)

    def addi_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'addi_op', [])
        self._scan('"addi"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        imm = immediate
        return ADDI(dst, reg1, imm)

    def addiu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'addiu_op', [])
        self._scan('"addiu"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        imm = immediate
        return ADDIU(dst, reg1, imm)

    def subu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'subu_op', [])
        self._scan('"subu"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return SUBU(dst, reg1, reg2)

    def div_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'div_op', [])
        self._scan('"div"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return DIV(reg1, reg2)

    def divu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'divu_op', [])
        self._scan('"divu"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return DIVU(reg1, reg2)

    def mult_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'mult_op', [])
        self._scan('"mult"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return MULT(reg1, reg2)

    def and_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'and_op', [])
        self._scan('"and"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return AND(dst, reg1, reg2)

    def or_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'or_op', [])
        self._scan('"or"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return OR(dst, reg1, reg2)

    def andi_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'andi_op', [])
        self._scan('"andi"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        imm = immediate
        return ANDI(dst, reg1, imm)

    def ori_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'ori_op', [])
        self._scan('"ori"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        imm = immediate
        return ORI(dst, reg1, imm)

    def beq_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'beq_op', [])
        self._scan('"beq"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        ref = LABEL_REF
        return BEQ(reg1, reg2, ref)

    def bne_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'bne_op', [])
        self._scan('"bne"')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        self._scan('","')
        LABEL_REF = self._scan('LABEL_REF')
        lref = LABEL_REF
        return BNE(reg1, reg2, label_ref)

    def slt_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'slt_op', [])
        self._scan('"slt"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg2 = REGISTER
        return SLT(dst, reg1, reg2)

    def slti_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'slti_op', [])
        self._scan('"slti"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg1 = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        imm = immediate
        return SLTI(dst, reg1, imm)

    def sltu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'sltu_op', [])
        self._scan('"sltu"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        im = immediate
        return SLTU(dst, reg, im)

    def sltiu_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'sltiu_op', [])
        self._scan('"sltiu"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        REGISTER = self._scan('REGISTER')
        reg = REGISTER
        self._scan('","')
        immediate = self.immediate(_context)
        im = immediate
        return SLTIU(dst, reg, im)

    def jump_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'jump_op', [])
        self._scan('"j"')
        LABEL_REF = self._scan('LABEL_REF')
        return JUMP(LABEL_REF)

    def jal_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'jal_op', [])
        self._scan('"jal"')
        LABEL_REF = self._scan('LABEL_REF')
        return JAL(LABEL_REF)

    def jr_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'jr_op', [])
        self._scan('"jr"')
        REGISTER = self._scan('REGISTER')
        return JR(REGISTER)

    def mfhi_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'mfhi_op', [])
        self._scan('"mfhi"')
        REGISTER = self._scan('REGISTER')
        return MFHI(REGISTER)

    def mflo_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'mflo_op', [])
        self._scan('"mflo"')
        REGISTER = self._scan('REGISTER')
        return MFLO(REGISTER)

    def lw_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'lw_op', [])
        self._scan('"lw"')
        REGISTER = self._scan('REGISTER')
        dst = REGISTER
        self._scan('","')
        indirect_address = self.indirect_address(_context)
        iaddress = indirect_address
        return LW(dst, iaddress)

    def sw_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, self._pos, 'sw_op', [])
        self._scan('"sw"')
        REGISTER = self._scan('REGISTER')
        src = REGISTER
        self._scan('","')
        indirect_address = self.indirect_address(_context)
        iaddress = indirect_address
        return SW(src, iaddress)


def parse(rule, text):
    P = MipsParser(MipsParserScanner(text))
    return yappsrt.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
