from Automatas import *

class AnalizadorLexico():

	def __init__(self, automata, cadena):
		self._cadena = cadena

		self._estadoActual = automata.getEstadoInicial()
		self._indiceCadena = 0
		self._ultimoLexema = ''
		self._indiceUltimoEstadoAceptacion = -1

		self._historialEstadosAceptacion = [[Estado.estado(self._estadoActual),0,'']]

	def getToken(self):
		if self._indiceCadena == len(self._cadena):
			return 0

		while self._indiceCadena < len(self._cadena):
			estadoTransicion = self._estadoActual.getEstadosTransicion(self._cadena[self._indiceCadena])

			if estadoTransicion:
				self._estadoActual = estadoTransicion[0]
				self._indiceCadena += 1
				self._ultimoLexema += self._cadena[self._indiceCadena-1]

				if self._estadoActual.isAceptacion():

					self._historialEstadosAceptacion.append([Estado.estado(self._estadoActual),int(int(self._indiceCadena) - 1),self._ultimoLexema])
					if self._indiceCadena == len(self._cadena):
						return self._estadoActual.getToken()

			else:
				#No hay transiciones para el símbolo
				if len(self._historialEstadosAceptacion) == 1:
					#Error de entrada
					self._estadoActual = None
					return -1
				
				if len(self._historialEstadosAceptacion) > 1:
					self._estadoActual = self._historialEstadosAceptacion[-2][0]
					self._ultimoLexema = self._ultimoLexema[len(self._historialEstadosAceptacion[-1][2])+1:len(self._ultimoLexema)]

					return self._historialEstadosAceptacion[-1][0].getToken()

	def rewind(self):
		self._historialEstadosAceptacion.pop()

		self._estadoActual = self._historialEstadosAceptacion[-2][0]
		self._indiceCadena = self._historialEstadosAceptacion[-2][1]
		self._indiceUltimoEstadoAceptacion = self._historialEstadosAceptacion[-2][1]

	def getUltimoLexema(self):
		return self._historialEstadosAceptacion[-1][2]

class Token(object):

	#Constantes referentes a los token de las ER
	UNION = 10

	CONCATENACION = 20

	CERRADURA_POSITIVA = 30

	CERRADURA_KLEENE = 40

	OPCIONAL = 50

	SIMBOLO = 60

	BACK_SLASH = 70

	PARENTESIS_IZQUIERDO = 80

	PARENTESIS_DERECHO = 81