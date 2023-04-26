import pgzrun
import copy
import random

pocet_pixelu = 10
vyska = 30
sirka = 30
WIDTH = pocet_pixelu * sirka
HEIGHT = pocet_pixelu * vyska
velikost_hada = 5
had_souradnice = []
hlava_hada = []
pole = []
smer = [1, 1]
point_collected = False
spawned = False
konec = False
escaped = True
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
    pole[had_souradnice[had][0]][had_souradnice[had][1]] = 1


def pohyb():
    global hlava_hada, pole, point_collected, velikost_hada, spawned, konec, escaped
    if smer[0] == 0:
        if can_move(hlava_hada[0] + smer[1], hlava_hada[1], "pohyb"):
            hlava_hada_neco = copy.deepcopy(hlava_hada)
            hlava_hada_neco[smer[0]] += smer[1]
            if not point_collected:
                odpad = had_souradnice.pop(0)
                pole[odpad[0]][odpad[1]] = 0
            point_collected = False
            had_souradnice.append(hlava_hada_neco)
            hlava_hada = copy.deepcopy(hlava_hada_neco)
            for had in range(velikost_hada):
                pole[had_souradnice[had][0]][had_souradnice[had][1]] = 1
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
                pole[odpad[0]][odpad[1]] = 0
            point_collected = False
            had_souradnice.append(hlava_hada_neco)
            hlava_hada = copy.deepcopy(hlava_hada_neco)
            for had in range(velikost_hada):
                pole[had_souradnice[had][0]][had_souradnice[had][1]] = 1
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

def can_move(y, x, kdo):
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
        pole[had_souradnice[had][0]][had_souradnice[had][1]] = 1

def point_spawn():
    global spawned, souradky_pointu
    while not spawned:
        x = random.randint(0, sirka - 1)
        y = random.randint(0, vyska - 1)
        if pole[y][x] == 0:
            spawned = True
            pole[y][x] = 2
            souradky_pointu = [y, x]

def on_key_down(key):
    global smer, escaped
    if escaped:
        if key == 32:
            escaped = False
            point_spawn()
            clock.schedule_interval(pohyb, 0.5)
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


#def update():
#    draw()

def draw():
    global started
    screen.clear()
    if not konec:
        for y, radek in enumerate(pole):
            for x, had in enumerate(radek):
                if had == 0:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0x00, 0x00, 0x00))
                if had == 1:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0xff, 0xff, 0x00))
                if had == 2:
                    r = Rect((x * pocet_pixelu, y * pocet_pixelu), (pocet_pixelu, pocet_pixelu))
                    screen.draw.filled_rect(r, (0xfe, 0x01, 0x9a))
    if escaped:
        screen.draw.text("PRESS SPACE", ((sirka / 2 - 7) * pocet_pixelu, (vyska / 2 - 2) * pocet_pixelu), color="white", fontsize=30/10 * pocet_pixelu)

pgzrun.go()