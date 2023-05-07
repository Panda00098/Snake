import pgzrun
import copy
import random
import time
import math
import collections

pocet_pixelu = 10
vyska = 50  #50
sirka = 100  #100
WIDTH = pocet_pixelu * sirka
HEIGHT = pocet_pixelu * (vyska + 2)
velikost_hada = 5
had_souradnice = []
hlava_hada = []
pole = []
smer = [1, 1]
point_collected = False
spawned = False
konec = False
escaped = True
started = False
bot = True
cesta = collections.deque()
nacteno = 0
souradky_pointu = [0, 0]
for y in range(vyska):
    radek = []
    for x in range(sirka):
        had_a_had_hledani = [0, 0]
        radek.append(had_a_had_hledani)
    pole.append(radek)
for had in range(velikost_hada):
    hlava_hada = [int(vyska / 2), int(sirka / 2) + had - 2]
    had_souradnice.append(hlava_hada)
for had in range(velikost_hada):
    pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1


def pohyb():
    global hlava_hada, pole, point_collected, velikost_hada, spawned, konec, escaped
    if not bot:
        if smer[0] == 0:
            if can_move(hlava_hada[0] + smer[1], hlava_hada[1], "pohyb"):
                hlava_hada_neco = copy.deepcopy(hlava_hada)
                hlava_hada_neco[smer[0]] += smer[1]
                if not point_collected:
                    odpad = had_souradnice.pop(0)
                    pole[odpad[0]][odpad[1]][0] = 0
                point_collected = False
                had_souradnice.append(hlava_hada_neco)
                hlava_hada = copy.deepcopy(hlava_hada_neco)
                for had in range(velikost_hada):
                    pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1
                if hlava_hada == souradky_pointu:
                    point_collected = True
                    spawned = False
                    velikost_hada += 1
                    point_spawn()
            else:
                konec = True
                escaped = True
                konec_hry()
                clock.unschedule(pohyb)
        else:
            if can_move(hlava_hada[0], hlava_hada[1] + smer[1], "pohyb"):
                hlava_hada_neco = copy.deepcopy(hlava_hada)
                hlava_hada_neco[smer[0]] += smer[1]
                if not point_collected:
                    odpad = had_souradnice.pop(0)
                    pole[odpad[0]][odpad[1]][0] = 0
                point_collected = False
                had_souradnice.append(hlava_hada_neco)
                hlava_hada = copy.deepcopy(hlava_hada_neco)
                for had in range(velikost_hada):
                    pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1
                if hlava_hada == souradky_pointu:
                    point_collected = True
                    spawned = False
                    velikost_hada += 1
                    point_spawn()
            else:
                konec = True
                escaped = True
                konec_hry()
                clock.unschedule(pohyb)
    else:
        for x in range(nacteno):
            misto = cesta.pop()
            had_souradnice.append(misto)
            if not point_collected:
                odpad = had_souradnice.pop(0)
                pole[odpad[0]][odpad[1]][0] = 0
            point_collected = False
            for had in range(velikost_hada):
                pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1
            if hlava_hada == souradky_pointu:
                point_collected = True
                spawned = False
                velikost_hada += 1
                point_spawn()

def can_move(y, x, kdo):
    if y < 0 or x < 0:
        return False
    if kdo == "pohyb":
        try:
            if pole[y][x] != 1:
                return True
            else:
                return False
        except IndexError:
            return False
    if kdo == "smer":
        if had_souradnice[velikost_hada - 2][0] == y and had_souradnice[velikost_hada - 2][1] == x:
            return False
        else:
            return True
    return True

def konec_hry():
    global hlava_hada, smer, point_collected, spawned, konec, escaped, started, souradky_pointu, pole, had_souradnice, velikost_hada
    velikost_hada = 5
    had_souradnice = []
    hlava_hada = []
    pole = []
    smer = [1, 1]
    point_collected = False
    spawned = False
    konec = False
    escaped = True
    started = False
    souradky_pointu = [0, 0]
    for y in range(vyska):
        radek = []
        for x in range(sirka):
            radek.append(0)
        pole.append(radek)
    for had in range(velikost_hada):
        hlava_hada = [int(vyska / 2), int(sirka / 2) + had - 2]
        had_souradnice.append(hlava_hada)
    for had in range(velikost_hada):
        pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1

def point_spawn():
    global spawned, souradky_pointu
    while not spawned:
        x = random.randint(0, sirka - 1)
        y = random.randint(0, vyska - 1)
        if pole[y][x][0] == 0:
            spawned = True
            pole[y][x][0] = 2
            souradky_pointu = [y, x]
            if bot:
                hledani_cesty()

