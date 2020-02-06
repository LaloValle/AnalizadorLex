from Automatas import AFN,Estado

class GeneradorAFN():

	"""

		Clase generadora de AFNs con el paso de símbolos pertenecientes al alfabeto de una expresión regular o de AFNs también generados por algún método de esta clase

	"""

	@staticmethod
	def __init__(self):


	def _generarautomata(self,simbolo):
		""" Función que genera un AFN de un símbolo dado
			@param simbolo : string
			@returns afn : AFN """
		nombre = simbolo[0]

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

		nombre = automatas[1].getNombre() + '°' + automatas[0].getNombre()

		afn = AFN(nombre)

		#El estado final del primer autómata se convierte en el primer estado del segundo
		automatas[1].getEstadosAceptacion()[0].setTransiciones(automatas[0].getEstadoInicial().getTransiciones())

		#Se le elimina al estado de aceptación del primer automata la propiedad de ser aceptación
		automatas[1].getEstadosAceptacion()[0].setAceptacion(False)
		#Se elimina el estado inicial del segundo autómata
		automatas[0].eliminarEstado(automatas[0].getEstadoInicial())

		#Se conforma el nuevo autómata con las modificaciones realizadas
		afn.agregarEstados(automatas[1].getEstados())
		afn.agregarEstados(automatas[0].getEstados())

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

				#Se llama la función para operar los símbolos o AFN
				pilaSimbolos.append(operaciones[s][1](automatasOperar))

			else:
				#Es un símbolo perteneciente al alfabeto
				if s in alfabeto:
					pilaSimbolos.append(generador._generarautomata(s))
				else:
					return -1,'Símbolo no reconocido como operación ni perteneciente al alfabeto'

		if type(pilaSimbolos[-1]) == AFN and len(pilaSimbolos) == 1:
			afn = pilaSimbolos.pop()
		else:
			return -1,'El resultado de la pila no es un autómata o existen más elementos'

		afn.setAlfabeto(alfabeto)

		return afn,'Generación correcta del AFN'


class GeneradorAFD(AFN):

	"""

		Clase generadora de los AFD a partir de los estados que conforman a un AFN

		estadosNoAnalizados:	Diccionario que representa a un subconjunto de estados resultado de la operación 'generalizar' y a lo cuales aún no se les ha aplicado dicha operación, la llave es la lista de los estados y el elemento descrito por la llave el nombre del nuevo estado convertido
		estadosAnalizados:		Diccionario que representa al subconjunto de estados operados por 'generalizar'


	"""

	def __init__(self, estadosNoAnalizados = {}, estadosAnalizados = {}):
		self._estadosNoAnalizados = {}
		self._estadosAnalizados = {}


	# Getters

	def getEstadosNoAnalizados(self):
		return self._estadosNoAnalizados

	def getEstadosAnalizados(self):
		return self._estadosAnalizados

	def isEstadoNoAnalizado(self, estados):
		return self._estadoNoAnalizado[estados]

	def isEstadoAnalizado(self, estados):
		return self._estadoAnalizado[estados]

	def obtenerNombreEstadosAnalizados(self, estados):
		""" Método que devuelve el nombre dado a un conjunto de estados después de la operación generalizar, buscando tanto en los estados ya analizados y los aún no analizadas

			@param estados: list, conjunto de los estados que definen al nombre del nuevo estado
			@returns estadosAnalizados[estados] : string, nombre del conjunto de estados; ''(cadena vacía) : en caso de no existir el conjunto en los diccionarios """

		if estados in self._estadosAnalizados:
			return self._estadosAnalizados[estados]
		elif estados in self._estadosNoAnalizados:
			return self._estadosNoAnalizados[estados]
		else:
			return ''

	# Setters

	def agregarEstadoNoAnalizado(self, estados, nombre):
		self._estadoNoAnalizado[estados] = nombre

	def agregarEstadoAnalizado(self, estados, nombre):
		self._estadoAnalizado[estados] = nombre

	# Operaciones

	def generalizar(self, estado, simbolo, letraNombre = 'S', cuentaNumeroNombre = 0):
		""" Función utilizada para la generación de los nuevos estados pertenecientes al AFD perteneciente al AFN

			@param estado: Estado, estado perteneciente al diccionario estadosNoAnalizados, y al cual se le desea realizar la operación
			@param simbolo: string, símbolo con el que se realizará la operación
			@param letraNombre: string, letra que será acompañada del número especificado en el parámetro cuentaNumeroNombre, para el nombramiento de nuevos estados
			@param cuentaNumeroNombre: string, número inicial de la cuenta para la colocación junto a la letra del nombre para la identificación de los nuevos estados

			@returns 0: en caso correcto // -1 : en caso de un error en el proceso de la operación

			@precondition : el primer estado a analizar en el proceso debe ser resultado directo de la Cerradura Epsilon; La variable cuentaNumeroNombre se actualizará de forma que sea conocido cuál es el último número disponible para la generación de más nombres de estados
			@postcondition : se elimina del diccionario estadosNoAnalizados el estado recién analizado y se agrega al diccionario estadosAnalizados
		"""
		pass

	def generarAFD(self):
		""" Función que genera un nuevo AFD

			@retuns afd : AFD, autómata resultante

			@precondition se debió de haber realizado el proceso completo de la generalización de todos los estados resultantes en esta operación, finalmente el diccionario estadosNoAnalizados debe de estar vacío y el diccionario estadosAnalizados debe contener todos los estados convertidos
		"""
		pass
