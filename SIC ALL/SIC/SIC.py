import math

HexDict = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
           8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}


def Dec2Hex(Dec):
    Hex = ''
    while (Dec >= 16):
        Hex = (HexDict[Dec % 16] + Hex)
        Dec //= 16

    Hex = (HexDict[Dec] + Hex)
    return Hex


DecDict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}


def Hex2Dec(Hex):
    Dec = 0
    times = 0
    while (len(Hex) > 0):
        Dec += int(DecDict[Hex[-1]] * math.pow(16, times))
        Hex = Hex[:-1]
        times += 1

    return Dec


def BYTE(value):
    mode = value[0]
    data = value[2:-1]
    objCode = ''
    if (mode == 'C'):
        for i in data:
            objCode += (Dec2Hex(ord(i))).zfill(2)
    elif (mode == 'X'):
        objCode += data
    else:
        print('BYTE Error')

    index_add = (len(objCode)//2)
    return index_add, objCode


def WORD(value):
    if (int(value) >= 0):
        objCode = Dec2Hex(int(value)).zfill(6)
    else:
        full_hex = Hex2Dec('1000000')
        objCode = Dec2Hex(full_hex + int(value)).zfill(6)
    index_add = (len(objCode)//2)
    return index_add, objCode


def RESB(value):
    objCode = ''
    index_add = int(value)
    return index_add, objCode


def RESW(value):
    objCode = ''
    index_add = (int(value) * 3)
    return index_add, objCode


instruction_convert = {
    "ADD": "18", "ADDF": "58", "ADDR": "90", "AND": "40", "CLEAR": "B4", "COMP": "28", "COMPF": "88", "COMPR": "A0",
    "DIV": "24", "DIVF": "64", "DIVR": "9C", "FIX": "C4", "FLOAT": "C0", "HIO": "F4",
    "J": "3C", "JEQ": "30", "JGT": "34", "JLT": "38", "JSUB": "48",
    "LDA": "00", "LDB": "68", "LDCH": "50", "LDF": "70", "LDL": "08", "LDS": "6C", "LDT": "74", "LDX": "04", "LPS": "E0",
    "MUL": "20", "MULF": "60", "MULR": "98", "NORM": "C8", "OR": "44", "RD": "D8", "RMO": "AC", "RSUB": "4C",
    "SHIFTL": "A4", "SHIFTR": "A8", "SIO": "F0", "SSK": "EC", "STA": "0C", "STB": "78", "STCH": "54", "STF": "80", "STI": "D4",
    "STL": "14", "STS": "7C", "STSW": "E8", "STT": "84", "STX": "10", "SUB": "1C", "SUBF": "5C", "SUBR": "94", "SVC": "B0",
    "TD": "E0", "TIO": "F8", "TIX": "2C", "TIXR": "B8", "WD": "DC"}

pseudo_instruction = ['START', 'BYTE', 'WORD', 'RESB', 'RESW', 'END']

original_input = {}  # 儲存 location 的原始輸入
function_index = {}  # 儲存 function 所在位置
# 後續轉 object code 會需要(ex:00(opcode)RESTART(location:1850) => 001850)
object_code = {}  # 儲存 location 的 object code


with open('Input.txt', 'r', encoding='utf-8') as inp:
    input = inp.readlines()

    start = input[0].replace('\n', '').split(' ')
    if (start[-2] != 'START'):
        print('Error START')

    else:
        index = [Dec2Hex(Hex2Dec(start[-1]))]

        for i in input:
            if (i[0] == '.'):  # 註解
                continue

            now_input = []
            now = i.replace('\n', '').split(' ')

            for j in range(len(now)):
                if ((now[j] in instruction_convert) or (now[j] in pseudo_instruction)):

                    if (now[j] != 'START'):
                        if (now[j] == 'BYTE'):
                            index_add, objCode = BYTE(now[j+1])
                        elif (now[j] == 'WORD'):
                            index_add, objCode = WORD(now[j+1])
                        elif (now[j] == 'RESB'):
                            index_add, objCode = RESB(now[j+1])
                        elif (now[j] == 'RESW'):
                            index_add, objCode = RESW(now[j+1])
                        elif (now[j] == 'END'):
                            index_add, objCode = 0, ''
                        else:
                            index_add = 3
                            try:
                                if (',X' in now[j+1]):
                                    objCode = f'nx,{instruction_convert[now[j]]}{now[j+1]}'
                                else:
                                    objCode = f'n,{instruction_convert[now[j]]}{now[j+1]}'
                            except:
                                objCode = f'{instruction_convert[now[j]]}0000'

                        next_index = Dec2Hex(Hex2Dec(index[-1]) + index_add)
                    else:
                        index_add, objCode = 0, ''
                        next_index = index[0]
                        original_input['START'] = now

                    if (j == 1):
                        if now[0] not in function_index:
                            function_index[now[0]] = index[-1]
                        else:
                            print('Function Error, line:', index[-1])

                        now_input = [now[0]] + now[1:]
                    else:
                        now_input = [''] + now

                    if (len(now_input) == 2):
                        now_input.append('')

                    object_code[index[-1]] = objCode
                    original_input[index[-1]] = now_input

                    index.append(next_index)

        for i in object_code.keys():
            if ('n' in object_code[i]):
                objCode = object_code[i].split(',')[1]
                address = function_index[objCode[2:]]
                if (len(address) < 4):
                    address = ("0"*(4 - len(address)) + address)
                if ('nx' in object_code[i]):
                    address = (Dec2Hex(int(address[0]) + 8) + address[1:])

                object_code[i] = (objCode[:2] + address)


print('\n\nLine'.ljust(15) + 'Location'.ljust(15) +
      'Original input'.ljust(45) + 'Object code'.rjust(15))
print('------------------------------------------------------------------------------------------')


print(str(5).ljust(15) + index[0].ljust(15) +
      original_input['START'][0].ljust(15) +
      original_input['START'][1].ljust(15) +
      original_input['START'][2].ljust(15) +
      ''.rjust(15))

for i, location in enumerate(index[1:-1]):
    line = (i+2)*5
    print(str(line).ljust(15) +
          location.ljust(15) +
          original_input[location][0].ljust(15) +
          original_input[location][1].ljust(15) +
          original_input[location][2].ljust(15) +
          object_code[location].rjust(15))
