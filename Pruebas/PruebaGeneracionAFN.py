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
    afn,mensaje = GeneradorAFN.generarAFNDePostfija(ER.getExpresionPostfija(),ER.getAlfabeto())

    print(mensaje)
    if afn != -1:
        n,mensaje2 = afn.renombreAutomaticoEstados('e')

        print(mensaje2)

        afn.imprimirAutomataConsola()
        afn.imprimirAutomata()
else:
    print('Error' + mensaje)
