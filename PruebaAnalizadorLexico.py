from Automatas import *
from GeneradorAutomatas import *
from AnalizadorLexico import *
from AnalizadorSintactico import *
import sys

cadena = sys.argv[1]

generador = GeneradorAFN()

tabular = ManejadorTabulares.recuperarTabular('TabularER.dat')

#ManejadorTabulares.imprimirTablaConsola(tabular)

afdER = ManejadorTabulares.generarAFDDeTabular(tabular)

lexico = AnalizadorLexico(afdER, cadena)

sintactico = AnalizadorSintacticoER(lexico)

afn = AFN('ERPrueba')
valido = sintactico.analizar(afn)

if valido:
	afn.imprimirAutomata()
else:
	print('No es válido')