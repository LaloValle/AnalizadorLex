class Estado():

	""" 

		Clase definitoria de un estado para un AFN o un AFD

			nombre: 		Nombre del estado
			transiciones:	Diccionario que define las transiciones del estado con otros estados, la llave es un síbolo del alfabeto y los elementos descritos por la llave los estados a los que transiciona
			aceptacion:		Valor Booleano lo denota como estado de aceptación

	"""

	def __init__(self, nombre, transiciones = {} , aceptacion = False):
		self._nombre = nombre
		self._transiciones = transiciones
		self._aceptacion = aceptacion

	# Getters

	def getNombre(self):
		return self._nombre

	def getTransiciones(self):
		return self._transiciones

	def isAceptacion(self):
		return self._aceptacion

	# Setters

	def setNombre(self, nombre):
		self._nombre = nombre

	def setTransiciones(self, transiciones):
		self._transiciones = transiciones

	def setAceptacion(self):
		self._aceptacion = True

	def agregarTransicion(self, simbolo, estados = []):
		self._transiciones[simbolo] = estados

	# Operaciones

	def mover(self, simbolo):
		""" Operación que retorna un conjunto de estados al que transiciona un estado con el símbolo dado

			@param simbolo: string
			@returns transiciones[simbolo] : list(Estado)"""

		return self._transiciones[simbolo]


class Automata():
	"""

		Clase definitoria de un Automata y los elementos que lo componen:

			estados: 	Lista del conjunto de objetos tipo Estado
			alfabeto: 	Conjunto de símbolos que conforman al alfabeto del Automata

	"""

	def __init__(self, estados = [], alfabeto = []):
		self._estados = []
		self._alfabeto = []

	# Getters

	def getEstados(self):
		return self._estados

	def getAlfabeto(self):
		return self._alfabeto

	def getEstado(self, nombre):
		for estado in self._estados:
			if estado.getNombre() == nombre: 
				return estado
			else:
				return None

	def inAlfabeto(self, simbolo):
		return simbolo in self._alfabeto

	# Setters

	def setEstados(self, estados):
		self._estados = estados

	def setAlfabeto(self, alfabeto):
		self._alfabeto = alfabeto

	def agregarEstado(self, estado):
		""" Método que permite agregar un estado al conjunto perteneciente al Autómata

			@param estado: Estado
			@returns 0 : en caso correcto // -1 : estado no es una instancia de la clase Estado """

		if type(estado) == Estado:
			self._estados.append(estado)
			return 0
		
		return -1

	def agregarSimboloAlfabeto(self, simbolo):
		""" Método que permite agregar un símbolo al Alfabeto perteneciente al Autómata

			@param simbolo: string
			@returns 0 : en caso correcto // -1 : el símbolo ya es parte del Alfabeto """
		
		if simbolo not in self._alfabeto:
			self._alfabeto.append(simbolo)
			return 0

		return -1


class AFN(Automata):

	"""

		Clase definitoria de un AFN

	"""

	def __init__(self, estados =[], alfabeto = []):
		self._estados = estados
		self._alfabeto = alfabeto

	def cerraduraEpsilon(self, estados = []):
		""" Caso especial de la operación mover donde se obtienen el número máximo de estados que transicionan desde el primer estado con 'ɛ' como símbolo
			
			@param estados : lista de estados que transicionan con ɛ
			@returns 0: en caso correcto // -1 : en un error en el proceso de la operación
			El resultado de los estados que transicionan con 'ɛ' se agregarán a la lista 'estados' pasada como parámetro
		"""
		pass


class AFD(Automata):

	"""

		Clase definitori de una AFD

	"""
	def __init__(self, estados = [], alfabeto = []):
		self._estados = estados
		self._alfabeto = alfabeto