from Automatas import *

"""
	Para la instalación de graphviz:

	Ubuntu $ sudo apt install python-pydot python-pydot-ng graphviz

"""

class GeneradorAFN():

	"""

		Clase generadora de AFNs con el paso de símbolos pertenecientes al alfabeto de una expresión regular o de AFNs también generados por algún método de esta clase

	"""

	def _generarAutomata(self,simbolo):
		""" Función que genera un AFN de un símbolo dado
			@param simbolo : string
			@returns afn : AFN """
		nombre = simbolo

		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{nombre:[ef]},False,True)

		afn = AFN(nombre)
		afn.setEstados([e0,ef])

		return afn

	def _generarUnion(self,automatas):
		""" Función que genera un AFN con la operación de union para dos símbolos o dos AFN dado
			@param automatas : list
			@returns afn : AFN """

		nombre = automatas[1].getNombre() + '|' + automatas[0].getNombre()

		afn = AFN(nombre)

		#Creación de estados comunes
		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{},False,True)

		afn.agregarEstado(e0)

		for automata in automatas:
			estadoInicial = automata.getEstadoInicial()
			estadoAceptacion = automata.getEstadosAceptacion()[0]

			estadoInicial.setInicial(False)
			estadoAceptacion.setAceptacion(False)

			e0.agregarTransicion('ε',[estadoInicial])
			estadoAceptacion.agregarTransicion('ε',[ef])

			afn.agregarEstados(automata.getEstados())

		#Se agrega el estado de aceptación
		afn.agregarEstado(ef)

		return afn

	def _generarConcatenacion(self,automatas):
		""" Función que genera un AFN con la operación de concatenación para dos símbolos o dos AFN dado
			@param automatas : list
			@returns afn : AFN """

		nombre = automatas[0].getNombre() + '°' + automatas[1].getNombre()

		afn = AFN(nombre)

		#El estado final del primer autómata se convierte en el primer estado del segundo
		automatas[0].getEstadosAceptacion()[0].setTransiciones(automatas[1].getEstadoInicial().getTransiciones())

		#Se le elimina al estado de aceptación del primer automata la propiedad de ser aceptación
		automatas[0].getEstadosAceptacion()[0].setAceptacion(False)
		#Se elimina el estado inicial del segundo autómata
		automatas[1].eliminarEstado(automatas[1].getEstadoInicial())

		#Se conforma el nuevo autómata con las modificaciones realizadas
		afn.agregarEstados(automatas[0].getEstados())
		afn.agregarEstados(automatas[1].getEstados())

		return afn


	def _generarCerraduraPositiva(self,automata):
		""" Función que genera un AFN con la operación de cerradura para un símbolo o un AFN dado
			@param automata : list
			@returns afn : AFN """
		automata = automata[0]
		nombre = automata.getNombre()

		afn = AFN(nombre)

		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{},False,True)

		estadoInicial = automata.getEstadoInicial()
		estadoAceptacion = automata.getEstadosAceptacion()[0]

		estadoInicial.setInicial(False)
		estadoAceptacion.setAceptacion(False)

		estadoAceptacion.agregarTransicion('ε',[estadoInicial,ef])
		e0.agregarTransicion('ε',[estadoInicial])

		afn.agregarEstados([e0] + automata.getEstados() + [ef])

		return afn

	def _generarCerraduraKleene(self,automata):
		""" Función que genera un AFN con la operación de cerradura de Kleene para un símbolo o un AFN dado
			@param automata : list
			@returns afn : AFN """

		afn = self._generarCerraduraPositiva(automata)

		afn.getEstadoInicial().agregarTransicion('ε',[afn.getEstadosAceptacion()[0]])

		return afn

	def _generarOpcional(self,automata):
		""" Función que genera un AFN con la operación de opcional para un símbolo o un AFN dado
			@param automata : list
			@returns afn : AFN """
		automata = automata[0]
		nombre = automata.getNombre()

		afn = AFN(nombre)

		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{},False,True)

		estadoInicial = automata.getEstadoInicial()
		estadoAceptacion = automata.getEstadosAceptacion()[0]

		estadoInicial.setInicial(False)
		estadoAceptacion.setAceptacion(False)

		estadoAceptacion.agregarTransicion('ε',[ef])
		e0.agregarTransicion('ε',[estadoInicial,ef])

		#Se agregan los estados que conforman al automata antes de realizar la operación
		afn.agregarEstados([e0] + automata.getEstados() + [ef])

		return afn

	@staticmethod
	def generarAFNDePostfija(postfija, alfabeto):
		generador = GeneradorAFN()

		operaciones = {'|':[2,generador._generarUnion], '°':[2,generador._generarConcatenacion], '⁺':[1,generador._generarCerraduraPositiva],'^+':[1,generador._generarCerraduraPositiva], '*':[1,generador._generarCerraduraKleene], '?':[1,generador._generarOpcional]}

		pilaSimbolos = []
		afn = None

		for s in postfija:
			if s in operaciones:
				#Es una operación

				automatasOperar = []

				#Se obtiene los automatas que serán operados
				for _ in range(operaciones[s][0]):
					automatasOperar.append(pilaSimbolos.pop())

				if s == '|' or s == '°':
					automatasOperar.reverse()

				#Se llama la función para operar los símbolos o AFN
				pilaSimbolos.append(operaciones[s][1](automatasOperar))

			else:
				#Es un símbolo perteneciente al alfabeto
				if s in alfabeto:
					pilaSimbolos.append(generador._generarAutomata(s))
				else:
					return -1,'Símbolo no reconocido como operación ni perteneciente al alfabeto'

		if type(pilaSimbolos[-1]) == AFN and len(pilaSimbolos) == 1:
			afn = pilaSimbolos.pop()
		else:
			return -1,'El resultado de la pila no es un autómata o existen más elementos'

		afn.setAlfabeto(alfabeto)

		return afn,'Generación correcta del AFN'


