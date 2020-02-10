from ExpresionRegular import ExpresionRegular
import sys

expresion = sys.argv[1]

ER = ExpresionRegular(expresion)
print(ER.getExpresion())
# Probamos que reconozca el alfabeto
print(ER.reconocerAlfabeto())
# Probamos que realice correctamente la conversión postfija
error, mensaje = ER.conversionAPostfija()
print(ER.getExpresionPostfija())