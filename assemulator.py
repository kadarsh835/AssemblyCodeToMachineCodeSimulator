
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
def converter(instruction):
    if():



file_read = open("read_file.asm","r")
file_write= open("write_file.mc","w+")
if file_read.mode=='r':
    asm_code=file_read.read()
    registers = {'x0':0, 'x1':0, 'x2':2147483632, 'x3':268435456, 'x4':0, 'x5':0, 'x6':0, 'x7':0, 'x8':0, 'x9':0, 'x10':0, 'x11':0, 'x12':0, 'x13':0, 'x14':0, 'x15':0, 'x16':0, 'x17':0, 'x18':0, 'x19':0, 'x20':0, 'x21':0, 'x22':0, 'x23':0, 'x24':0, 'x25':0, 'x26':0, 'x27':0, 'x28':0, 'x29':0, 'x30':0, 'x31':0}
    print(len(registers))
    print(registers)
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
        registers = {'x0':0, 'x1':0, 'x2':2147483632, 'x3':268435456, 'x4':0, 'x5':0, 'x6':0, 'x7':0, 'x8':0, 'x9':0, 'x10':0, 'x11':0, 'x12':0, 'x13':0, 'x14':0, 'x15':0, 'x16':0, 'x17':0, 'x18':0, 'x19':0, 'x20':0, 'x21':0, 'x22':0, 'x23':0, 'x24':0, 'x25':0, 'x26':0, 'x27':0, 'x28':0, 'x29':0, 'x30':0, 'x31':0}
        MACHINE_CODE=''
        print(len(registers))
        print(registers)
        instructions = text.split('\n')
        for instruction in instructions:
            instruction=instruction.replace(', ', ' ')
            instruction=instruction.replace(' ,', ' ')
            instruction=instruction.replace(',', ' ')
            words=instruction.split(' ')
            
            if(words[0] == 'lw'):
                registers[words[1]] = dictionary[words[2]]



            elif(words[0] == 'add'):
                pass
            



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