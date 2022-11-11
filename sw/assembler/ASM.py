from .ASMsymbolTable import SymbolTable
from .ASMcode import Code
from .ASMparser import Parser


class ASM:

    # DONE
    def __init__(self, nasm, hack):
        self.hack = hack
        self.symbolTable = SymbolTable()
        self.nasm = nasm
        self.parser = Parser(nasm)
        self.code = Code()
        self.hackLineCount = 0

    # DONE
    def run(self):
        try:
            self.fillSymbolTable()
            self.generateMachineCode()
            return 0
        except:
            print(f"--> ERRO AO TRADUZIR: {self.parser.currentLine}")
            return -1

    def fillSymbolTable(self):
        """
        primeiro passo para a construção da tabela de símbolos de marcadores (labels)
        varre o código em busca de novos Labels e Endereços de memórias (variáveis)
        e atualiza a tabela de símbolos com os endereços (table).

        Dependencia : Parser, SymbolTable
        """
        self.parser.reset()
        self.hackLineCount = 0
        numb_of_jumps_no_nop = 0
        num_of_leaw_d = 0
        last_command = ['a']
        while self.parser.advanced():
            if last_command[0][0] == 'j' and self.parser.currentCommand[0] != 'nop':
                numb_of_jumps_no_nop += 1
            
            if self.parser.currentCommand[0] == 'leaw' and self.parser.currentCommand[2] == '%D':
                num_of_leaw_d += 1

            if self.parser.commandType() == 'L_COMMAND':
                if not self.symbolTable.contains(self.parser.label()):
                    self.symbolTable.addEntry(self.parser.label(), self.hackLineCount + numb_of_jumps_no_nop + num_of_leaw_d)
            else:
                self.hackLineCount += 1
            last_command = self.parser.currentCommand


    def generateMachineCode(self):
        """
        Segundo passo para a geração do código de máquina
        Varre o código em busca de instruções do tipo A, C
        gerando a linguagem de máquina a partir do parse das instruções.

        Dependencias : Parser, Code
        """
        allStrings = ''
        string = ''
        self.parser.reset()
        last_command = ['a']

        while self.parser.advanced():
            cmnd = self.parser.currentCommand[0]            


            if self.parser.commandType() == "A_COMMAND":
                symbol = self.parser.symbol()
                try:
                    symbol = int(symbol)
                except:
                    symbol = self.symbolTable.getAddress(symbol)
                bin = '00' + self.code.toBinary(symbol)
                string = str(bin + "\n")
                allStrings += string
                if self.parser.currentCommand[2] == '%D':
                        allStrings += '100001100000010000\n'
            elif self.parser.commandType() == "L_COMMAND":
                pass

            elif cmnd[0] == 'j':
                bin = '100000011000000' + self.code.jump(self.parser.currentCommand)
                string = str(bin + "\n")
                allStrings += string
                allStrings += '100001010100000000\n'

            elif cmnd == 'nop' and last_command[0] != 'j':
                allStrings += '100001010100000000\n'
            
            elif cmnd == 'nop' and last_command[0] == 'j':
                pass

            elif self.parser.commandType() == "C_COMMAND":
                bin = "1000" + self.code.comp(self.parser.command()) + '0' + self.code.dest(self.parser.currentCommand) + '000'
                string = str(bin + "\n")
                allStrings += string
            else: 
                allStrings += f'{self.parser.command()} <------------- erro \n'

            last_command = cmnd
        
        self.hack.write(allStrings)

