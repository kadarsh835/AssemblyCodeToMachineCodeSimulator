from bitstring import BitArray


mnemonic_fmt = {
    'lb':['I', '0000011', '000'],
    'lh':['I', '0000011', '001'],
    'lw':['I', '0000011', '010'],
    'ld':['I', '0000011', '011'],
    'lbu':['I', '0000011', '100'],
    'lhu':['I', '0000011', '101'],
    'lwu':['I', '0000011', '110'],
    'fence':['I', '0001111', '000'],
    'fence.i':['I', '0001111', '001'],
    'addi':['I', '0010011', '000'],
    'slli':['I', '0010011', '001', '0000000'],
    'slti':['I', '0010011', '010'],
    'sltiu':['I', '0010011', '011'],
    'xori':['I', '0010011', '100'],
    'srli':['I', '0010011', '101', '0000000'],
    'srai':['I', '0010011', '101', '0100000'],
    'ori':['I', '0010011', '110'],
    'andi':['I', '0010011', '111'],
    'auipc':['U', '0010111'],
    'addiw':['I', '0011011', '000'],
    'slliw':['I', '0011011', '001', '0000000'],
    'srliw':['I', '0011011', '101', '0000000'],
    'sraiw':['I', '0011011', '101', '0100000'],
    'sb':['S', '0100011', '000'],
    'sh':['S', '0100011', '001'],
    'sw':['S', '0100011', '010'],
    'sd':['I', '0100011', '011'],
    'add':['R', '0110011', '000', '0000000'],
    'sub':['R', '0110011', '000', '0100000'],
    'sll':['R', '0110011', '001', '0000000'],
    'slt':['R', '0110011', '010', '0000000'],
    'sltu':['R', '0110011', '011', '0000000'],
    'xor':['R', '0110011', '100', '0000000'],
    'srl':['R', '0110011', '101', '0000000'],
    'sra':['R', '0110011', '101', '0100000'],
    'or':['R', '0110011', '110', '0000000'],
    'and':['R', '0110011', '111', '0000000'],
    'lui':['U', '0110111'],
    'addw':['R', '0111011', '000', '0000000'],
    'subw':['R', '0111011', '000', '0100000'],
    'sllw':['R', '0111011', '001', '0000000'],
    'srlw':['R', '0111011', '101', '0000000'],
    'sraw':['R', '0111011', '101', '0100000'],
    'beq':['SB', '1100011', '000'],
    'bne':['SB', '1100011', '001', ],
    'blt':['SB', '1100011', '100'],
    'bge':['SB', '1100011', '101'],
    'bltu':['SB', '1100011', '110'],
    'bgeu':['SB', '1100011', '111'],
    'jalr':['I', '1100111', '000'],
    'jal':['UJ', '1101111'],
    'ecall':['I', '1110011', '000', '000000000000'],
    'ebreak':['I', '1110011', '000', '000000000001'],
    'CSRRW':['I', '1110011', '001'],
    'CSRRS':['I', '1110011', '010'],
    'CSRRC':['I', '1110011', '011'],
    'CSRRWI':['I', '1110011', '101'],
    'CSRRSI':['I', '1110011', '110'],
    'CSRRCI':['I', '1110011', '111'],
}


def R_type(instruction):
    words=instruction.split(' ')
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    funct7=mnemonic_fmt[words[0]][3]

    rd='{0:05b}'.format(int(words[1][1:]))
    rs1='{0:05b}'.format(int(words[2][1:]))
    rs2='{0:05b}'.format(int(words[3][1:]))

    machine_code=funct7 + rs2 + rs1 + funct3 + rd + opcode
    return machine_code
    

def I_type(instruction):
    words=instruction.split(' ')
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    rd='{0:05b}'.format(int(words[1][1:]))
    rs1='{0:05b}'.format(int(words[2][1:]))
    imm=''

    if(words[3][0:2] == '0x'):
        imm='{0:012b}'.format(int(words[3][2:], 16))

    elif(words[3][0:2] == '0b'):
        imm='{0:012b}'.format(int(words[3][2:], 2))
        
    else:
        imm=BitArray(int=int(words[3]), length=12).bin


    machine_code = imm + rs1 + funct3 + rd + opcode
    return machine_code

def S_type(instruction):
    words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    rs1='{0:05b}'.format(int(words[1][1:]))

    temp_str=''
    # third word should be in the format like 986(x7)
    for i in range(2, len(words)):
        temp_str += words[i]

    offset = temp_str[0:temp_str.find('(')]
    rs2=temp_str[temp_str.find('(')+2:temp_str.find(')')]
    rs2='{0:05b}'.format(int(rs2))

    imm=''
    if(offset[0:2] == '0x'):
        imm='{0:012b}'.format(int(offset[2:], 16))

    elif(offset[0:2] == '0b'):
        imm='{0:012b}'.format(int(offset[2:], 2))
        
    else:
        imm=BitArray(int=int(offset), length=12).bin

    machine_code = imm[0:7] + rs2 + rs1 + funct3 + imm[7:12] + opcode
    return machine_code


a=input('Enter input : ')
print(S_type(a))