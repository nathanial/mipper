from mipper import *
from ops import *
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

    rule statement: (add_op {{ ret = add_op }} |
                    addi_op {{ ret = addi_op }} |
                    li_op {{ ret = li_op }} |
                    j_op {{ ret = j_op }} |
                    beq_op {{ ret = beq_op }} |
                    bne_op {{ ret = bne_op }} |
                    blt_op {{ ret = blt_op }} |
                    la_op {{ ret = la_op }} |
                    jal_op {{ ret = jal_op }} |
                    jr_op {{ ret = jr_op }} |
                    move_op {{ ret = move_op }} |
                    div_op {{ ret = div_op }} |
                    mfhi_op {{ ret = mfhi_op }} |
                    lw_op {{ ret = lw_op }} |
                    sw_op {{ ret = sw_op }} ) end_line {{ return ret }}

    rule immediate: NUM {{ return int(NUM, 10) }} | HEX {{ return int(HEX, 16) }}
    rule num_or_register: NUM | REGISTER

    rule indirect_address: {{ offset = 0 }}
                           (NUM {{ offset = NUM }} |
                            LABEL_REF {{ offset = LABEL_REF }})?
                           "\\(" REGISTER {{ reg = REGISTER }} "\\)"
                           {{ return (offset, reg) }}

    rule add_op: "add"
                 REGISTER {{ dst = REGISTER }} ","
                 REGISTER {{ reg1 = REGISTER }} ","
                 REGISTER {{ reg2 = REGISTER }}
                 {{ return ADD(dst, reg1, reg2) }}

    rule addi_op: "addi"
                  REGISTER {{ dst = REGISTER }} ","
                  REGISTER {{ reg1 = REGISTER }} ","
                  immediate {{ imm = immediate }}
                  {{ return ADDI(dst, reg1, imm) }}

    rule li_op: "li"
                REGISTER {{ dst = REGISTER }} ","
                immediate {{ imm = immediate }}
                {{ return ADDIU(dst, "$0", imm) }}

    rule j_op: "j" LABEL_REF {{ return JUMP(LABEL_REF) }}

    rule beq_op: "beq" REGISTER {{ arg1 = REGISTER }} ","
                       REGISTER {{ arg2 = REGISTER }} ","
                       LABEL_REF {{ arg3 = LABEL_REF }}
                 {{ return BEQ(arg1, arg2, arg3) }}

    rule bne_op: "bne" REGISTER {{ arg1 = REGISTER }} ","
                       REGISTER {{ arg2 = REGISTER }} ","
                       LABEL_REF {{ arg3 = LABEL_REF }}
                 {{ return BNE(arg1, arg2, arg3) }}

    rule blt_op: "blt" REGISTER {{ arg1 = REGISTER }} ","
                       REGISTER {{ arg2 = REGISTER }} ","
                       LABEL_REF {{ arg3 = LABEL_REF }}
                 {{ return BLT(arg1, arg2, arg3) }}

    rule la_op: "la" REGISTER {{ reg1 = REGISTER }} ","
                     LABEL_REF {{ address = LABEL_REF }}
                     {{ return LA(reg1, address) }}

    rule jal_op: "jal" LABEL_REF {{ return JAL(LABEL_REF) }}

    rule jr_op: "jr" REGISTER {{ return JR(REGISTER) }}

    rule move_op: "move" REGISTER {{ dst = REGISTER }} ","
                         REGISTER {{ src = REGISTER }}
                         {{ return MOVE(dst, src) }}

    rule div_op: "div" REGISTER {{ reg1 = REGISTER }} ","
                       REGISTER {{ reg2 = REGISTER }}
                       {{ return DIV(reg1, reg2) }}

    rule mfhi_op: "mfhi" REGISTER {{ dst = REGISTER }}
                  {{ return MFHI(dst) }}

    rule lw_op: "lw" REGISTER {{ dst = REGISTER }} ","
                     indirect_address {{ iaddress = indirect_address }}
                     {{ return LW(dst, iaddress) }}

    rule sw_op: "sw" REGISTER {{ src = REGISTER }} ","
                     indirect_address {{ iaddress = indirect_address }}
                     {{ return SW(src, iaddress) }}