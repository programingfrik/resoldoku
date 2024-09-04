#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este módulo contiene una batería de pruebas unitarias
# para probar la clase sudoku.py que es la clase que se
# usa para representar la matriz del rompecabezas en el
# programa principal resoldoku.py

import sys
import sudoku

def pruebaEs1al9():
    """Pruebas de la función es1al9."""
    es1al9 = sudoku.es1al9
    # El 0 es menor que 1.
    assert not es1al9(0)
    # El 4 si está en el intervalo.
    assert es1al9(4)
    assert es1al9(9)
    assert es1al9(1)
    assert not es1al9(-1)
    # El 10 es mayor que el 9.
    assert not es1al9(10)

def pruebaCrearGrupoCasillas():
    """Probando la creacion de la clase GrupoCasillas."""
    grupoCasillas = sudoku.grupoCasillas
    casilla = sudoku.casilla
    origen = 9
    muestra = grupoCasillas(origen)
    assert len(muestra) == origen
    # Inicialmente debería estar lleno de 0s.
    assert all(map(lambda x: x.valor == 0,
                   [v for v in muestra]))
    origen = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    muestra = grupoCasillas(origen)
    assert len(muestra) == len(origen)
    # El grupo se puede recorrer y contiene los valores
    # de ejemplo usados.
    assert all(map(lambda x, y: x.valor == y,
                   muestra, origen))
    origen = [casilla(), casilla(1),
              casilla(2), casilla(3)]
    muestra = grupoCasillas(origen)
    assert len(muestra) == len(origen)
    assert all(map(lambda x, y: x is y,
                   muestra, origen))

def pruebaContainsGrupoCasillas():
    """Probando que se puede combrobar si un valor está
    dentro de un grupo."""
    grupoCasillas = sudoku.grupoCasillas
    casilla = sudoku.casilla
    origen = [1, 2, 3, 4]
    muestra = grupoCasillas(origen)
    assert all(map(lambda x: x in muestra, origen))
    origen = [casilla(1), casilla(2), casilla(3)]
    muestra = grupoCasillas(origen)
    assert all(map(lambda x: x in muestra, origen))
    assert 9 not in muestra
    assert casilla(7) not in muestra

def pruebaCopiarCasilla():
    """Comprobando que al copiar una casilla no se usa
    la misma instancia."""
    casilla = sudoku.casilla
    muestra = casilla()
    muestra.valor = 7
    muestra.tipo = sudoku.TIPO_NORMAL
    muestra.color = "rojo"
    copia = muestra.copiar()
    copia.valor = 3
    copia.tipo = sudoku.TIPO_FIJO
    copia.color = "azul"
    # comprobando que no son la misma instancia.
    assert muestra.valor != copia.valor
    assert muestra.tipo != copia.tipo
    assert muestra.color != copia.color

def pruebaTraducirCoord9NumCuadro():
    traducir = sudoku.traducirCoord9NumCuadro
    assert traducir(0, 0) == 0
    assert traducir(1, 2) == 5
    assert traducir(2, 2) == 8
    assert traducir(0, 2) == 2
    assert traducir(2, 0) == 6

def pruebaTraducirCoordNumCuadro():
    traducir = sudoku.traducirCoordNumCuadro
    assert traducir(0, 0) == 0
    assert traducir(3, 0) == 3
    assert traducir(5, 2) == 3
    assert traducir(6, 6) == 8
    assert traducir(8, 8) == 8

def pruebaTraducirNumCuadroCoord9():
    traducir = sudoku.traducirNumCuadroCoord9
    assert traducir(0) == (0, 0)
    assert traducir(3) == (1, 0)
    assert traducir(8) == (2, 2)

def pruebaTraducirCuadroCasCoord():
    traducir = sudoku.traducirCuadroCasCoord
    assert traducir(0, 0) == (0, 0)
    assert traducir(3, 0) == (3, 0)
    assert traducir(1, 2) == (0, 5)
    assert traducir(5, 5) == (4, 8)
    assert traducir(6, 8) == (8, 2)

def pruebaTraducirCoordCuadroCas():
    traducir = sudoku.traducirCoordCuadroCas
    assert traducir(0, 0) == (0, 0)
    assert traducir(3, 0) == (3, 0)
    assert traducir(0, 5) == (1, 2)
    assert traducir(4, 8) == (5, 5)
    assert traducir(8, 2) == (6, 8)

