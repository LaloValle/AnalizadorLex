from Automatas import AFN,Estado

class GeneradorAFN():

	"""

		Clase generadora de AFNs con el paso de símbolos pertenecientes al alfabeto de una expresión regular o de AFNs también generados por algún método de esta clase

	"""
	def _ingresosMismoTipo(self,ingresos):
		""" Verifica que dos 'simbolos' ingresados seán de tipo str o AFN, si no llegarán a ser del mismo tipo entonces convertirá al símbolo en un AFN

			@param ingresos: list, lista de los dos ingresos
		"""
		aux = ingresos

		if type(ingresos[0]) != type(ingresos[1]):
			aux = []
			for s in ingresos:
				if type(s) == str:
					s = self._generarSimbolo(s)
				aux.append(s)

		return aux


	def _generarSimbolo(self,simbolo):
		""" Función que genera un AFN de un símbolo dado
			@param simbolo : string
			@returns afn : AFN """
		nombre = simbolo[0]

		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{nombre:[ef]},False,True)

		afn = AFN(nombre)
		afn.setEstados([e0,ef])

		return afn

	def _generarUnion(self,simbolos):
		""" Función que genera un AFN con la operación de union para dos símbolos o dos AFN dado
			@param simbolos : list
			@returns afn : AFN """

		#Verifica que los dos ingresos sean o str o AFNs
		simbolos = self._ingresosMismoTipo(simbolos)

		nombre = simbolos[1].getNombre() + '|' + simbolos[0].getNombre() if type(simbolos[0]) == AFN else simbolos[1] + '|' + simbolos[0]

		afn = AFN(nombre)

		nombre = '(' + nombre + ')'
		#Creación de estados comunes
		ef = Estado(nombre+'f',{},True)
		e0 = Estado(nombre+'0',{})
		afn.setEstadoInicial(e0)

		# llave :[estado transición del inicial, estado que transiciona a estado final]
		estadosAux = {}

		#Se verifica que tipo de argumentos se han ingresado
		if type(simbolos[0]) == AFN:
			#Se han ingresado AFNs

			for automata in simbolos:
				estadoAceptacion = automata.getEstadosAceptacion()
				estadoAceptacion[0].setAceptacion(False)
				estadosAux[len(estadosAux)] = [automata.getEstadoInicial(),estadoAceptacion[0]]

				afn.agregarEstados(automata.getEstados())

		elif type(simbolos[0]) == str:
			# Se han ingresado símbolos
			numeracion = 1

			for simbolo in simbolos:
				e2 = Estado(nombre+str(numeracion+1))
				e1 = Estado(nombre+str(numeracion), {simbolo:[e2]})

				estadosAux[numeracion] = [e1,e2]

				numeracion += 2

		#Se asignan las transciciones del estado inicial y al estado final
		for llave, estados in estadosAux.items():
			e0.agregarTransicion('ε',[estados[0]])
			estados[1].agregarTransicion('ε',[ef])

			#Se agregan los estados al AFN
			afn.agregarEstado(estados[0])
			afn.agregarEstado(estados[1])

		#Se agrega el estado de aceptación
		afn.agregarEstado(ef)

		return afn

	def _generarConcatenacion(self,simbolos):
		""" Función que genera un AFN con la operación de concatenación para dos símbolos o dos AFN dado
			@param simbolos : list
			@returns afn : AFN """

		#Verifica que los dos ingresos sean o str o AFNs
		simbolos = self._ingresosMismoTipo(simbolos)

		nombre = simbolos[1].getNombre() + '°' + simbolos[0].getNombre() if type(simbolos[0]) == AFN else simbolos[1] + '°' + simbolos[0]

		afn = AFN(nombre)

		nombre = '(' + nombre + ')'

		#Se verifica que tipo de argumentos se han ingresado
		if type(simbolos[0]) == AFN:
			#Se han ingresado AFNs

			#El estado final del primer autómata se convierte en el primer estado del segundo
			simbolos[1].getEstadosAceptacion()[0].setTransiciones(simbolos[0].getEstadoInicial().getTransiciones())

			#Se le elimina al estado de aceptación del primer automata la propiedad de ser aceptación
			simbolos[1].getEstadosAceptacion()[0].setAceptacion(False)
			#Se elimina el estado inicial del segundo autómata
			simbolos[0].eliminarEstado(simbolos[0].getEstadoInicial())

			#Se conforma el nuevo autómata con las modificaciones realizadas
			afn.agregarEstados(simbolos[1].getEstados())
			afn.agregarEstados(simbolos[0].getEstados())

		elif type(simbolos[0]) == str:
			# Se han ingresado símbolos

			ef = Estado(nombre+'f',{},True)
			e1 = Estado(nombre+'1',{simbolos[0]:[ef]})
			e0 = Estado(nombre+'0',{simbolos[1]:[e1]},False,True)

			afn.agregarEstados([e0,e1,ef])

		return afn


	def _generarCerraduraPositiva(self,simbolo):
		""" Función que genera un AFN con la operación de cerradura para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass

	def _generarCerraduraKleene(self,simbolo):
		""" Función que genera un AFN con la operación de cerradura de Kleene para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass

	def _generarOpcional(self,simbolo):
		""" Función que genera un AFN con la operación de opcional para un símbolo o un AFN dado
			@param simbolo : list
			@returns afn : AFN """
		pass


	@staticmethod
	def generarAFNDePostfija(postfija, alfabeto):
		generador = GeneradorAFN()

		operaciones = {'|':[2,generador._generarUnion], '°':[2,generador._generarConcatenacion], '⁺':[1,generador._generarCerraduraPositiva],'^+':[1,generador._generarCerraduraPositiva], '*':[1,generador._generarCerraduraKleene], '?':[1,generador._generarOpcional]}

		pilaSimbolos = []

		for s in postfija:
			if s in operaciones:
				#Es una operación

				simbolosOperar = []

				#Se obtiene los simbolos que serán operados
				for _ in range(operaciones[s][0]):
					simbolosOperar.append(pilaSimbolos.pop())

				#Se llama la función para operar los símbolos o AFN
				pilaSimbolos.append(operaciones[s][1](simbolosOperar))

			else:
				#Es un símbolo perteneciente al alfabeto
				if s in alfabeto:
					pilaSimbolos.append(s)
				else:
					return -1

		#Se verifica el caso en el que solo sea necesite transformar el AFN de un símbolo
		if len(pilaSimbolos) > 0:
			if type(pilaSimbolos[-1]) == str:
				afn = generador._generarSimbolo(pilaSimbolos.pop())

			elif type(pilaSimbolos[-1]) == AFN:
				afn = pilaSimbolos.pop()

		afn.setAlfabeto(alfabeto)

		return afn
		



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
