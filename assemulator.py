file_read = open("read_file.asm","r")
file_write= open("write_file.mc","w+")
if file_read.mode=='r':
    asm_code=file_read.read()
    if asm_code.find(".data")>=0 :
        data = asm_code[asm_code.find(".data")+5:asm_code.find(".text")].strip()        #Sheky will look into for 5
        instructions = data.split('\n')
        data_address = int("0x10000000", 0)
        for i in range(len(instructions) - 1, -1, -1):
            if(instructions[i]==''):                                                    #removal of '\n's
                del instructions[i]
            else:
                file_write.write(hex(data_address)+' \n')
        print(instructions)
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