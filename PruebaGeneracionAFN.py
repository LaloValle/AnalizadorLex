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

        #Probamos la función mover
        generadorAFD = GeneradorAFD()

        conjunto = generadorAFD._cerraduraEpsilon({afn.getEstadoInicial()})

        conjunto2 = generadorAFD._irA(set(conjunto), 'a')

        print('>>>>>> Cerradura epsilon S0')

        while len(conjunto) > 0:
        	print(conjunto.pop().getNombre())

        print('>>>>>> IrA de S0')

        while len(conjunto2) > 0:
        	print(conjunto2.pop().getNombre())

        afnAux = afn

        afd = GeneradorAFD.generarAFDDeAFN(afnAux)

        afd.imprimirAutomata()

else:
    print('Error' + mensaje)
