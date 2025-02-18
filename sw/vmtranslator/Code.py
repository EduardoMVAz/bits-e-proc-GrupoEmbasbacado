#!/usr/bin/env python3
import io
import os
import queue
import uuid


class Code:
    def __init__(self, outFile):
        self.outFile = outFile
        self.counter = 0
        self.vmFileName = None
        self.labelCounter = 0

    # DONE
    def close(self):
        self.outFile.close()

    # DONE
    def updateVmFileName(self, name):
        self.vmFileName = os.path.basename(name).split(".")[0]

    # DONE
    def commandsToFile(self, commands):
        for line in commands:
            self.outFile.write(f"{line}\n")

    # DONE
    def getUniqLabel(self):
        return self.vmFileName + str(self.labelCounter)

    # DONE
    def updateUniqLabel(self):
        self.labelCounter = self.labelCounter + 1

    # DONE
    def writeHead(self, command):
        self.counter = self.counter + 1
        return ";; " + command + " - " + str(self.counter)

    # DONE
    def writeInit(self, bootstrap, isDir):
        commands = []

        if bootstrap or isDir:
            commands.append(self.writeHead("init"))

        if bootstrap:
            commands.append("leaw $256,%A")
            commands.append("movw %A,%D")
            commands.append("leaw $SP,%A")
            commands.append("movw %D,(%A)")

        if isDir:
            commands.append("leaw $Main.main, %A")
            commands.append("jmp")
            commands.append("nop")

        if bootstrap or isDir:
            self.commandsToFile(commands)

    # TODO
    def writeLabel(self, label):
        commands = []
        commands.append(self.writeHead("label") + " " + label)

        commands.append(f"{label}:")
        self.commandsToFile(commands)

    # TODO
    def writeGoto(self, label):
        commands = []
        commands.append(self.writeHead("goto") + " " + label)

        commands.append(f'leaw ${label}, %A')
        commands.append('jmp')
        commands.append('nop')
        self.commandsToFile(commands)

    # TODO
    def writeIf(self, label):
        commands = []
        commands.append(self.writeHead("if") + " " + label)

        commands.append("leaw $SP, %A") 
        commands.append("subw (%A), $1, %D")
        commands.append('movw %D, (%A)')

        commands.append('movw %D, %A')
        commands.append('movw (%A), %D')
        commands.append("notw %D") 

        commands.append(f'leaw ${label}, %A')
        commands.append('je')
        commands.append('nop')

        self.commandsToFile(commands)

    # TODO
    def writeArithmetic(self, command):
        self.updateUniqLabel()
        if len(command) < 2:
            print("instrucão invalida {}".format(command))
        commands = []
        commands.append(self.writeHead(command))

        if command == "add":

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('addw (%A), %D, %D')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif command == "sub":

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('subw (%A), %D, %D')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif command == "or":

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('orw (%A), %D, %D')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif command == "and":

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('andw (%A), %D, %D')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif command == "not":
            
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('notw %D')
            commands.append('movw %D, (%A)')

        elif command == "neg":

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('notw %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif command == "eq":
            # dica, usar self.getUniqLabel() para obter um label único

            label_igual_zero = self.getUniqLabel()
            self.updateUniqLabel()
            label_diferente_zero = self.getUniqLabel()
            self.updateUniqLabel()
            label_end = self.getUniqLabel()

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('subw (%A), %D, %D')
            commands.append(f'leaw ${label_igual_zero}, %A')
            commands.append('je')
            commands.append('nop')
            commands.append(f'leaw ${label_diferente_zero}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_igual_zero}:')
            commands.append('leaw $65535, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')
            commands.append(f'leaw ${label_end}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_diferente_zero}:')
            commands.append('leaw $0, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

            commands.append(f'{label_end}:')

        elif command == "gt":
            # dica, usar self.getUniqLabel() para obter um label único

            label_maior = self.getUniqLabel()
            self.updateUniqLabel()
            label_outro = self.getUniqLabel()
            self.updateUniqLabel()
            label_end = self.getUniqLabel()

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('subw (%A), %D, %D')
            commands.append(f'leaw ${label_maior}, %A')
            commands.append('jg')
            commands.append('nop')
            commands.append(f'leaw ${label_outro}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_maior}:')
            commands.append('leaw $65535, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')
            commands.append(f'leaw ${label_end}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_outro}:')
            commands.append('leaw $0, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

            commands.append(f'{label_end}:')
            
        elif command == "lt":
            # dica, usar self.getUniqLabel() para obter um label único
            
            label_menor = self.getUniqLabel()
            self.updateUniqLabel()
            label_outro = self.getUniqLabel()
            self.updateUniqLabel()
            label_end = self.getUniqLabel()
            
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('decw %A')
            commands.append('subw (%A), %D, %D')
            commands.append(f'leaw ${label_menor}, %A')
            commands.append('jl')
            commands.append('nop')
            commands.append(f'leaw ${label_outro}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_menor}:')
            commands.append('leaw $65535, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')
            commands.append(f'leaw ${label_end}, %A')
            commands.append('jmp')
            commands.append('nop')

            commands.append(f'{label_outro}:')
            commands.append('leaw $0, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('decw %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

            commands.append(f'{label_end}:')

        self.commandsToFile(commands)

    def writePop(self, command, segment, index):
        self.updateUniqLabel()
        commands = []
        commands.append(self.writeHead(command) + " " + segment + " " + str(index))

        if segment == "" or segment == "constant":
            return False
        elif segment == "local":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $LCL, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "argument":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $ARG, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "this":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $THIS, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "that":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $THAT, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "temp":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $5, %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "static":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $STATIC, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %D, %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('decw %A')
            commands.append('movw (%A), %D')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('decw %D')
            commands.append('movw %D, (%A)')

        elif segment == "pointer":
            if index == 0:
                commands.append("leaw $SP, %A")
                commands.append("movw (%A), %A")
                commands.append("decw %A")
                commands.append("movw (%A), %D")
                commands.append("leaw $THIS, %A")
                commands.append("movw %D, (%A)")
                commands.append("leaw $SP, %A")
                commands.append("movw (%A), %D")
                commands.append("decw %D")
                commands.append("movw %D, (%A)")
            elif index == 1:
                commands.append("leaw $SP, %A")
                commands.append("movw (%A), %A")
                commands.append("decw %A")
                commands.append("movw (%A), %D")
                commands.append("leaw $THAT, %A")
                commands.append("movw %D, (%A)")
                commands.append("leaw $SP, %A")
                commands.append("movw (%A), %D")
                commands.append("decw %D")
                commands.append("movw %D, (%A)")

        self.commandsToFile(commands)

    def writePush(self, command, segment, index):
        commands = []
        commands.append(self.writeHead(command + " " + segment + " " + str(index)))

        if segment == "constant":
            # dica: usar index para saber o valor da consante
            # push constant index
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D') 
            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A') 
            commands.append('movw %D, (%A)')
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif segment == "local":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $LCL, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D') 

            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif segment == "argument":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $ARG, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D') 

            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')
            
            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif segment == "this":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $THIS, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D') 

            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif segment == "that":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $THAT, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D') 

            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif segment == "static": #N TEM TESTE LOGO N SEI
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $STATIC, %A')
            commands.append('movw (%A), %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D') 

            commands.append('leaw $SP, %A') 
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %D')
            commands.append('incw %D')
            commands.append('movw %D, (%A)')

        elif segment == "temp":
            commands.append(f'leaw ${index}, %A')
            commands.append('movw %A, %D')
            commands.append('leaw $5, %A')
            commands.append('addw %A, %D, %A')
            commands.append('movw (%A), %D')

            commands.append('leaw $SP, %A')
            commands.append('movw (%A), %A')
            commands.append('movw %D, (%A)')
            commands.append('incw %A')
            commands.append('movw %A, %D')
            commands.append('leaw $SP, %A')
            commands.append('movw %D, (%A)')

        elif segment == "pointer": #resolver o SP 
            if index == 0:
                commands.append('leaw $THIS, %A')
                commands.append('movw (%A), %D')
                commands.append('leaw $SP, %A')
                commands.append('movw (%A), %A')
                commands.append('movw %D, (%A)')
                commands.append('incw %A')
                commands.append('movw %A, %D')
                commands.append('leaw $SP, %A')
                commands.append('movw %D, (%A)')
            elif index == 1:
                commands.append('leaw $THAT, %A')
                commands.append('movw (%A), %D')
                commands.append('leaw $SP, %A')
                commands.append('movw (%A), %A')
                commands.append('movw %D, (%A)')
                commands.append('incw %A')
                commands.append('movw %A, %D')
                commands.append('leaw $SP, %A')
                commands.append('movw %D, (%A)')

        self.commandsToFile(commands)

    # TODO
    def writeCall(self, funcName, numArgs):
        commands = []
        commands.append(self.writeHead("call") + " " + funcName + " " + str(numArgs))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeReturn(self):
        commands = []
        commands.append(self.writeHead("return"))

        # TODO
        # ...

        self.commandsToFile(commands)

    # TODO
    def writeFunction(self, funcName, numLocals):
        commands = []
        commands.append(self.writeHead("func") + " " + funcName + " " + str(numLocals))

        # TODO
        # ...

        self.commandsToFile(commands)
