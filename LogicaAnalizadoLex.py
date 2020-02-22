from GeneradorAutomatas import *
from ExpresionRegular import *

class LogicaAnalizadorLex():

	def __init__(self, vista):

		self._vista = vista

		self._automatasGuardados = [None, None, None]

		#Creación del autómata transiciones epsilon
		self._automataTransicionesEpsilon = AFN('Automata Transiciones ε')
		self._automataTransicionesEpsilon.agregarEstado(Estado('Sε',{},False,True)) 

	def getAutomataGuardado(self, indice):
		return self._automatasGuardados[indice] if indice < 3 else self._automataTransicionesEpsilon

	def _agregarAutomataTransicionesEpsilon(self, automata):
		type(automata)
		estadoInicial = automata.getEstadoInicial()
		estadoInicial.setInicial(False)

		self._automataTransicionesEpsilon.getEstadoInicial().agregarTransicion('ε',[estadoInicial])
		self._automataTransicionesEpsilon.agregarEstados(automata.getEstados())

		self._automataTransicionesEpsilon.setAlfabeto(self._automataTransicionesEpsilon.getAlfabeto()+automata.getAlfabeto())

		return 0


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

	def operacionAFN(self, operacion, token):
		
		generador = GeneradorAFN()
		operaciones = {'α':[1] , '|':[2,generador._generarUnion], '°':[2,generador._generarConcatenacion], '⁺':[1,generador._generarCerraduraPositiva],'*':[1,generador._generarCerraduraKleene], '?':[1,generador._generarOpcional]}

		automata1 = None
		automata2 = None
		automataResultado = None

		alfabetoAux = []

		if self._vista.getAFNSimbolo1() != '':
			automata1 = generador._generarAutomata(self._vista.getAFNSimbolo1())

			alfabetoAux.append(self._vista.getAFNSimbolo1())

			if operaciones[operacion][0] > 1:
				#Operación con 2 símbolos
				if self._vista.getAFNSimbolo2() != '':
					automata2 = generador._generarAutomata(self._vista.getAFNSimbolo2())

					alfabetoAux.append(self._vista.getAFNSimbolo2())

				elif self._vista.getAFNGuardadoCargado1() != '':
					#Se busca la opción del 1° autómata guardado
					automata2 = self._automatasGuardados[self._vista.getAFNGuardadoCargado1()]

					self._automatasGuardados[self._vista.getAFNGuardadoCargado1()] = None

					if  automata2 == None:
						self._vista.mostrarAdvertencia('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
						return -1

					alfabetoAux += automata2.getAlfabeto()

				else:
					self._vista.mostrarAdvertencia('Se ha escogido realizar una operación que necesitas dos elementos y solo se ha cargado 1')
					return -1

		elif self._vista.getAFNGuardadoCargado1() >= 0:
			if operacion != 'α':
				automata1 = self._automatasGuardados[self._vista.getAFNGuardadoCargado1()]

				if automata1 != None:
					alfabetoAux = automata1.getAlfabeto()

					if operaciones[operacion][0] > 1:
						#Se tiene una operación con 2 elementos
						if self._vista.getAFNGuardadoCargado2() >= 0:
							automata2 = self._automatasGuardados[self._vista.getAFNGuardadoCargado2()]

							if  automata2 == None:
								self._vista.mostrarAdvertencia('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
								return -1

							else:
								alfabetoAux += automata2.getAlfabeto()

								self._automatasGuardados[self._vista.getAFNGuardadoCargado1()] = None
								self._automatasGuardados[self._vista.getAFNGuardadoCargado2()] = None

						else:
							self._vista.mostrarAdvertencia('Se ha escogido realizar una operación que necesita 2 autómatas, pero solo se ha escogido 1')
							return -1

				else:
					self._vista.mostrarAdvertencia('Se ha elegido utilizar un elemento de los autómatas guardados pero el elemento escogido está vacío')
					return -1

			else:
				self._vista.mostrarAdvertencia('No se puede realizar la operación de autómata básico en un autómata ya creado')
				return -1

		else:
			self._vista.mostrarAdvertencia('No se ha ingresado o escogido un autómata para realizar la operación')
			return -1

		if token == '':
			self._vista.mostrarAdvertencia('Debe ser ingresado un valor de token para crear el autómata')
			return -1

		else:
			token = int(token)

			if token > 0:

				if operacion != 'α':
					automataResultado = operaciones[operacion][1]([automata1, automata2])
				else:
					automataResultado = automata1

				automataResultado.setAlfabeto(alfabetoAux)

				automataResultado.renombreAutomaticoEstados('e')

				if self._vista.getAFNguardadoSeleccionado() >= 0:
					self._automatasGuardados[self._vista.getAFNguardadoSeleccionado()] = automataResultado
				else:
					self._vista.mostrarInformacion('Solo se imprimirá el autómata resultado de la operación elegida, no se eligió un espacio donde guardarlo')

				automataResultado.getEstadosAceptacion()[0].setToken(token)
				automataResultado.imprimirAutomata()

			else:
				self._vista.mostrarAdvertencia('El token no puede ser un valor negativo ni igual a cero')
				return -1

	def operacionAFD(self, operacion, cadenaAutomataGuardado):
		generador = GeneradorAFD()
		operaciones = {'cerradura':[2, generador._cerraduraEpsilon] , 'mover':[3,generador._mover], 'irA':[3,generador._irA], 'añadir a automata':[1,self._agregarAutomataTransicionesEpsilon], 'transformar':[1, generador.generarAFDDeAFN]}

		"""automata1 = None
		automata2 = None
		automataResultado = None"""
		automata = None
		resultado = None

		guardadoSeleccionado = self._vista.getAFDGuardadoSeleccionado()
		if cadenaAutomataGuardado != '':
			if cadenaAutomataGuardado == 'ε':
				automata = self._automataTransicionesEpsilon

			else:
				numAutomata = cadenaAutomataGuardado[-1]

				if numAutomata == 'ε':
					automata = self._automataTransicionesEpsilon

				else:
					numAutomata = int(numAutomata) -1

					automata = self._automatasGuardados[numAutomata]
			
			if automata != None:
				if operaciones[operacion][0] > 1:
					#Se debe de obtener el valor del estado y/o símbolo
					simbolo = self._vista.getAFDSimbolo()
					estado = None

					if self._vista.getAFDEstadoSeleccionado()  != '':
						for estadoAux in automata.getEstados():
							if estadoAux.getNombre() == self._vista.getAFDEstadoSeleccionado():
								estado = estadoAux
								break

					else:
						if type(automata) == AFN or type(automata) == AFD:
							self._vista.mostrarAdvertencia('Es necesario para la realización de la operación la elección de un estado del autómata')
							return -1

					if operaciones[operacion][0] == 2:
						resultado = operaciones[operacion][1]([estado] if type(automata) != set else set(automata))

					else:
						resultado = operaciones[operacion][1]([estado] if type(automata) != set else set(automata),simbolo)

				else:
					#Se trata de añadir al automata transiciones epsilon o la transformación de un AFN a AFD
					resultado = operaciones[operacion][1](automata)

			else:
				self._vista.mostrarAdvertencia('El elemento seleccionado para los autómatas guardados esta vacío')
				return -1
		else:
			self._vista.mostrarAdvertencia('Debe ser ingresado un valor de token para crear el autómata')
			print('No se ha seleccionado ningún elemento de los autómatas guardados')
			return -1

		if operacion == 'añadir a automata':
			self._automatasGuardados[numAutomata] = None

			self._automataTransicionesEpsilon.renombreAutomaticoEstados('S')

			self._vista.mostrarInformacion('Se ha agregado exitosamente el autómata')

		else:
			if guardadoSeleccionado >= 0:
				self._automatasGuardados[guardadoSeleccionado] = set(resultado) if type(resultado) != AFD else resultado

				self._vista.mostrarInformacion('Se ha generado exitosamente el conjunto' if type(resultado) != AFD else 'Se ha transformado el autómata exitosamente')
			else:
				self._vista.mostrarAdvertencia('No se guardará el conjunto de estados resultado de la operación realizada pues no se seleccionó ningún elemento donde guardarlo')

		if resultado != None:
			if type(resultado) == set:
				resultado = set(resultado)
				generador._imprimirConjuntoEstados(resultado)

		
	def opcionGraficar(self, seleccion):
		if seleccion == 'ε':
			self._automataTransicionesEpsilon.imprimirAutomata()

		else:
			seleccion = int(seleccion) - 1
			seleccionado = self._automatasGuardados[seleccion]
			
			if seleccionado != None:
				if type(seleccionado) != set:
					seleccionado.imprimirAutomata()

				else:
					self._vista.mostrarInformacion(GeneradorAFD()._imprimirConjuntoEstados(set(seleccionado)))

			else:
				self._vista.mostrarAdvertencia('El elemento de la lista de autómatas está vacío')
				return -1
