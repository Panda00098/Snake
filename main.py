import pgzrun
import copy
import random
import time
import math
import collections

pocet_pixelu = 10
vyska = 10  #50
sirka = 10  #100
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
        if y == 480 or y == 200:
            if x == 900 or x == 182:
                had_a_had_hledani = [3, 0]
                radek.append(had_a_had_hledani)
            else:
                had_a_had_hledani = [0, 0]
                radek.append(had_a_had_hledani)
        else:
            had_a_had_hledani = [0, 0]
            radek.append(had_a_had_hledani)
    pole.append(radek)
for had in range(velikost_hada):
    hlava_hada = [round(vyska / 2), round(sirka / 2) + had - 2]
    had_souradnice.append(hlava_hada)
    print(hlava_hada)
for had in range(velikost_hada):
    pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1
print(had_souradnice)


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
        try:
            misto = cesta.pop()
            had_souradnice.append(misto)
            if not point_collected:
                odpad = had_souradnice.pop(0)
                pole[odpad[0]][odpad[1]][0] = 0
            point_collected = False
            for had in range(velikost_hada):
                pole[had_souradnice[had][0]][had_souradnice[had][1]][0] = 1
            hlava_hada = misto
            if hlava_hada == souradky_pointu:
                spawned = False
                point_spawn()
        except IndexError:
            point_collected = True
            velikost_hada += 1
#            point_spawn()
            hledani_cesty()

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
#            if bot:
#                hledani_cesty()

def hledani_cesty():
    global cesta, nacteno
    breakout = False
    na_hlave = False
#    doba_trvani = 0
    nacteno = 0
    scitani = 0
    pole_z_wishe = copy.deepcopy(pole)
    neighbours = collections.deque()
    neighbours.append(hlava_hada)
    cesta = collections.deque()
    cesta.append(souradky_pointu)
    if spawned:
        while not breakout:
            pozice = neighbours.popleft()
            for sx, sy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                y = pozice[0] + sy
                x = pozice[1] + sx
                if x < 0 or x >= sirka or y < 0 or y >= vyska:
                    continue
                if souradky_pointu == [y, x]:
                    pole_z_wishe[y][x][1] = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
                    breakout = True
                if pole_z_wishe[y][x][1] == 0 and pole_z_wishe[y][x][0] != 1:
                    pole_z_wishe[y][x][1] = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
                    if velikost_hada - 1 >= pole_z_wishe[y][x][1]:
                        pole_z_wishe[had_souradnice[pole_z_wishe[y][x][0]][0]][had_souradnice[pole_z_wishe[y][x][0]][1]][0] = 0
                    neighbours.append([y, x])
#            if doba_trvani == 0:
#                doba_trvani = 1
#                for sx, sy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
#                   y = hlava_hada[0] + sy
#                    x = hlava_hada[1] + sx
#                    if x < 0 or x >= sirka or y < 0 or y >= vyska:
#                      continue
#                   if souradky_pointu == [y, x]:
#                       pole_z_wishe[y][x][1] = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                       breakout = True
#                    if pole_z_wishe[y][x][1] == 0 and pole_z_wishe[y][x][0] != 1:
#                        pole_z_wishe[y][x][1] = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                        if velikost_hada - 1 >= pole_z_wishe[y][x][1]:
#                           pole_z_wishe[had_souradnice[pole_z_wishe[y][x][1]][0]][had_souradnice[pole_z_wishe[y][x][1]][1]][0] = 0
#                        neighbours.append([y, x])
#            else:


