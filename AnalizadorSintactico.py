from AnalizadorLexico import *
from GeneradorAutomatas import GeneradorAFN

class AnalizadorSintactico():

    def __init__(self, lexico):
        self._lexico = lexico
        self._generador = GeneradorAFN()

    def E(afn):
        if T(afn):
            if Ep(afn):
                return True

        return False

    def Ep(afn):
        token = self._lexico.getToken()
        afn2 = AFN('AFN2')

        if token == Token.UNION:
            if T(afn2):
                afn = generador._generarUnion([afn,afn2])

                if Ep(afn):
                    return True
            return False

        self._lexico.rewind()
        return True

    def T(afn):
        if C(afn):
            if Tp(afn):
                return True

        return False

    def Tp(afn):
        token = self._lexico.getToken()
        afn2 = AFN('AFN2')

        if token == Token.CONCATENACION:
            if C(afn2):
                afn = generador._generarConcatenacion([afn,afn2])

                if Tp(afn):
                    return True
            return False

        self._lexico.rewind()
        return True

    def C(afn):
        if F(afn):
            if Cp(afn):
                return True
        return False

    def Cp(afn):
        token = self._lexico.getToken()

        if token == Token.CERRADURA_POSITIVA:
            afn = generador._generarCerraduraPositiva([afn])

            if Cp(afn):
                return True
            return False

        elif token == Token.CERRADURA_KLEENE:
            afn = generador._generarCerraduraKleene([afn])

            if Cp(afn):
                return True
            return False

        elif token == Token.OPCIONAL:
            afn = generador._generarOpcional([afn])

            if Cp(afn):
                return True
            return False

        self._lexico.rewind()
        return True

    def F(afn):
        token = self._lexico.getToken()

        if token == Token.PARENTESIS_IZQUIERDO:
            if E(afn):
                token = self._lexico.getToken()
                
                if token == Token.PARENTESIS_DERECHO:
                    return True

            return False

        elif token == Token.BACK_SLASH:
            token = self._lexico.getToken()

            if token in (Token.UNION,Token.CONCATENACION,Token.CERRADURA_POSITIVA,Token.CERRADURA_KLEENE,Token.OPCIONAL):
                afn = self._generador._generarAutomata('\\{}'.format(self._lexico.getUltimoLexema()))
                return True
            return False

        elif token == Token.SIMBOLO:
            afn = self._generador._generarAutomata(self._lexico.getUltimoLexema())
            return True

        self._lexico.rewind()
        return True
