#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Un sudoku es un rompecabezas de números. Se le
# presenta al jugador un cuadro de 9 X 9 casillas
# subdividida en sub-cuadros de 3 X 3. El cuadro se le
# presenta al jugador con algunas casillas llenas y el
# objetivo es que el jugador termine de llenarlas para
# completar el cuadro siguiendo las siguientes reglas;
# cada fila, columna y sub-cuadro de 3 X 3 debe contener
# los números del 1 al 9 en cualquier orden. Esto es un
# programa que permite introducir, guardar, leer y lo
# más importante resolver rompecabezas de sudoku.

# Este programa lo estoy escribiendo desde la pantalla
# tactil de mi Samsung A21S. Lo comencé durante un vuelo
# con mi esposa Mariel y mi suegra Doña Mildred de Santo
# Domingo a New Jersey. Luego continue trabajando en el
# cuando acompañe a mi esposa a un retiro de Barahona de
# mujeres feministas. Mientras ellas hablaban de
# feminismo yo estaba en una mesedora por ahí jugando
# con este programita en el celular. Después de ahí en
# otras ocasiones he estado avanzado según se me
# presenta el tiempo y la inspiración.

# Este fichero en particular es el programa de interface
# con el usuario, este es el programa que se ejecuta
# para crear un sudoku nuevo, tratar de resolverlo a
# mano o pedirle al programa que lo resuelva. Hay dos
# ficheros más en este paquete que también son
# importantes. sudoku.py es el módulo más importante de
# hecho, contiene la clase sudoku y sus sub-partes que
# es lo que uso para representar un sudoku, una
# instancia del rompecabezas. El último fichero sería
# PruebasSudoku.py que contiene una colección de pruebas
# unitarias para evaluar todas las funciones que se
# necesitan para que este programa funcione.

import sudoku
import re

exComando = re.compile(
    "^ *([efcutvlht])([1-9])?(( *, *[0-9]?)*) *$")

def volverEOD(valor, defecto):
    try:
        val = int(valor)
    except:
        val = defecto
    return val

def leerEntero(pedido):
    val = input(pedido)
    return volverEOD(val, -1)

def leerOpcion(opciones):
    print("Elija una opción:")
    for i, o in zip(
            range(1, len(opciones) + 1),
            opciones):
        print("{} - {}".format(i, o))
    print("\n")
    val = leerEntero("opción: ")
    while (val < 1) or (val > len(opciones)):
        print("Opción inválida")
        val = leerEntero("opción: ")
    return val

def mostrarComandosIntro():
    print("Introduzca los valores del sudoku")
    print(" - e, x, y, valor para valor de casilla..")
    print(" - fN, v1, v2, v3, ..., v9 para fila N.")
    print(" - cN, v1, v2, v3, ..., v9 para columna N.")
    print(" - uN, v1, v2, v3, ..., v9 para cuadro N.")
    print(" - t, v1, v2, v3, ..., v81 para todos.")
    print(" - v para ver el cuadro.")
    print(" - l para limpiar el cuadro.")
    print(" - h para ver estas instrucciones.")
    print(" - t para terminar.")

def avisarComErrado():
    print("Error: El comando introducido contiene errores.")

def procesarComando(com, juego):
    global exComando
    encaje = exComando.fullmatch(com)
    if encaje:
        accion = encaje.group(1)
        ref = volverEOD(encaje.group(2), 0)
        if encaje.group(3) == "":
            val = None
        else:
            val = encaje.group(3).replace(" ", "").split(",")[1:]
            val = list(map(volverEOD, val, [0] * len(val)))
        if ((accion == "e") and (ref == 0)
            and (val != None)
            and (len(val) == 3)
            and sudoku.es1al9(val[0])
            and sudoku.es1al9(val[1])):
            juego.ponerValor(val[0] - 1, val[1] - 1, val[2])
        elif (ref == 0) and (val == None):
            if (accion == "v"):
                print(juego.mostrar())
            elif (accion == "l"):
                print(juego.limpiar())
            elif (accion == "h"):
                mostrarComandosIntro()
            elif (accion == "t"):
                print("Terminando la introducción del sudoku.")
        else:
            avisarComErrado()
    else:
        avisarComErrado()

def introducirSudoku(juego):
    mostrarComandosIntro()
    com = ""
    while com != "t":
        com = input("#> ")
        procesarComando(com, juego)

def guardarSudoku(juego):

    pass

def leerSudoku(juego):

    pass

def solucionarSudoku(juego):
    pass

def evaluarSolucion(juego):
    pass

def main():
    juego = sudoku()
    print("\nResolvedor de Sudokus\n\n")
    operaciones = {1: introducirSudoku,
                   2: guardarSudoku,
                   3: leerSudoku,
                   4: solucionarSudoku,
                   5: evaluarSolucion}
    menu = ["Introducir", "Guardar",
            "Leer", "Soluciones",
            "Evaluar solución",
            "Salir"]
    opc = 1
    while opc <= len(operaciones):
        opc = leerOpcion(menu)
        if opc <= len(operaciones):
            operacion = operaciones[opc]
            operacion(juego)
    print("Pase feliz resto del día.")

if __name__ == "__main__":
    main()
