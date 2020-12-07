from pico2d import *
import gfw
import Scene_game
from background import HorzScrollBackground

canvas_width = 1120
canvas_height = 630

mouse = (0,0)
select = None

def enter(select):
    global bg1, bg2, ui_start
    global brave, bright, zombie, angle, coonku
    global bravex, bravey, bravesize
    global brightx, brighty, brightsize
    global zombiex, zombiey, zombiesize
    global anglex, angley, anglesize
    global coonkux, coonkuy, coonkusize
    global bgm, effect
    bg1 = HorzScrollBackground('Menu_bg_01.png')
    bg1.speed = 10
    bg2 = HorzScrollBackground('Menu_bg_02.png')
    bg2.speed = 50
    brave = load_image('./res/Menu_cookie_01.png')
    bright = load_image('./res/Menu_cookie_02.png')
    zombie = load_image('./res/Menu_cookie_03.png')
    angle = load_image('./res/Menu_cookie_04.png')
    coonku = load_image('./res/Menu_cookie_05.png')
    ui_start = load_image('./res/play.png')

    bravex = 0
    bravey = 270
    bravesize = (270, 270)

    brightx = 0
    brighty = 288
    brightsize = (288, 288)

    zombiex = 0
    zombiey = 360
    zombiesize = (360, 360)

    anglex = 0
    angley = 320
    anglesize = (320, 320)

    coonkux = 0
    coonkuy = 344
    coonkusize = (344, 344)
    show_cursor()

    bgm = load_wav('./res/bgm_main_rockstar.wav')
    bgm.get_volume()
    bgm.repeat_play()

    effect = load_wav('./res/ui_3.wav')
    effect.get_volume()
    pass

def exit():
    global brave, bright, zombie, angle, coonku, bgm, effect
    global mouse, oldmouse
    del brave
    del bright
    del zombie
    del angle
    del coonku
    del bgm
    del effect
    mouse = (0,0)
    oldmouse = (0,0)
    pass

def update():
    global bg1, bg2
    global bravex, bravey
    global brightx, brighty
    global zombiex, zombiey
    global anglex, angley
    global coonkux, coonkuy
    global select
    global effect
    global oldmouse
    bg1.update()
    bg2.update()

    bravex += 272
    if bravex > 1086:
        bravex = 0
    brightx += 290
    if brightx > 1158:
        brightx = 0
    zombiex += 362
    if zombiex > 1446:
        zombiex = 0
    anglex += 322
    if anglex > 1286:
        anglex = 0
    coonkux += 346
    if coonkux > 1382:
        coonkux = 0


    if mouse[0] > 405 and mouse[0] < 650 and mouse[1] > 550 and mouse[1] < 610:
        if oldmouse != mouse:
            effect.play(1)
        gfw.change(Scene_game, select)
    elif mouse[0] > 50 and mouse[0] < 150 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = -1
        bravey = 0
        brighty = 288
        zombiey = 360
        angley = 320
        coonkuy = 344
        if oldmouse != mouse:
            effect.play(1)
    elif mouse[0] > 250 and mouse[0] < 350 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = 0
        brighty = 0
        bravey = 270
        zombiey = 360
        angley = 320
        coonkuy = 344
        if oldmouse != mouse:
            effect.play(1)
    elif mouse[0] > 450 and mouse[0] < 550 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = 5
        zombiey = 0
        bravey = 270
        brighty = 288
        angley = 320
        coonkuy = 344
        if oldmouse != mouse:
            effect.play(1)
    elif mouse[0] > 650 and mouse[0] < 750 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = 14
        angley = 0
        bravey = 270
        brighty = 288
        zombiey = 360
        coonkuy = 344
        if oldmouse != mouse:
            effect.play(1)
    elif mouse[0] > 850 and mouse[0] < 950 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 200:
        select = 3
        coonkuy = 0
        bravey = 270
        brighty = 288
        zombiey = 360
        angley = 320
        if oldmouse != mouse:
            effect.play(1)


    oldmouse = mouse
    delay(0.03)
    pass

def draw():
    global bg1, bg2, ui_start
    global brave, bright, zombie, angle, coonku
    global bravex, bravey, bravesize
    global brightx, brighty, brightsize
    global zombiex, zombiey, zombiesize
    global anglex, angley, anglesize
    global coonkux, coonkuy, coonkusize
    bg1.draw()
    bg2.draw()
    brave.clip_draw(bravex, bravey, *bravesize, 100, canvas_height / 2)
    bright.clip_draw(brightx, brighty, *brightsize, 300, canvas_height / 2)
    zombie.clip_draw(zombiex, zombiey, *zombiesize, 500, canvas_height / 2, 300, 300)
    angle.clip_draw(anglex, angley, *anglesize, 700, canvas_height / 2)
    coonku.clip_draw(coonkux, coonkuy, *coonkusize, 900, canvas_height / 2, 300, 300)

    ui_start.clip_draw(0, 0, 300, 85, canvas_width / 2 - 30, 50)
    pass

def handle_event(e):
    global mouse, select
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.quit()
            return
        elif e.key == SDLK_RETURN:
            gfw.change(test_state, select)
    elif e.type == SDL_MOUSEBUTTONDOWN:
        print(e.x, e.y)
        mouse = (e.x, e.y)
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
