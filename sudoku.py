#!/usr/bin/python3
# -*- coding: utf-8 -*-

TIPO_NORMAL = 0
TIPO_FIJO = 1

def es1al9(val):
    return (val > 0) and (val <= 9)

def traducirCoord9NumCuadro(cx, cy):
    return (cx * 3) + cy

def traducirCoordNumCuadro(x, y):
    c = y // 3
    f = x // 3
    return traducirCoord9NumCuadro(f, c)

def traducirNumCuadroCoord9(num):
    cy = num % 3
    cx = num // 3
    return cx, cy

def traducirNumCuadroCoord(num):
    y = num % 9
    x = num // 9
    return x, y

def traducirCuadroCasCoord(cuadro, cas):
    x, y = traducirNumCuadroCoord9(cuadro)
    x *= 3
    y *= 3
    cx, cy = traducirNumCuadroCoord9(cas)
    x += cx
    y += cy
    return x, y

def traducirCoordCuadroCas(x, y):
    cuadro = traducirCoordNumCuadro(x, y)
    cx = x % 3
    cy = y % 3
    cas = traducirCoord9NumCuadro(cx, cy)
    return cuadro, cas

class casilla:
    def __init__(self, valor = 0):
        self.limpiar()
        self.valor = valor

    def limpiar(self):
        self.valor = 0
        self.tipo = TIPO_NORMAL
        self.color = ""

    def copiar(self):
        copia = casilla()
        copia.valor = self.valor
        copia.tipo = self.tipo
        copia.color = self.color
        return copia

class grupoCasillas:
    def __init__(self, ini):
        self.grupo = []
        if (type(ini) is int) and (ini > 0):
            self.grupo = [casilla() for i in range(ini)]
        elif ((type(ini) is list) and (len(ini) > 0)
              and (type(ini[0]) is int)):
            for val in ini:
                self.grupo.append(casilla(val))
        elif ((type(ini) is list) and (len(ini) > 0)
              and (type(ini[0]) is casilla)):
            self.grupo = ini

    def __contains__(self, item):
        if type(item) is casilla:
            if item in self.grupo:
                return True
            buscado = item.valor
        elif type(item) is int:
            buscado = item
        else:
            raise TypeError("Solo puede buscar int o casilla")
        for cas in self.grupo:
            if buscado == cas.valor:
                return True
        return False

    def __iter__(self):
        yield from self.grupo

    def __getitem__(self, key):
        return self.grupo[key]

    def __len__(self):
        return len(self.grupo)

    def copiar(self):
        copia = []
        for casilla in self.grupo:
            copia.append(casilla.copiar())
        return grupoCasillas(copia)

class sudoku:
    def __init__(self, filas = None):
        if filas == None:
            filas = self.crearFilasVacias()
        self.llenarValores(filas)
        self.verificacion = True

    def crearFilasVacias(self):
        return [grupoCasillas(9) for i in range(9)]

    def llenarValores(self, filas):
        assert len(filas) == 9
        self.filas = filas
        self.iniciarColumnas()
        self.iniciarSubCuadros()        

    def iniciarColumnas(self):
        assert self.filas != None
        assert len(self.filas) == 9
        self.columnas = []
        for y in range(9):
            tempg = []
            for x in range(9):
                tempg.append(self.filas[x][y])
            self.columnas.append(grupoCasillas(tempg))

    def iniciarSubCuadros(self):
        assert self.filas != None
        assert len(self.filas) == 9
        self.subcuadros = []
        for cuadro in range(9):
            cx, cy = traducirNumCuadroCoord9(cuadro)
            tempg = []
            for elem in range(9):
                sx, sy = traducirNumCuadroCoord9(elem)
                x = (cx * 3) + sx
                y = (cy * 3) + sy
                tempg.append(self.filas[x][y])
            self.subcuadros.append(tempg)

    def ponerVerificacion(self, val):
        self.verificacion = val

    def limpiar(self):
        for fila in self.filas:
            for cas in fila:
                cas.limpiar()

    def mostrar(self):
        salida = "\n"
        cv = 0 # contador valor
        cf = 0 # contador fila
        for fila in self.filas:
            for cas in fila:
                if not es1al9(cas.valor):
                    salida += " "
                else:
                    salida += str(cas.valor)
                cv += 1
                if ((cv % 3) == 0) and ((cv % 9) != 0):
                    salida += "|"
            salida += "\n"
            cf += 1
            if ((cf % 3) == 0) and ((cf % 9) != 0):
                salida += (
                    ("-" * 3)
                    + (("+" + ("-" * 3)) * 2)
                    + "\n")
        return salida

    def ponerValor(self, x, y, val):
        if ((val == None)
            or (self.filas[x][y].tipo == TIPO_FIJO)):
            return
        if (val != 0) and self.verificacion:
            numCuadro = self.filas[x][y].valor
            if ((val in self.filas[x])
                or (val in self.columnas[y])
                or (val in self.subcuadros[numCuadro])):
                raise ValueError(
                    ("El valor {} ya está en la "
                     + "fila, columna o subcuadro.")
                    .format(val))
        self.filas[x][y].valor = val

    def copiar(self):
        nuevasfilas = []
        for fila in self.filas:
            nuevasfilas.append(fila.copiar())
        copia = sudoku(nuevasfilas)
        return copia

    def ponerTodosONinguno(sujeto):
        def poniendoTodosONinguno(self, *params, **kparams):
            temp = self.copiar()
            try:
                sujeto(self, *params, **kparams)
            except ValueError:
                self.llenarValores(temp.filas)
                raise
        return poniendoTodosONinguno

    @ponerTodosONinguno
    def ponerFila(self, f, vals):
        assert vals != None
        assert type(vals) is list
        assert (len(vals) >= 1) and (len(vals) <= 9)
        ceros = [0] * len(vals)
        for j in [ceros, vals]:
            for i in range(len(vals)):
                self.ponerValor(f, i, j[i])

    @ponerTodosONinguno
    def ponerColumna(self, c, vals):
        assert vals != None
        assert type(vals) is list
        assert (len(vals) >= 1) and (len(vals) <= 9)
        ceros = [0] * len(vals)
        for j in [ceros, vals]:
            for i in range(len(vals)):
                self.ponerValor(i, c, j[i])
    
    @ponerTodosONinguno
    def ponerSubcuadro(self, n, vals):
        assert vals != None
        assert type(vals) is list
        assert (len(vals) >= 1) and (len(vals) <= 9)
        cx, cy = traducirNumCuadroCoord9(n)
        ceros = [0] * len(vals)
        for j in [ceros, vals]:
            for i in range(len(vals)):
                x, y = traducirNumCuadroCoord9(i)
                x, y = (cx * 3) + x, (cy * 3) + y
                self.ponerValor(x, y, j[i])

    @ponerTodosONinguno
    def ponerTodos(self, vals):
        assert vals != None
        assert type(vals) is list
        assert (len(vals) >= 1) and (len(vals) <= 81)
        ceros = [0] * len(vals)
        for j in [ceros, vals]:
            for i in range(len(vals)):
                x, y = traducirNumCuadroCoord(i)
                self.ponerValor(x, y, j[i])

    def fijarCuadro(self):
        assert self.filas != None
        assert len(self.filas) == 9
        for fila in self.filas:
            for cas in fila:
                if cas.valor > 0:
                    cas.tipo = TIPO_FIJO
