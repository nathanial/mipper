from mipper import *
from gnrl_ops import *
from math_ops import *
from bool_ops import *
%%
parser MipsParser:
    ignore: ' '
    token END: "$"
    token NUM: '-?[0-9]+'
    token HEX: '0x[0-9]+'
    token REGISTER: '\$(gp|sp|fp|ra|v[0-1]|a[0-3]|t[0-9]|s[0-7]|k[0-1]|zero)'
    token LABEL: '\\w+:'
    token LABEL_REF: '\\w+'
    token SYSTEM_CALL: 'syscall'
    token STRING: '"[^"]*"'
    token COMMENT: '#[^\n]*\n'

    rule end_line: "\n" | COMMENT

    rule empty_line: end_line

    rule program: empty_line*
                  (data text {{ ret = data, text }} |
                   text data {{ ret = data, text }}) END {{ return ret }}

    rule data: ".data\n" {{ allocations = [] }}
               (allocation {{ allocations.append(allocation) }} |
                empty_line)*
               {{ return allocations }}

    rule text: ".text\n" {{ lines = [] }}
                       (statement {{ lines.append(statement) }} |
                        LABEL end_line {{ lines.append(LABEL.strip(':')) }} |
                        SYSTEM_CALL end_line {{ lines.append(SYSCALL()) }} |
                        empty_line)+
                        {{ return lines }}

    rule allocation: LABEL (allocate_asciiz {{ f = allocate_asciiz }} |
                            allocate_space {{ f = allocate_space }}) end_line
                            {{ return f(LABEL.strip(':')) }}

    rule allocate_asciiz: ".asciiz" STRING {{ str_val = STRING }}
                          {{ return lambda lbl : CREATE_STRING(lbl, str_val) }}

    rule allocate_space: ".space" NUM {{ nsize = NUM }}
                         {{ return lambda lbl : CREATE_SPACE(lbl, nsize) }}

    rule immediate: NUM {{ return int(NUM, 10) }} | HEX {{ return int(HEX, 16) }}
    rule num_or_register: NUM | REGISTER

    rule indirect_address: {{ offset = 0 }}
                           (NUM {{ offset = NUM }} |
                            LABEL_REF {{ offset = LABEL_REF }})?
                           "\\(" REGISTER {{ reg = REGISTER }} "\\)"
                           {{ return (offset, reg) }}


    rule statement: (gnrl_op {{ ret = gnrl_op }} |
                     math_op {{ ret = math_op }} |
                     bool_op {{ ret = bool_op }} |
                     pseudo_op {{ ret = pseudo_op }})
                     end_line {{ return ret }}

    rule gnrl_op: (jump_op {{ ret = jump_op }} |
                   jal_op {{ ret = jal_op }} |
                   jr_op {{ ret = jr_op }} |
                   mfhi_op {{ ret = mfhi_op }} |
                   mflo_op {{ ret = mflo_op }} |
                   lw_op {{ ret = lw_op }} |
                   sw_op {{ ret = sw_op }} |
                   syscall {{ ret = sycall }}) {{ return ret }}

    rule math_op: (add_op {{ ret = add_op }} |
                   sub_op {{ ret = sub_op }} |
                   addu_op {{ ret = addu_op }} |
                   addi_op {{ ret = addi_op }} |
                   addiu_op {{ ret = addiu_op }} |
                   subu_op {{ ret = subu_op }} |
                   div_op {{ ret = div_op }} |
                   divu_op {{ ret = divu_op }} |
                   mult_op {{ ret = mult_op }})
                   {{ return ret }}

    rule bool_op: (and_op {{ ret = and_op }} |
                   or_op {{ ret = or_op }} |
                   andi_op {{ ret = andi_op }} |
                   ori_op {{ ret = ori_op }} |
                   beq_op {{ ret = beq_op }} |
                   bne_op {{ ret = bne_op }} |
                   slt_op {{ ret = slt_op }} |
                   slti_op {{ ret = slti_op }} |
                   sltu_op {{ ret = sltu_op }} |
                   sltiu_op {{ ret = sltiu_op }})
                   {{ return ret }}

    #math ops ----------------------------------

    rule add_op: "add"
                 REGISTER {{ dst = REGISTER }} ","
                 REGISTER {{ reg1 = REGISTER }} ","
                 REGISTER {{ reg2 = REGISTER }}
                 {{ return ADD(dst, reg1, reg2) }}

    rule sub_op: "sub"
                 REGISTER {{ dst = REGISTER }} ","
                 REGISTER {{ reg1 = REGISTER }} ","
                 REGISTER {{ reg2 = REGISTER }}
                 {{ return SUB(dst, reg1, reg2) }}

    rule addu_op: "addu"
                  REGISTER {{ dst = REGISTER }} ","
                  REGISTER {{ reg1 = REGISTER }} ","
                  REGISTER {{ reg2 = REGISTER }}
                  {{ return ADDU(dst, reg1, reg2) }}

    rule addi_op: "addi"
                  REGISTER {{ dst = REGISTER }} ","
                  REGISTER {{ reg1 = REGISTER }} ","
                  immediate {{ imm = immediate }}
                  {{ return ADDI(dst, reg1, imm) }}

    rule addiu_op: "addiu"
                   REGISTER {{ dst = REGISTER }} ","
                   REGISTER {{ reg1 = REGISTER }} ","
                   immediate {{ imm = immediate }}
                   {{ return ADDIU(dst, reg1, imm) }}

    rule subu_op: "subu"
                  REGISTER {{ dst = REGISTER }} ","
                  REGISTER {{ reg1 = REGISTER }} ","
                  REGISTER {{ reg2 = REGISTER }}
                  {{ return SUBU(dst, reg1, reg2) }}

    rule div_op: "div" REGISTER {{ reg1 = REGISTER }} ","
                       REGISTER {{ reg2 = REGISTER }}
                       {{ return DIV(reg1, reg2) }}

    rule divu_op: "divu" REGISTER {{ reg1 = REGISTER}} ","
                         REGISTER {{ reg2 = REGISTER}}
                         {{ return DIVU(reg1, reg2) }}

    rule mult_op: "mult" REGISTER {{ reg1 = REGISTER}} ","
                         REGISTER {{ reg2 = REGISTER}}
                         {{ return MULT(reg1, reg2) }}

    #bool ops ------------------------

    rule and_op: "and"
                 REGISTER {{ dst = REGISTER }} ","
                 REGISTER {{ reg1 = REGISTER }} ","
                 REGISTER {{ reg2 = REGISTER }}
                 {{ return AND(dst, reg1, reg2) }}

    rule or_op: "or"
                REGISTER {{ dst = REGISTER }} ","
                REGISTER {{ reg1 = REGISTER }} ","
                REGISTER {{ reg2 = REGISTER }}
                {{ return OR(dst, reg1, reg2) }}

    rule andi_op: "andi"
                  REGISTER {{ dst = REGISTER }} ","
                  REGISTER {{ reg1 = REGISTER }} ","
                  immediate {{ imm = immediate }}
                  {{ return ANDI(dst, reg1, imm) }}

    rule ori_op: "ori"
                 REGISTER {{ dst = REGISTER }} ","
                 REGISTER {{ reg1 = REGISTER }} ","
                 immediate {{ imm = immediate }}
                 {{ return ORI(dst, reg1, imm) }}

    rule beq_op: "beq"
                 REGISTER {{ reg1 = REGISTER }}
                 REGISTER {{ reg2 = REGISTER }}
                 LABEL_REF {{ lref = LABEL_REF }}
                 {{ return BEQ(reg1, reg2, label_ref) }}

    rule bne_op: "bne"
                 REGISTER {{ reg1 = REGISTER }}
                 REGISTER {{ reg2 = REGISTER }}
                 LABEL_REF {{ lref = LABEL_REF }}
                 {{ return BNE(reg1, reg2, label_ref) }}

    rule slt_op: "slt"
                 REGISTER {{ dst = REGISTER }}
                 REGISTER {{ reg1 = REGISTER }}
                 REGISTER {{ reg2 = REGISTER }}
                 {{ return SLT(dst, reg1, reg2) }}

    rule slti_op: "slti"
                  REGISTER {{ dst = REGISTER }}
                  REGISTER {{ reg1 = REGISTER }}
                  immediate {{ imm = immediate }}
                  {{ return SLTI(dst, reg1, imm) }}

    rule sltu_op: "sltu"
                  REGISTER {{ dst = REGISTER }}
                  REGISTER {{ reg = REGISTER }}
                  immediate {{ im = immediate }}
                  {{ return SLTU(dst, reg, im) }}

    rule sltiu_op: "sltiu"
                   REGISTER {{ dst = REGISTER }}
                   REGISTER {{ reg = REGISTER }}
                   immediate {{ im = immediate }}
                   {{ return SLTIU(dst, reg, im) }}

    #gnrl ops ---------------------------

    rule jump_op: "j" LABEL_REF {{ return JUMP(LABEL_REF) }}

    rule jal_op: "jal" LABEL_REF {{ return JAL(LABEL_REF) }}

    rule jr_op: "jr" REGISTER {{ return JR(REGISTER) }}

    rule mfhi_op: "mfhi" REGISTER {{ return MFHI(REGISTER) }}

    rule mflo_op: "mflo" REGISTER {{ return MFLO(REGISTER) }}

    rule lw_op: "lw"
                REGISTER {{ dst = REGISTER }}
                indirect_address {{ iaddress = indirect_address }}
                {{ return LW(dst, iaddress) }}

    rule sw_op: "sw"
                REGISTER {{ src = REGISTER }}
                indirect_address {{ iaddress = indirect_address }}
                {{ return SW(src, iaddress) }}

    rule syscall: SYSTEM_CALL {{ return SYSCALL() }}
