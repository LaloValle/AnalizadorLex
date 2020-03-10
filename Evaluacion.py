from GeneradorAutomatas import *
from AnalizadorLexico import *
from Automatas import *
from tabulate import *

import sys

#Se obtiene la cadena a analizar
cadena = sys.argv[1]

tablaAnalisis = [['Lexema','Token']]

#Se obtiene la tabla del autómata
tabularEvaluacion = ManejadorTabulares.recuperarTabular('Evaluación/AutomataEvaluacion.dat')
ManejadorTabulares.imprimirTablaConsola(tabularEvaluacion)

#Se genera el autómata a partir de la tabla
afdEvaluacion = ManejadorTabulares.generarAFDDeTabular(tabularEvaluacion)
afdEvaluacion.imprimirAutomata()

#Instancia de la Clase AnalizadorLexico
lexico = AnalizadorLexico(afdEvaluacion, cadena)
#Se obtiene el análisis léxico
token = 100
while token > 0:
	token = lexico.getToken()

	if token > 0:
		filaAnalisis = [lexico.getUltimoLexemaValido(),token]
		tablaAnalisis.append(filaAnalisis)

#Se imprimen los resultados
print(tabulate(tablaAnalisis, headers='firstrow', tablefmt='psql'))


if token < 0:
	print('ERROR>> Se ha encontrador un error en la cadena con índice {} y lexema no válido {}'.format(lexico.getIndiceCadena() ,lexico.getUltimoLexema()))