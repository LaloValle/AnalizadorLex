from Automatas import AFN

class GeneradorAFN():

	"""

		Clase generadora de AFNs con el paso de símbolos pertenecientes al alfabeto de una expresión regular o de AFNs también generados por algún método de esta clase

		Las funciones de esta clase son exclusivamente métodos estáticos, por lo tanto no debe ser instanciada

	"""

	@staticmethod
	def generarSimbolo(simbolo):
		""" Función que genera un AFN de un símbolo dado
			@param simbolo : string
			@returns afn : AFN """

		pass

	@staticmethod
	def generarUnion(*simbolos):
		""" Función que genera un AFN con la operación de union para dos símbolos o dos AFN dado
			@param simbolos : list
			@returns afn : AFN """
		pass

	@staticmethod
	def generarConcatenacion(*simbolos):
		""" Función que genera un AFN con la operación de concatenación para dos símbolos o dos AFN dado
			@param simbolos : list
			@returns afn : AFN """
		pass

	@staticmethod
	def generarCerraduraPositiva(*simbolo):
		""" Función que genera un AFN con la operación de cerradura para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass
                 
	@staticmethod
	def generarCerraduraKleene(*simbolo):
		""" Función que genera un AFN con la operación de cerradura de Kleene para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass

	@staticmethod
	def generarOpcional(*simbolo):
		""" Función que genera un AFN con la operación de opcional para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass


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