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

def R_type(words):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    funct7=mnemonic_fmt[words[0]][3]

    rd='{0:05b}'.format(int(words[1][1:]))
    rs1='{0:05b}'.format(int(words[2][1:]))
    rs2='{0:05b}'.format(int(words[3][1:]))

    machine_code=funct7 + rs2 + rs1 + funct3 + rd + opcode
    return machine_code

def I_type(words):
    #words=instruction.split()
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

def S_type(words):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    rs1='{0:05b}'.format(int(words[1][1:]))

    temp_str=''
    # third word should be in the format like 986(x7)
    for i in range(2, len(words)):
        temp_str += words[i]

    offset = temp_str[0:temp_str.find('(')]
    rs2=temp_str[temp_str('(')+2:temp_str(')')]

    imm=''
    if(offset[0:2] == '0x'):
        imm='{0:012b}'.format(int(offset[2:], 16))

    elif(offset[0:2] == '0b'):
        imm='{0:012b}'.format(int(offset[2:], 2))
        
    else:
        imm=BitArray(int=int(offset), length=12).bin

    machine_code = imm[0:7] + rs2 + rs1 + funct3 + imm[7:12] + opcode
    return machine_code


def SB_type(words, label_offset):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    funct3=mnemonic_fmt[words[0]][2]
    rs1='{0:05b}'.format(int(words[1][1:]))
    rs2='{0:05b}'.format(int(words[2][1:]))

    label_offset = label_offset
    imm=BitArray(int=int(str(label_offset)), length=12).bin

    machine_code = imm[0:7] + rs2 + rs1 + funct3 + imm[7:12] + opcode
    return machine_code

def U_type(words, var_address):
    #words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    rd='{0:05b}'.format(int(words[1][1:]))
    
    machine_code = var_address + rd + opcode
    return machine_code

def UJ_type(words, label_address):
#    words=instruction.split()
    opcode=mnemonic_fmt[words[0]][1]
    rd='{0:05b}'.format(int(words[1][1:]))

    machine_code = label_address + rd + opcode
    return machine_code

file_write= open("write_file.mc","w+")
file_read = open("read_file.asm","r")

if file_read.mode=='r':
    asm_code=file_read.read()
    # .data and .text part of the code can come in any order
    if(asm_code.find('.data') >= 0):
        data = ''
        text = ''
        
        if asm_code.find(".data") < asm_code.find('.text') :
            data = asm_code[asm_code.find(".data")+5:asm_code.find(".text")].strip()        #Sheky have looked into for 5
            text = asm_code[asm_code.find('.text')+5:].strip()
        else:
            text = asm_code[asm_code.find('.text')+5:asm_code.find('.data')].strip()
            data = asm_code[asm_code.find('.data')+5:].strip()

        #Handling of data part of code starts here
        dictionary = {}                                                                 #Declaration of a dictionary(to be used later as reference to memory addresses)
        instructions = data.split('\n')
        data_address = int("0x10000000", 0)
        for i in range(len(instructions) - 1, -1, -1):
            if(instructions[i]==''):                                                    #removal of '\n's
                del instructions[i]
            else:
                dictionary[instructions[i][:instructions[i].find(':')].strip()] = hex(data_address)
                if instructions[i].find('.word')>=0:
                    for word in (instructions[i][instructions[i].find('.word'):].strip()).split():
                        try:
                            file_write.write(str(hex(data_address))+' '+str(hex(int(word)))+'\n')
                            data_address=data_address+4
                        except: pass
                if instructions[i].find('.byte')>=0:
                    for byte in (instructions[i][instructions[i].find('.byte'):].strip()).split():
                        try:
                            file_write.write(str(hex(data_address))+' '+str(hex(int(byte)))+'\n')
                            data_address=data_address+1
                        except: pass
                #file_write.write(hex(data_address)+' \n')
        print(instructions)
        print(dictionary)

        # Handling of text part ends here
        #registers = {'x0':0, 'x1':0, 'x2':2147483632, 'x3':268435456, 'x4':0, 'x5':0, 'x6':0, 'x7':0, 'x8':0, 'x9':0, 'x10':0, 'x11':0, 'x12':0, 'x13':0, 'x14':0, 'x15':0, 'x16':0, 'x17':0, 'x18':0, 'x19':0, 'x20':0, 'x21':0, 'x22':0, 'x23':0, 'x24':0, 'x25':0, 'x26':0, 'x27':0, 'x28':0, 'x29':0, 'x30':0, 'x31':0}
        #print(len(registers))
        #print(registers)

        instructions = list(filter(bool, text.splitlines()))
        # Assuming there is no extra '\n' in the text part of the code
        n=len(instructions)
        
        label_position={}
        for i in range(0, n):
            k=instructions[i].find(':')
            if (k > 0):
                instructions[i]=instructions[i].strip()
                label_position[instructions[i][:k-1]]=i

        for i in range(0, n):
            instructions[i]=instructions[i].replace(',', ' ')
            words=instructions[i].split()

            pc=hex(i*4)+' '
            if(mnemonic_fmt[words[0]][0] == 'R'):
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(R_type(words), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(R_type(words), 2)))
                file_write.write('\n')
            elif(mnemonic_fmt[words[0]][0] == 'I'):
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(I_type(words), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(I_type(words), 2)))
                file_write.write('\n')
            elif(mnemonic_fmt[words[0]][0] == 'S'):
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(S_type(words), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(S_type(words), 2)))
                file_write.write('\n')
            elif(mnemonic_fmt[words[0]][0] == 'SB'):
                var=(label_position[words[3]]-i)*4
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(SB_type(words, var), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(SB_type(words, var))))
                file_write.write('\n')
            elif(mnemonic_fmt[words[0]][0] == 'U'):
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(U_type(words, '10101'), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(U_type(words, '10101'), 2)))
                file_write.write('\n')
            elif(mnemonic_fmt[words[0]][0] == 'UJ'):
                file_write.write(pc)
                print('0x' + '{0:08x}'.format(int(UJ_type(words, '10101'), 2)))
                file_write.write('0x' + '{0:08x}'.format(int(UJ_type(words, '10101'), 2)))
                file_write.write('\n')

    else:
        pass


# if file_read.mode == 'r':
#     asm_code=file_read.read()
#     instructions=asm_code.split('\n')
#     for line in instructions:
#         line=line.replace(', ',' ')
#         line=line.replace(' ,',' ')
#         line=line.replace(',',' ')
#         words=line.split(' ')
#         print(words)