def hledani_cesty():
    global cesta, nacteno
    breakout = True
    doba_trvani = 0
    nacteno = 0
    print("here")
    neighbours = collections.deque()
    while breakout:
        print("sem ano")
        if doba_trvani == 0:
            doba_trvani = 1
            print("jsem zde")
            for y in range(2):
                for x in range(2):
                    if pole[hlava_hada[0] + y * 2 - 1][hlava_hada[1] + x * 2 - 1][0] != 1:
                        pole[hlava_hada[0] + y * 2 - 1][hlava_hada[1] + x * 2 - 1][1] = 1
                        soused = [hlava_hada[0] + y * 2 - 1, hlava_hada[1] + x * 2 - 1]
                        neighbours.append(soused)
                    if hlava_hada[0] + y * 2 - 1 == souradky_pointu[0] and hlava_hada[1] + x * 2 - 1 == souradky_pointu:
                        poradi = pole[hlava_hada[0]][hlava_hada[1]][1] + 1
                        pole[hlava_hada[0] + y * 2 - 1][hlava_hada[1] + x * 2 - 1][1] = poradi
                        breakout = True
                if breakout:
                    break
            if breakout:
                print("ahoj")
                break
        else:
            pozice = neighbours.popleft
            for y in range(2):
                for x in range(2):
                    if pozice[0] + y * 2 - 1 == souradky_pointu[0] and pozice[1] + x * 2 - 1 == souradky_pointu:
                        poradi = pole[pozice[0]][pozice[1]][1] + 1
                        pole[pozice[0] + y * 2 - 1][pozice[1] + x * 2 - 1][1] = poradi
                        breakout = False
                    if pole[pozice[0] + y * 2 - 1][pozice[1] + x * 2 - 1][0] != 0 and pole[pozice[0] + y * 2 - 1][pozice[1] + x * 2 - 1][0] == 0:
                        poradi = pole[pozice[0]][pozice[1]][1] + 1
                        pole[pozice[0] + y * 2 - 1][pozice[1] + x * 2 - 1][1] = poradi
                        soused = [pozice[0] + y * 2 - 1, pozice[1] + x * 2 - 1]
                        neighbours.append(soused)
                if breakout:
                    break
            if breakout:
                print("ahoj po druhy")
                break

    for y in range(2):
        for x in range(2):
            if pole[souradky_pointu[0]][souradky_pointu[1]][0] != 0:
                if pole[souradky_pointu[0] + y * 2 - 1][souradky_pointu[1] + x * 2 - 1][1] == pole[souradky_pointu[0]][souradky_pointu[1]][1] - 1:
                    pozice = [souradky_pointu[0] + y * 2 - 1, souradky_pointu[1] + x * 2 - 1]
                    cesta = collections.deque()
                    cesta.append(pozice)
            else:
                pozice = neighbours[nacteno]
                if pole[pozice[0] + y * 2 - 1][pozice[1] + x * 2 - 1][1] == pole[pozice[0]][pozice[1]][1]:
                    pozice = [pozice[0] + y * 2 - 1, pozice[1] + x * 2 - 1]
                    nacteno += 1
                    cesta.append(pozice)

    for y in range(vyska):
        for x in range(sirka):
            if pole[y][x][1] != 0:
                pole[y][x][1] = 0
    print("cs")


def on_key_down(key):
    global smer, escaped, aktualnicas, casovac, started
    if escaped:
        if key == 32:
            casovac = time.time()
            if started:
                casovac -= aktualnicas
            if not started:
                point_spawn()
                started = True
            clock.schedule_interval(pohyb, 0.1)
            escaped = False
    if not escaped:
        if key == 119 or key == keys.UP:
            if can_move(hlava_hada[0] - 1, hlava_hada[1], "smer"):
                smer[0] = 0
                smer[1] = -1
        if key == 115 or key == keys.DOWN:
            if can_move(hlava_hada[0] + 1, hlava_hada[1], "smer"):
                smer[0] = 0
                smer[1] = 1
        if key == 100 or key == keys.RIGHT:
            if can_move(hlava_hada[0], hlava_hada[1] + 1, "smer"):
                smer[0] = 1
                smer[1] = 1
        if key == 97 or key == keys.LEFT:
            if can_move(hlava_hada[0], hlava_hada[1] - 1, "smer"):
                smer[0] = 1
                smer[1] = -1
        if key == keys.ESCAPE:
            escaped = True
            clock.unschedule(pohyb)


def update():
    draw()

def draw():
    global aktualnicas
    screen.clear()
    if not konec:
        for y, radek in enumerate(pole):
            for x, had in enumerate(radek):
                if had[0] == 0:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0x00, 0x00, 0x00))
                if had[0] == 1:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0xff, 0xff, 0x00))
                if had[0] == 2:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0xfe, 0x01, 0x9a))
    screen.draw.line((0, vyska * pocet_pixelu), ((sirka + 1) * pocet_pixelu, vyska * pocet_pixelu), (0xff, 0xff, 0xff))
    if escaped:
        screen.draw.text("PRESS SPACE", ((sirka / 2 - 7) * pocet_pixelu, (vyska / 2 - 2) * pocet_pixelu), color="white", fontsize=30/10 * pocet_pixelu)
    if not escaped:
        if started or not escaped:
            aktualnicas = time.time() - casovac
            cashms = time.strftime("%H:%M:%S", time.gmtime(aktualnicas))
            milisec = (aktualnicas - math.floor(aktualnicas)) * 1000
            milisec = math.floor(milisec)
            screen.draw.text(("time: " + cashms + ":" + str(milisec)), (1 * pocet_pixelu, vyska * pocet_pixelu),
                             color="green", fontsize=pocet_pixelu * (24 / 10))
    if escaped:
        screen.draw.text("time: 00:00:00:000", (1 * pocet_pixelu, vyska * pocet_pixelu),
                         color="green", fontsize=pocet_pixelu * (24 / 10))
pgzrun.go()