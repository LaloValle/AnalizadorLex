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
		if self._indiceCadena == len(self._cadena)-1:
			return 0

		while self._indiceCadena < len(self._cadena)-1:
			estadoTransicion = self._estadoActual.getEstadosTransicion(self._cadena[self._indiceCadena])
			
			if estadoTransicion:
				self._estadoActual = estadoTransicion[0]
				self._indiceCadena += 1
				self._ultimoLexema += self._cadena[self._indiceCadena]

				if self._estadoActual.isAceptacion():
					self._indiceUltimoEstadoAceptacion = int(self._indiceCadena) - 1

					self._historialEstadosAceptacion.append([Estado.estado(self._estadoActual),int(self._indiceUltimoEstadoAceptacion),self._ultimoLexema])

					return self._estadoActual.getToken()

			else:
				#No hay transiciones con el simbolo de la cadena
				if self._indiceUltimoEstadoAceptacion >= 0:
					self._indiceCadena = self._indiceUltimoEstadoAceptacion
					self._estadoActual = self._historialEstadosAceptacion[-1][0]
					self._ultimoLexema = self._historialEstadosAceptacion[-1][2]

				else:
					#Error de entrada
					self._estadoActual = None
					return -1

	def rewind(self):
		self._historialEstadosAceptacion.pop()

		self._estadoActual = self._historialEstadosAceptacion[-1][0]
		self._indiceCadena = self._historialEstadosAceptacion[-1][1]
		self._indiceUltimoEstadoAceptacion = self._historialEstadosAceptacion[-1][1]

	def getUltimoLexema(self):
		return self._ultimoLexema

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