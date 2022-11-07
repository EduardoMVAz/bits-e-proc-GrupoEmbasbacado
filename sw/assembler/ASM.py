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

    # TODO
    def fillSymbolTable(self):
        """
        primeiro passo para a construção da tabela de símbolos de marcadores (labels)
        varre o código em busca de novos Labels e Endereços de memórias (variáveis)
        e atualiza a tabela de símbolos com os endereços (table).

        Dependencia : Parser, SymbolTable
        """
        self.hackLineCount = 0
        while self.parser.advanced():
            if self.parser.commandType() == 'L_COMMAND':
                if not self.symbolTable.contains(self.parser.label()):
                    self.symbolTable.addEntry(self.parser.label(), self.hackLineCount)
            else:
                self.hackLineCount += 1


    # TODO
    def generateMachineCode(self):
        """  
        
        Segundo passo para a geração do código de máquina
        Varre o código em busca de instruções do tipo A, C
        gerando a linguagem de máquina a partir do parse das instruções.

        Dependencias : Parser, Code
        """
        allStrings = ''
        string = ''
        self.parser.lineNumber = 0
        self.parser.currentCommand = ''
        self.parser.file = open('test_assets/factorial.nasm', 'r')

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

            elif cmnd == 'nop':
                allStrings += '100001010100000000\n'
                
            elif self.parser.commandType() == "L_COMMAND":
                pass # for tags

            elif cmnd[0] == 'j':
                bin = '100000011000000' + self.code.jump(self.parser.currentCommand)
                string = str(bin + "\n")
                allStrings += string
            
            elif self.parser.commandType() == "C_COMMAND":
                bin = "1000" + self.code.comp(self.parser.command()) + '0' + self.code.dest(self.parser.currentCommand) + '000'
                string = str(bin + "\n")
                allStrings += string

            else: 
                allStrings += f'{self.parser.command()} <------------- erro \n'
                    
        self.hack.write(allStrings)
            
NASM_IN = 'test_assets/factorial.nasm'
HACK_OUT = 'test_assets/factorial_out.hack'
HACK_REF = 'test_assets/factorial.hack'
fNasm = open(NASM_IN, 'r')
fHack = open(HACK_OUT, 'w')
asm = ASM(fNasm, fHack)
asm.run()
fHack.close()