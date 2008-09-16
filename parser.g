from mipper import *
from ops import *
%%
parser MipsParser:
    ignore: ' '
    token END: "$"
    token NUM: '[0-9]+'
    token HEX: '0x[0-9]+'
    token REGISTER: '\$(gp|sp|fp|ra|v[0-1]|a[0-3]|t[0-9]|s[0-7]|k[0-1]|zero)'
    token LABEL: '\\w+:'
    token LABEL_REF: '\\w+'
    token SYSCALL: 'syscall'
    token STRING: '"[^"]*"'
    
    rule program: (data text {{ ret = data, text }} |
                   text data {{ ret = data, text }}) END {{ return ret }}

    rule data: ".data\n" {{ allocations = {} }}
               (allocation {{ allocations.update(allocation) }})*
               {{ return allocations }}

    rule text: ".text\n" {{ lines = [] }}
                       (statement {{ lines.append(statement) }} |
                        LABEL "\n" {{ lines.append(LABEL.strip(':')) }} |
                        SYSCALL "\n" {{ lines.append(SYSCALL) }})+
                        {{ return lines }}

    rule allocation: LABEL ".asciiz"?
                           ( immediate {{ value = immediate }} |
                             STRING {{ value = STRING }} ) "\n"
                             {{ return [[LABEL.strip(':'), value.strip('"')]] }}


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
                    mfhi_op {{ ret = mfhi_op }}) "\n" {{ return ret }}

    rule immediate: NUM {{ return int(NUM, 10) }} | HEX {{ return int(HEX, 16) }}

    rule indirect_address: {{ offset = 0 }}
                           (NUM {{ offset = NUM }})?
                           "\\(" REGISTER {{ reg = REGISTER }} "\\)"
                           {{ return (offset, register) }}

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
                {{ return LI(dst, imm) }}

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