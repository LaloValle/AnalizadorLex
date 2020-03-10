from AnalizadorLexico import *
from GeneradorAutomatas import GeneradorAFN

class AnalizadorSintacticoER():

    def __init__(self, lexico):
        self._lexico = lexico
        self._generador = GeneradorAFN()

    def analizar(self,afn):
        analisisValido = self.E(afn)

        if analisisValido:
            #Se verifica que todos los caracteres de la cadena hayan sido analizados
            if self._lexico.getToken() != 0:
                analisisValido = False

        return analisisValido

    def E(self,afn):
        if self.T(afn):
            if self.Ep(afn):
                return True
        return False

    def Ep(self,afn):
        token = self._lexico.getToken()
        afn2 = AFN('AFN2')

        if token >= 0:
            if token == TokenER.UNION:
                if self.T(afn2):
                    afn.automata(self._generador._generarUnion([afn,afn2]))

                    if self.Ep(afn):
                        return True
                return False

        else:
            return False

        if token > 0:
            self._lexico.rewind()
        return True

    def T(self,afn):
        if self.C(afn):
            if self.Tp(afn):
                return True

        return False

    def Tp(self,afn):
        token = self._lexico.getToken()
        afn2 = AFN('AFN2')

        if token >= 0:
            if token == TokenER.CONCATENACION:
                if self.C(afn2):
                    afn.automata(self._generador._generarConcatenacion([afn,afn2]))

                    if self.Tp(afn):
                        return True
                return False
        else:
            return False

        if token > 0:
            self._lexico.rewind()
        return True

    def C(self,afn):
        if self.F(afn):
            if self.Cp(afn):
                return True
        return False

    def Cp(self,afn):
        token = self._lexico.getToken()

        if token >= 0:
            if token == TokenER.CERRADURA_POSITIVA:
                afn.automata(self._generador._generarCerraduraPositiva([afn]))

                if self.Cp(afn):
                    return True
                return False

            elif token == TokenER.CERRADURA_KLEENE:
                afn.automata(self._generador._generarCerraduraKleene([afn]))

                if self.Cp(afn):
                    return True
                return False

            elif token == TokenER.OPCIONAL:
                afn.automata(self._generador._generarOpcional([afn]))

                if self.Cp(afn):
                    return True
                return False

        else:
            return False

        if token > 0:
            self._lexico.rewind()
        return True

    def F(self,afn):
        token = self._lexico.getToken()

        if token >= 0:
            if token == TokenER.PARENTESIS_IZQUIERDO:
                if self.E(afn):
                    token = self._lexico.getToken()
                    
                    if token == TokenER.PARENTESIS_DERECHO:
                        return True

                return False

            elif token == TokenER.SIMBOLO:
                afn.automata(self._generador._generarAutomata(self._lexico.getUltimoLexemaValido()))
                return True
                
        else:
            return False

        self._lexico.rewind()
        return True

class TokenER(object):

    #Constantes referentes a los token de las ER
    UNION = 10

    CONCATENACION = 20

    CERRADURA_POSITIVA = 30

    CERRADURA_KLEENE = 40

    OPCIONAL = 50

    SIMBOLO = 60

    PARENTESIS_IZQUIERDO = 70

    PARENTESIS_DERECHO = 71