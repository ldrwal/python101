#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np  # import biblioteki do obliczeń naukowych
import matplotlib.pyplot as plt  # import biblioteki do tworzenia wykresów
from random import randint
from time import sleep
import mcpi.minecraft as minecraft  # import modułu minecraft
import mcpi.block as block  # import modułu block

os.environ["USERNAME"] = "Steve"  # wpisz dowolną nazwę użytkownika
os.environ["COMPUTERNAME"] = "mykomp"  # wpisz dowolną nazwę komputera

mc = minecraft.Minecraft.create("192.168.1.10")  # połaczenie z symulatorem


def plac(x, y, z, roz=10, gracz=False):
    """
    Funkcja tworzy podłoże i wypełnia sześcienny obszar od podanej pozycji,
    opcjonalnie umieszcza gracza w środku.
    Parametry: x, y, z - współrzędne pozycji początkowej,
    roz - rozmiar wypełnianej przestrzeni,
    gracz - czy umieścić gracza w środku
    Wymaga: globalnych obiektów mc i block.
    """

    podloga = block.WATER
    wypelniacz = block.AIR

    # podloga i czyszczenie
    mc.setBlocks(x, y - 1, z, x + roz, y - 1, z + roz, podloga)
    mc.setBlocks(x, y, z, x + roz, y + roz, z + roz, wypelniacz)
    # umieść gracza w środku
    if gracz:
        mc.player.setPos(x + roz / 2, y + roz / 2, z + roz / 2)


def wykres(x, y, tytul="Wykres funkcji", *extra):
    """
    Funkcja wizualizuje wykres funkcji, której argumenty zawiera lista x
    a wartości lista y i ew. dodatkowe listy w parametrze *extra
    """
    if len(extra):
        plt.plot(x, y, extra[0], extra[1])  # dwa wykresy na raz
    else:
        plt.plot(x, y, "o:")
    plt.title(tytul)
    # plt.xlabel(podpis)
    plt.grid(True)
    plt.show()


def rysuj(x, y, z, blok=block.IRON_BLOCK):
    """
    Funkcja wizualizuje wykres funkcji, umieszczając bloki w pionie/poziomie
    w punktach wyznaczonych przez pary elementów list x, y lub x, z
    """
    czylista = True if len(y) > 1 else False
    for i in range(len(x)):
        if czylista:
            print(x[i], y[i])
            mc.setBlock(x[i], y[i], z[0], blok)
        else:
            print(x[i], z[i])
            mc.setBlock(x[i], y[0], z[i], blok)


def rysuj_linie(x, y, z, blok=block.IRON_BLOCK):
    """
    Funkcja wizualizuje wykres funkcji, umieszczając bloki w pionie/poziomie
    w punktach wyznaczonych przez pary elementów list x, y lub x, z
    przy użyciu metody drawLine()
    """
    import local.minecraftstuff as mcstuff
    mcfig = mcstuff.MinecraftDrawing(mc)
    czylista = True if len(y) > 1 else False
    for i in range(len(x) - 1):
        x1 = int(x[i])
        x2 = int(x[i + 1])
        if czylista:
            y1 = int(y[i])
            y2 = int(y[i + 1])
            mc.setBlock(x2, y2, z[0], block.GRASS)
            mc.setBlock(x1, y1, z[0], block.GRASS)
            mcfig.drawLine(x1, y1, z[0], x2, y2, z[0], blok)
            mc.setBlock(x2, y2, z[0], block.GRASS)
            mc.setBlock(x1, y1, z[0], block.GRASS)
            print (x1, y1, z[0], x2, y2, z[0])
        else:
            z1 = int(z[i])
            z2 = int(z[i + 1])
            mc.setBlock(x1, y[0], z1, block.GRASS)
            mc.setBlock(x2, y[0], z2, block.GRASS)
            mcfig.drawLine(x1, y[0], z1, x2, y[0], z2, blok)
            mc.setBlock(x1, y[0], z1, block.GRASS)
            mc.setBlock(x2, y[0], z2, block.GRASS)
            print (x1, y[0], z1, x2, y[0], z2)
        sleep(1)  # przerwa na reklamę :-)
    mc.setBlock(0, 1, 0, block.OBSIDIAN)
    if czylista:
        mc.setBlock(x2, y2, z[0], block.OBSIDIAN)
    else:
        mc.setBlock(x2, y[0], z2, block.OBSIDIAN)


def ruchyBrowna():

    n = int(raw_input("Ile ruchów? "))
    r = int(raw_input("Krok przesunięcia? "))

    x = y = 0
    lx = [0]  # lista odciętych
    ly = [0]  # lista rzędnych

    for i in range(0, n):
        # losujemy kąt i zamieniamy na radiany
        rad = float(randint(0, 360)) * np.pi / 180
        x = x + r * np.cos(rad)  # wylicz współrzędną x
        y = y + r * np.sin(rad)  # wylicz współrzędną y
        x = int(round(x, 2))  # zaokrągl
        y = int(round(y, 2))  # zaokrągl
        print x, y
        lx.append(x)
        ly.append(y)

    # oblicz wektor końcowego przesunięcia
    s = np.fabs(np.sqrt(x**2 + y**2))
    print "Wektor przesunięcia: {:.2f}".format(s)

    wykres(lx, ly, "Ruchy Browna")

    mc.player.setPos(x, 20, y)
    rysuj(lx, [1], ly, block.WOOL)

    import json
    plik = open('rbrowna.log', 'w')
    json.dump((lx, ly), plik)
    plik.close()


def main():
    mc.postToChat("Ruchy Browna")  # wysłanie komunikatu do mc
    plac(-80, -20, -80, 160)
    plac(-80, 0, -80, 160)
    ruchyBrowna()
    return 0


if __name__ == '__main__':
    main()