def pruebaTraducirNumCuadroCoord():
    traducir = sudoku.traducirNumCuadroCoord
    assert traducir(0) == (0, 0)
    assert traducir(8) == (0, 8)
    assert traducir(9) == (1, 0)
    assert traducir(30) == (3, 3)

def pruebaCopiarGrupo():
    grupoCasillas = sudoku.grupoCasillas
    casilla = sudoku.casilla
    muestra = grupoCasillas([1, 2, 3, 4])
    copia = muestra.copiar()
    cambio = [5, 6, 7, 8]
    for cas in copia:
        cas.valor = cambio.pop()
    assert all(map(lambda x, y: x.valor != y.valor,
                   muestra, copia))

def verificarEquivFilaColumnaCuadro(sujeto):
    for i in range(9):
        for j in range(9):
            cua, cas = sudoku.traducirCoordCuadroCas(i, j)
            assert (sujeto.filas[i][j]
                    is sujeto.columnas[j][i])
            assert (sujeto.filas[i][j]
                    is sujeto.subcuadros[cua][cas])

def pruebaEquivSudoku():
    muestra = sudoku.sudoku()
    verificarEquivFilaColumnaCuadro(muestra)
    otro = muestra.copiar()
    verificarEquivFilaColumnaCuadro(otro)

def pruebaCopiarSudoku():
    tablero = sudoku.sudoku
    muestra = tablero()
    muestra.filas[4][2].valor = 3
    muestra.filas[5][1].valor = 9
    muestra.filas[4][7].valor = 1
    copia = muestra.copiar()
    assert copia is not muestra
    assert len(muestra.filas) == len(copia.filas)
    assert all(map(lambda x, y: len(x) == len(y),
                   muestra.filas, copia.filas))
    for i in range(9):
        for j in range(9):
            assert (muestra.filas[i][j].valor
                    == copia.filas[i][j].valor)

def pruebaPonerValor():
    sujeto = sudoku.sudoku()
    copia = sujeto.copiar()
    sujeto.ponerValor(4, 4, 2)
    for i in range(9):
        for j in range(9):
            if ((i == 4) and (j == 4)):
                continue
            assert (sujeto.filas[i][j].valor
                    == copia.filas[i][j].valor)
    assert sujeto.filas[4][4].valor == 2

def comprobarSubparte(origen, vals):
    for i in range(len(vals)):
        if ((vals[i] != None)
            and (vals[i] != origen[i].valor)):
            print ("{} != {}".format(
                vals[i], origen[i].valor))
            return False
    return True

def pruebaPonerFila():
    sujeto = sudoku.sudoku()
    muestra = [3, 4, None, 5, 0, 1, 0]
    sujeto.ponerFila(2, muestra)
    assert comprobarSubparte(sujeto.filas[2], muestra)
    muestra = [None, 5, 2, 7, 0, 9]
    sujeto.ponerFila(2, muestra)
    assert comprobarSubparte(sujeto.filas[2], muestra)

def pruebaPonerColumna():
    sujeto = sudoku.sudoku()
    muestra = [2, 4, 3, 0, None, 7]
    sujeto.ponerColumna(3, muestra)
    assert comprobarSubparte(sujeto.columnas[3], muestra)
    muestra = [2, None, 1, 8, 9, 4]
    sujeto.ponerColumna(3, muestra)
    assert comprobarSubparte(sujeto.columnas[3], muestra)

def pruebaPonerSubcuadro():
    sujeto = sudoku.sudoku()
    muestra = [4, 2, None, 5, 1, 2]
    sujeto.ponerSubcuadro(3, muestra)
    for i in range(len(muestra)):
        x, y = sudoku.traducirCuadroCasCoord(3, i)
        assert ((muestra[i] == None)
                or ((muestra[i] != None)
                    and (muestra[i]
                         == sujeto.filas[x][y].valor)))

def pruebaPonerTodos():
    sujeto = sudoku.sudoku()
    muestra = [3, 0, 1, 6, None, 9, 2, 0, 0, 4]
    sujeto.ponerTodos(muestra)
    for i in range(len(muestra)):
        x, y =
    # raise NotImplementedError()
    pass

def main():
    print("Haciendo pruebas del API de resoldoku.")
    for func in globals():
        if func.startswith("prueba"):
            print("Haciendo prueba {} ... "
                  .format(func), end = "")
            tempfunc = globals()[func]
            tempfunc()
            print("PASO!")

if __name__ == "__main__":
    main()
