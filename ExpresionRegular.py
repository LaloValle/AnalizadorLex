from GeneradorAutomatas import GeneradorAFN

class ExpresionRegular():

	"""
		
		Clase definitoria de una Expresión Regular, dotada con métodos que ayudan a la transformación de la ER a su respectivo AFN

		expresion 			Cadena de la expresión regular originalmente ingresada
		alfabeto: 			Lista con los símbolos que conforman al alfabeto de la ER
		operaciones: 		Diccionario utilizado para la descripción de las operaciones existentes en una ER, su procedencia o prioridad, y las funciones utilizadas para la transformación a su homólogo en terminos de un AFN
		expresionPostfija: 	Expresión resultado de la operación 'conversionAPostfija', lista con símbolos y operaciones pertenecientes a una ER

	"""


	def __init__(self, expresion = '', alfabeto = []):

		self._expresion = expresion
		self._alfabeto = alfabeto
		self._operaciones = {'α':[0,GeneradorAFN.generarSimbolo], '|':[1,GeneradorAFN.generarUnion], '°':[1,GeneradorAFN.generarConcatenacion], '⁺':[2,GeneradorAFN.generarCerraduraPositiva],
		'^+':[2,GeneradorAFN.generarCerraduraPositiva], '*':[2,GeneradorAFN.generarCerraduraKleene], '?':[2,GeneradorAFN.generarOpcional]}
		self._expresionPostfija = []
		self._agrupadores = ['(',')','[',']','{','}']

	# Getters

	def getExpresion(self):
		return self._expresion

	def getAlfabeto(self):
		return self._alfabeto

	def getOperaciones(self):
		return self._operaciones

	def getExpresionPostfija(self):
		return self._expresionPostfija

	def inAlfabeto(self, simbolo):
		return simbolo in self._alfabeto

	def inOperaciones(self, operador):
		return operador in self._operaciones

	def getOperacionConversionAFN(self, operador):
		""" Método que regresa la función que transforma a la operación dada en ER a su homóloga en los AFNs

			@param operador: string, cadena del operador utilizado en la ER
			@returns función: GeneradorAFN.método, método perteneciente a la clase GeneradorAFN que genera el AFN de dicha operación según los parámetros ingresados // None: en caso de no existir tal operación	
		"""
		if self.inOperaciones(operador):
			return self._operaciones[operador][1]
		else: return None

	# Setters

	def setExpresion(self, expresion):
		self._expresion = expresion

	def setAlfabeto(self, alfabeto = []):
		self._alfabeto = alfabeto

	def agregarSimboloAlfabeto(self, simbolo):
		self._alfabeto.append(simbolo)

	# Operaciones

	def reconocerAlfabeto(self):
		""" Método que reconoce el alfabeto automáticamente dada la expresión regular
			
			@returns alfabeto: lista, conjunto del alfabeto reconocido en la expresión regular
		"""
		simbolo = ''

		for s in self._expresion:
			# Se verifica si es un operador o agrupador
			if s in self._operaciones or s in self._agrupadores and s != 'α':
				if simbolo != '':
					#Se verifica que el símbolo no este ya en el alfabeto
					if simbolo not in self._alfabeto:
						self._alfabeto.append(simbolo)
					simbolo = ''

			else:
				simbolo += s

		if simbolo != '':
			if simbolo not in self._alfabeto:
				self._alfabeto.append(simbolo)

		return self.getAlfabeto()


	def conversionAPostfija(self):
		""" Método que permite convertir a la expresión regular dada en la variable 'expresión', a un expresión postfija, permitiendo realizar las operaciones correspondientes por la computadora
			
			@retuns 0: si se realizó correctamente // -1 : en caso de un error y una cadena describiendo el error: La expresión convertida se almacenará en 'expresionPostfija' colocando cada símbolo y operación en un índice de la lista

			REGLAS(dentro de la pila):

				# Precedencia del operador de la cadena = precedencia del operador en la pila -> Cambian de lugares, uno sale de la pila y el otro entra
				# Precedencia del operador de la cadena > precedencia del operador en la pila -> Se agrega el operador de la cadena a la pila
				# Precedencia del operador de la cadena < precedencia del operador en la pila -> Salen los operadores con mayor precendencia dentro de la pila e ingresa el de la cadena
				# Agrupadores derechos en la cadena ')]}' -> Se vacía la pila hasta encontrar el agrupador pareja de cierre
		"""
		if self._expresion == '': return -1

		simbolo = ''
		pila = []

		for s in self._expresion:
			# Se verifica si es una símbolo del alfabeto o una operación/agrupador
			if s in self._agrupadores or s in self._operaciones and s != 'α':
				# Se guarda en la lista resultante el símbolo existente en la variable de mismo número
				if simbolo != '':
					self._expresionPostfija.append(simbolo)
					simbolo = ''

				# Se verifica si es un agrupador
				if s in self._agrupadores:
					if self._agrupadores.index(s)%2 == 0:
						# Es un agrupador izquierdo
						pila.append(s)

					else:
						# Se verfica que en la pila exista su contraparte izquierda
						if self._agrupadores[self._agrupadores.index(s)-1] in pila:
							# Se vacía la pila
							for _ in range(len(pila)):
								sp = pila.pop()

								# Se verifica que el elemento de la pila no sea algún otro agrupador
								if sp in self._operaciones:
									# Es un operador y se agrega a la lista resultado
									self._expresionPostfija.append(sp)

								else:
									# Es un agrupador y se verifica que sea su contraparte de apertura, de otra forma la expresión no sería válida
									if sp != self._agrupadores[self._agrupadores.index(s)-1]:
										self._expresionPostfija.clear()
										return (-1,'Se ha encontrado un agrupador sin su contraparte')

									break

						else:
							self._expresionPostfija.clear()
							return (-1,'Se ha encontrado un agrupador de cierre sin su contraparte de apertura')
				else:
					# Se trata de un operador
					while len(pila) > 0:
						# Se verifica primero si el símbolo en la pila es una agrupador
						if pila[-1] in self._agrupadores:
							break

						# Se obtienen y evalúan las procedencias
						procedenciaS = self._operaciones[s][0]
						procedenciaSP = self._operaciones[pila[-1]][0]

						if procedenciaS > procedenciaSP:
							# La procedencia del símbolo de la cadena es mayor al de la pila e ingresa en la pila
							break
						elif procedenciaS <= procedenciaSP:
							# La procedencia del símbolo de la cadena es menor o igual al de la pila y saca al operador de la pila
							self._expresionPostfija.append(pila.pop())

					pila.append(s)

			else:
				# Se trata de un símbolo perteneciente al alfabeto
				simbolo += s

		# Se verifica que la pila este vacía y la variable símbolo este vacía
		if simbolo != '': self._expresionPostfija.append(simbolo)
		
		if len(pila) > 0:
			for _ in range(len(pila)):
				#Se verifica que no existan agrupadores restantes en la pila
				if pila[-1] in self._agrupadores:
					self._expresionPostfija.clear()
					return (-1,'Se ha encontrado un agrupador sin su contraparte')
				else:
					self._expresionPostfija.append(pila.pop())

		return (0 , '')