#                for y in range(2):
#                    for x in range(2):
#                        if y == 0:
#                            if hlava_hada[1] + x * 2 - 1 >= 0:
#                                if (hlava_hada[0] == souradky_pointu[0] and hlava_hada[1] + x * 2 - 1 == souradky_pointu[1] and
#                                        pole_z_wishe[hlava_hada[0]][hlava_hada[1] + x * 2 - 1][0] != 1):
#                                    poradi = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                                    pole_z_wishe[hlava_hada[0]][hlava_hada[1] + x * 2 - 1][1] = poradi
#                                   breakout = False
#                                try:
#                                    if pole_z_wishe[hlava_hada[0]][hlava_hada[1] + x * 2 - 1][1] == 0 and pole_z_wishe[hlava_hada[0]][hlava_hada[1] + x * 2 - 1][0] != 1:
#                                        poradi = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                                        pole_z_wishe[hlava_hada[0]][hlava_hada[1] + x * 2 - 1][1] = poradi
#                                        soused = [hlava_hada[0], hlava_hada[1] + x * 2 - 1]
#                                        if velikost_hada - 1 >= poradi:
#                                            pole_z_wishe[had_souradnice[poradi][0]][had_souradnice[poradi][1]][0] = 0
#                                        neighbours.append(soused)
#                                except IndexError:
#                                    continue
#                        if y == 1:
#                            if hlava_hada[0] + x * 2 - 1 >= 0:
#                                if (hlava_hada[0] + x * 2 - 1 == souradky_pointu[0] and hlava_hada[1] == souradky_pointu[1] and
#                                        pole_z_wishe[hlava_hada[0] + x * 2 - 1][hlava_hada[1]][0] != 1):
#                                    poradi = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                                    pole_z_wishe[hlava_hada[0] + x * 2 - 1][hlava_hada[1]][1] = poradi
#                                    breakout = False
#                                try:
#                                    if pole_z_wishe[hlava_hada[0] + x * 2 - 1][hlava_hada[1]][1] == 0 and pole_z_wishe[hlava_hada[0] + x * 2 - 1][hlava_hada[1]][0] != 1:
#                                        poradi = pole_z_wishe[hlava_hada[0]][hlava_hada[1]][1] + 1
#                                        pole_z_wishe[hlava_hada[0] + x * 2 - 1][hlava_hada[1]][1] = poradi
#                                        soused = [hlava_hada[0] + x * 2 - 1, hlava_hada[1]]
#                                        if velikost_hada - 1 >= poradi:
#                                            pole_z_wishe[had_souradnice[poradi][0]][had_souradnice[poradi][1]][0] = 0
#                                        neighbours.append(soused)
#                                except IndexError:
#                                    continue
#                    if not breakout:
#                        break
#                if not breakout:
#                    break
#            else:
#                print(neighbours)
#                pozice = neighbours.popleft()
#                for y in range(2):
#                    for x in range(2):
#                        if y == 0:
#                           if pozice[1] + x * 2 - 1 >= 0:
#                               try:
#                                    if pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][0] == 2:
#                                        poradi = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
#                                        pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][1] = poradi
#                                        breakout = False
#                                        break
#                                    if pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][1] == 0 and pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][0] != 1:
#                                        poradi = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
#                                        pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][1] = poradi
#                                        soused = [pozice[0], pozice[1] + x * 2 - 1]
#                                        if velikost_hada - 1 >= poradi:
#                                            pole_z_wishe[had_souradnice[poradi][0]][had_souradnice[poradi][1]][0] = 0
#                                        neighbours.append(soused)
#                                except IndexError:
#                                    continue
#                        if y == 1:
#                            if pozice[0] + x * 2 - 1 >= 0:
#                                try:
#                                    if pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][0] == 2:
#                                        poradi = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
#                                        pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][1] = poradi
#                                        breakout = False
#                                        break
#                                    if pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][1] == 0 and pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][0] != 1:
#                                       poradi = pole_z_wishe[pozice[0]][pozice[1]][1] + 1
#                                        pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][1] = poradi
#                                        soused = [pozice[0] + x * 2 - 1, pozice[1]]
#                                        if velikost_hada - 1 >= poradi:
#                                            pole_z_wishe[had_souradnice[poradi][0]][had_souradnice[poradi][1]][0] = 0
#                                        neighbours.append(soused)
#                                except IndexError:
#                                    continue
#                    if not breakout:
#                        break
#                if not breakout:
#                    break

        while not na_hlave:
            pozice = cesta.pop()
            cesta.append(pozice)
            scitani += 1
            if scitani == vyska * sirka:
                na_hlave = True
            for sx, sy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                y = pozice[0] + sy
                x = pozice[1] + sx
                if x < 0 or x >= sirka or y < 0 or y >= vyska:
                    continue
                if pole_z_wishe[y][x][1] == pole_z_wishe[pozice[0]][pozice[1]][1] - 1:
                    pole_z_wishe[pozice[0]][pozice[1]][1] = 0
                    cesta.append([y, x])
                if y == hlava_hada[0] and x == hlava_hada[1]:
                    na_hlave = True



