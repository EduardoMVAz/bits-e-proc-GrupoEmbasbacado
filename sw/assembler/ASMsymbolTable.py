

class SymbolTable:
    # DONE
    def __init__(self):
        self.table = {}
        self.init()

    # TODO
    def init(self):
        """
        Inicializa a tabela de simbolos com os simbolos pre definidos
        exemplo: R0, R1, ...
        SP, LCL, ARG, THIS, THAT
        SCREEN, KBD, ..
        """

        self.table = {
        'R0':0,
        'R1':1,
        'R2':2,
        'R3':3,
        'R4':4,
        'R5':5,
        'R6':6,
        'R7':7,
        'R8':8,
        'R9':9,
        'R10':10,
        'R11':11,
        'R12':12,
        'R13':13,
        'R14':14,
        'R15':15,
        'SP':0,
        'LCL':1,
        'ARG':2,
        'THIS':3,
        'THAT':4,
        'SCREEN':16384,
        'LED':21184,
        'SW':21185,
        'KBD':24576
        }

    # TODO
    def addEntry(self, symbol: str, address: int):
        """
        Insere uma entrada de um símbolo com seu endereço numérico na tabela de símbolos (self.table).
        @param symbol símbolo a ser armazenado na tabela de símbolos.
        @param address símbolo a ser armazenado na tabela de símbolos.
        """
        pass

    # TODO
    def contains(self, symbol):
        """
        Confere se o símbolo informado já foi inserido na tabela de símbolos.
        @param  symbol símbolo a ser procurado na tabela de símbolos.
        @return Verdadeiro se símbolo está na tabela de símbolos, Falso se não está na tabela de símbolos.
        """
        pass

    # TODO
    def getAddress(self, symbol):
        """
        Retorna o valor númerico associado a um símbolo já inserido na tabela de símbolos.
        @param  symbol símbolo a ser procurado na tabela de símbolos.
        @return valor numérico associado ao símbolo procurado.
        """
        pass
