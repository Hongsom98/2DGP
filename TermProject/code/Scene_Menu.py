from pico2d import *
import gfw
import test_state
from background import HorzScrollBackground

canvas_width = 1120
canvas_height = 630

mouse = (0,0)
select = None

def enter(select):
    global bg1, bg2, brave, bright#, cursor
    global bravex, bravey, bravesize
    global brightx, brighty, brightsize
    bg1 = HorzScrollBackground('Menu_bg_01.png')
    bg1.speed = 10
    bg2 = HorzScrollBackground('Menu_bg_02.png')
    bg2.speed = 50
    brave = load_image('./res/Menu_cookie_01.png')
    bright = load_image('./res/Menu_cookie_02.png')
    #cursor = load_image('./res/Menu_cursor.png')

    bravex = 0
    bravey = 270
    brightx = 0
    brighty = 288
    bravesize = (270,270)
    brightsize = (288, 288)
    show_cursor()
    pass

def exit():
    global brave, bright
    del brave
    del bright
    pass

def update():
    global bg1, bg2
    global bravex, bravey
    global brightx, brighty
    global select
    bg1.update()
    bg2.update()

    bravex += 272
    if bravex > 1086:
        bravex = 0
    brightx += 290
    if brightx > 1158:
        brightx = 0

    if mouse[0] > 50 and mouse[0] < 150 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = -1
        bravey = 0
        brighty = 288
    elif mouse[0] > 250 and mouse[0] < 350 and mouse[1] > canvas_height / 2 and mouse[1] < canvas_height / 2 + 270:
        select = 0
        brighty = 0
        bravey = 270


    delay(0.03)
    pass

def draw():
    global bg1, bg2, brave, bright
    global bravex, bravey, bravesize
    global brightx, brighty, brightsize
    bg1.draw()
    bg2.draw()
    brave.clip_draw(bravex, bravey, *bravesize, 100, canvas_height / 2)
    bright.clip_draw(brightx, brighty, *brightsize, 300, canvas_height / 2)
    pass

def handle_event(e):
    global mouse, select
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.change(test_state)
            return
        elif e.key == SDLK_RETURN:
            gfw.change(test_state, select)
    elif e.type == SDL_MOUSEBUTTONDOWN:
        mouse = (e.x, e.y)
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
