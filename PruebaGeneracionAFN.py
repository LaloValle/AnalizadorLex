from Automatas import *
from ExpresionRegular import *
from GeneradorAutomatas import *
import sys

expresion = sys.argv[1]

ER = ExpresionRegular(expresion)
ER.reconocerAlfabeto()
error, mensaje = ER.conversionAPostfija()

print(ER.getExpresionPostfija())

if error != -1:
	afn = GeneradorAFN.generarAFNDePostfija(ER.getExpresionPostfija(),ER.getAlfabeto())
	if afn != -1:
		afn.imprimirAutomataConsola()
	else:
		print('Error en el Automata')
else:
	print('Error' + mensaje)
