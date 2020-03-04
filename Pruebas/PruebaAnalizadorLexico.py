from Automatas import *
from GeneradorAutomatas import *
from AnalizadorLexico import *
import sys

cadena = sys.argv[1]

generador = GeneradorAFN()

tabular = ManejadorTabulares.recuperarTabular('AutomataER.dat')
ManejadorTabulares.imprimirTablaConsola(tabular)

afdER = ManejadorTabulares.generarAFDDeTabular(tabular)

afdER.imprimirAutomata()

lexico = AnalizadorLexico(afdER, cadena)

token = 100
while token > 0:
	token = lexico.getToken()
	print(str(token) + ':' + lexico.getUltimoLexema())