#            for y in range(2):
#                for x in range(2):
#                    if y == 0:
#                        try:
#                            if pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] != 0:
#                                if pole_z_wishe[souradky_pointu[0]][souradky_pointu[1] + x * 2 - 1][1] == pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] - 1 and souradky_pointu[1] + x * 2 - 1 >= 0:
#                                    pozice = [souradky_pointu[0], souradky_pointu[1] + x * 2 - 1]
#                                    pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] = 0
#                                    cesta = collections.deque()
#                                    nacteno += 1
#                                    cesta.append(pozice)
#                            else:
#                                pozice = cesta.pop()
#                                if pole_z_wishe[pozice[0]][pozice[1] + x * 2 - 1][1] == pole_z_wishe[pozice[0]][pozice[1]][1] - 1 and pozice[1] + x * 2 - 1 >= 0:
#                                    cesta.append(pozice)
#                                    pole_z_wishe[pozice[0]][pozice[1]][1] = 0
#                                    pozice = [pozice[0], pozice[1] + x * 2 - 1]
#                                    nacteno += 1
#                                cesta.append(pozice)
#                        except IndexError:
#                            continue
#                        try:
#                            pozice = cesta.pop()
#                            if pozice[0] == hlava_hada[0] and pozice[1] + x * 2 - 1 == hlava_hada[1] and pozice[1] + x * 2 - 1 >= 0:
#                                na_hlave = True
#                                cesta.append(pozice)
#                                break
#                            else:
#                                cesta.append(pozice)
#                        except IndexError:
#                            continue
#                    if y == 1:
#                        try:
#                            if pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] != 0:
#                                if pole_z_wishe[souradky_pointu[0] + x * 2 - 1][souradky_pointu[1]][1] == pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] - 1 and souradky_pointu[0] + x * 2 - 1 >= 0:
#                                    pozice = [souradky_pointu[0] + x * 2 - 1, souradky_pointu[1]]
#                                    pole_z_wishe[souradky_pointu[0]][souradky_pointu[1]][1] = 0
#                                    cesta = collections.deque()
#                                    nacteno += 1
#                                    cesta.append(pozice)
#                            else:
#                                pozice = cesta.pop()
#                                if pole_z_wishe[pozice[0] + x * 2 - 1][pozice[1]][1] == pole_z_wishe[pozice[0]][pozice[1]][1] - 1 and pozice[0] + x * 2 - 1 >= 0:
#                                    cesta.append(pozice)
#                                    pole_z_wishe[pozice[0]][pozice[1]][1] = 0
#                                    pozice = [pozice[0] + x * 2 - 1, pozice[1]]
#                                    nacteno += 1
#                                cesta.append(pozice)
#                        except IndexError:
#                            continue
#                        try:
#                            pozice = cesta.pop()
#                            if pozice[0] + x * 2 - 1 == hlava_hada[0] and pozice[1] == hlava_hada[1] and pozice[0] + x * 2 - 1 >= 0:
#                                na_hlave = True
#                                cesta.append(pozice)
#                                break
#                            else:
#                                cesta.append(pozice)
#                        except IndexError:
#                            continue
#                if na_hlave:
#                        break
#            if na_hlave:
#                    break

        for y in range(vyska):
            for x in range(sirka):
                if pole[y][x][1] != 0:
                    pole[y][x][1] = 0
        cesta.appendleft(souradky_pointu)
        je_toto_hlava = cesta.pop()
        if not je_toto_hlava == hlava_hada:
            cesta.append(je_toto_hlava)
        print(souradky_pointu, cesta, hlava_hada)


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
                hledani_cesty()
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
                if had[0] == 3:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0x00, 0x00, 0xff))
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