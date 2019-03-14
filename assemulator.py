file_read = open("read_file.asm","r")
file_write= open("write_file.mc","w+")
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
        instructions = text.split('\n')
        for instruction in instructions:
            instruction=instruction.replace(', ', ' ')
            instruction=instruction.replace(' ,', ' ')
            instruction=instruction.replace(',', ' ')
            words=instruction.split(' ')
            
            if(words[0] == 'lw'):
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