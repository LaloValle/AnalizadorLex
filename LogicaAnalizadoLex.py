from GeneradorAutomatas import *
from ExpresionRegular import *

class LogicaAnalizadorLex():

	def __init__(self, vista):

		self._vista = vista

		self._automatasGuardados = [None, None, None]

	def opcionGenerarDeER(self, tipoAutomata, expresion, guardado):
		if tipoAutomata == 'AFN':
			ER = ExpresionRegular(expresion)
			ER.reconocerAlfabeto()
			error, mensaje = ER.conversionAPostfija()

			if error != -1:
			    afn,mensaje = GeneradorAFN.generarAFNDePostfija(ER.getExpresionPostfija(),ER.getAlfabeto())

			    if afn != -1:
			        n,mensaje2 = afn.renombreAutomaticoEstados('e')

			        if n >= 0:
				        afn.imprimirAutomata()

				        self._automatasGuardados[guardado] = afn
			else:
			    print('Error' + mensaje)

		else:
			print('Aún no se ha implementado la generación de los AFD')

	def operacionAFN(self, operacion):
		
		generador = GeneradorAFN()
		operaciones = {'α':[1] , '|':[2,generador._generarUnion], '°':[2,generador._generarConcatenacion], '⁺':[1,generador._generarCerraduraPositiva],'*':[1,generador._generarCerraduraKleene], '?':[1,generador._generarOpcional]}

		automata1 = None
		automata2 = None
		automataResultado = None

		if self._vista.getAFNSimbolo1() != '':
			automata1 = generador._generarAutomata(self._vista.getAFNSimbolo1())

			if operaciones[operacion][0] > 1:
				#Operación con 2 símbolos
				if self._vista.getAFNSimbolo2() != '':
					automata2 = generador._generarAutomata(self._vista.getAFNSimbolo2())

				elif self._vista.getAFNGuardadoCargado1() != '':
					#Se busca la opción del 1° autómata guardado
					automata2 = self._automatasGuardados[self._vista.getAFNGuardadoCargado1()]

					if  automata2 == None:
						print('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
						return -1

				else:
					print('Se ha escogido realizar una operación que necesitas dos elementos y solo se ha cargado 1')
					return -1

		elif self._vista.getAFNGuardadoCargado1() >= 0:
			if operacion != 'α':
				automata1 = self._automatasGuardados[self._vista.getAFNGuardadoCargado1()]

				if automata1 != None:
					if operaciones[operacion][0] > 1:
						#Se tiene una operación con 2 elementos
						if self._vista.getAFNGuardadoCargado2() >= 0:
							automata2 = self._automatasGuardados[self._vista.getAFNGuardadoCargado2()]

							if  automata2 == None:
								print('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
								return -1

						else:
							print('Se ha escogido realizar una operación que necesita 2 autómatas, pero solo se ha escogido 1')
							return -1

				else:
					print('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
					return -1

			else:
				print('No se puede realizar la operación de autómata básico en un autómata ya creado')
				return -1

		else:
			print('No se ha ingresado o escogido un autómata para realizar la operación')
			return -1


		if operacion != 'α':
			automataResultado = operaciones[operacion][1]([automata1, automata2])
		else:
			automataResultado = automata1

		automataResultado.renombreAutomaticoEstados('e')

		if self._vista.getAFNguardadoSeleccionado() >= 0:
			self._automatasGuardados[self._vista.getAFNguardadoSeleccionado()] = automataResultado
		else:
			print('Solo se imprimirá el autómata resultado de la operación elegida, no se eligió un espacio donde guardarlo')

		automataResultado.imprimirAutomata()

	def opcionGraficar(self, seleccion):
		if self._automatasGuardados[seleccion] != None:
			self._automatasGuardados[seleccion].imprimirAutomata()
		else:
			print('El elemento de la lista de autómatas está vacío')