class GeneradorAFD():

	"""

		Clase generadora de los AFD a partir de los estados que conforman a un AFN

	"""

	def _mover(self, estados, simbolo):
		conjuntoResultado = set()

		for _ in range(len(estados)):
			estado = estados.pop()

			conjuntoResultado |= set(estado.getEstadosTransicion(simbolo))

		return conjuntoResultado

	def _cerraduraEpsilon(self, estados):
		conjuntoResultado = set(estados)

		for _ in range(len(estados)):
			estado = estados.pop()

			auxResultado = set(estado.getEstadosTransicion('ε'))

			conjuntoResultado |= self._cerraduraEpsilon(auxResultado)

		return conjuntoResultado

	def _irA(self, estados, simbolo):
		return self._cerraduraEpsilon(self._mover(estados, simbolo))

	def _crearNuevoEstadoConvertido(self, estadosAFN, numEstado, inicial = False):
		aceptacion = False

		for auxEstado in range(len(estadosAFN)):
			if estadosAFN.pop().isAceptacion():
				aceptacion = True
				break

		return Estado('s{}'.format(str(numEstado)),{},aceptacion, inicial)

	def _imprimirConjuntoEstados(self, conjunto):
		cadena = '{'

		while len(conjunto) > 0:
			aux = conjunto.pop()
			cadena += aux.getNombre() + ','

		cadena += '}'

		return cadena


	@staticmethod
	def generarAFDDeAFN(automata):
		#La llave se refiere al conjunto de estados del AFN resultados de una operación irA, y el valor asociado el estado instancia de la clase Estado que es utilizado en el nuevo AFD
		estadosConvertidos = {}
		#La llave se refiere al conjunto de estados obtenidos de la operación mover, y el valor asociado al conjunto de estados del autómata AFN que resulta de la operación irA con dicho conjunto de la operación Mover
		resultadosMover = {}
		estadosNoAnalizados = []

		numEstado = 1

		generador = GeneradorAFD()
		afd = AFD(automata.getNombre())
		afd.setAlfabeto(automata.getAlfabeto())

		#Creación estado S0
		estadoInicial = generador._cerraduraEpsilon([automata.getEstadoInicial()])
		estadosConvertidos[frozenset(estadoInicial)] = generador._crearNuevoEstadoConvertido(set(estadoInicial) , 0, True)
		estadosNoAnalizados.append(estadoInicial)

		while estadosNoAnalizados:

			estado = estadosNoAnalizados[0]
			#print(estado)
			#generador._imprimirConjuntoEstados(set(estado))
			estadosNoAnalizados.remove(estado)

			#print(type(estado))

			for simbolo in afd.getAlfabeto():
				#print('en simbolo ' + simbolo)
				resultadoMover = generador._mover(set(estado), simbolo)
				#print('resultadoMover')

				#generador._imprimirConjuntoEstados(set(resultadoMover))

				inResultadoMover = False
				for resMover in resultadosMover.keys():
					if set(resMover) == resultadoMover:
						inResultadoMover = True
						resultadoMover = resMover
						break

				if not inResultadoMover:
					estadoNuevo = generador._irA(set(estado), simbolo)

					#Se verifica que existan estados en la operación 
					if len(estadoNuevo) > 0:
						estadosConvertidos[frozenset(estadoNuevo)] = generador._crearNuevoEstadoConvertido(set(estadoNuevo), numEstado)
						estadosNoAnalizados.append(estadoNuevo)

						#Se agrega la transición al estado que se está analizando con el símbolo ingresado
						for estados in estadosConvertidos.keys():
							if set(estados) == estado:
								estadosConvertidos[estados].agregarTransicion(simbolo, [estadosConvertidos[frozenset(estadoNuevo)]])

						#Se agrega el resultado Mover
						resultadosMover[frozenset(resultadoMover)] = estadoNuevo

						numEstado += 1

				else:
					#Ya se existe el estado y solo se crea la transición
					for est in estadosConvertidos.keys():
						if set(est) == estado:
							estado = est
							break

					for estados in estadosConvertidos.keys():
							if set(estados) == resultadosMover[resultadoMover]:
								estadosConvertidos[estado].agregarTransicion(simbolo, [estadosConvertidos[estados]])

		#Se agregan los estados al AFD
		for conjunto,estado in estadosConvertidos.items():
			afd.agregarEstado(estado)

		return afd
