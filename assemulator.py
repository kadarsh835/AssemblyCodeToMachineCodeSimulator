file_read = open("read_file.asm","r")
file_write= open("write_file.mc","w+")
if file_read.mode=='r':
    asm_code=file_read.read()
    if asm_code.find(".data")>=0 :
        dictionary = {}                                                                 #Declaration of a dictionary(to be used later as reference to memory addresses)
        data = asm_code[asm_code.find(".data")+5:asm_code.find(".text")].strip()        #Sheky will look into for 5
        #Handling of data part of code starts here
        instructions = data.split('\n')
        data_address = int("0x10000000", 0)
        for i in range(len(instructions) - 1, -1, -1):
            if(instructions[i]==''):                                                    #removal of '\n's
                del instructions[i]
            else:
                dictionary[instructions[i][:instructions[i].find(':')].strip()] = hex(data_address)
                for word in (instructions[i][instructions[i].find('.word'):].strip()).split():
                    try:#we are never ever ever getting back together
                        file_write.write(str(hex(data_address))+' '+str(hex(int(word)))+'\n')
                        data_address=data_address+4
                    except: pass
                for byte in (instructions[i][instructions[i].find('.byte'):].strip()).split():
                    try:
                        file_write.write(str(hex(data_address))+' '+str(hex(int(byte)))+'\n')
                        data_address=data_address+1
                    except: pass
                #file_write.write(hex(data_address)+' \n')
        print(instructions)
        print(dictionary)
        #Handling of Data part ends here
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