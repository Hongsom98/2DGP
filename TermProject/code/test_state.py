import random
import gfw
from pico2d import *
import gobj
from player import Player
from background import HorzScrollBackground
from platform import Platform
import HPui
import stage_gen

canvas_width = 1120
canvas_height = 630
SCORE_TEXT_COLOR = (255, 255, 255)

def enter(select):
    gfw.world.init(['bg', 'platform', 'enemy', 'item', 'player', 'ui'])

    center = get_canvas_width() // 2, get_canvas_height() // 2

    for n, speed in [(1,10), (2,100)]:
        bg = HorzScrollBackground('Episode01_bg_0%d.png' % n)
        bg.speed = speed
        gfw.world.add(gfw.layer.bg, bg)

    global player
    player = Player(select)
    player.bg = bg
    gfw.world.add(gfw.layer.player, player)

    global ui
    ui= HPui.Hpui(0.05)
    gfw.world.add(gfw.layer.ui, ui)

    stage_gen.load(gobj.res('stage_01.txt'))
    global font, score
    font = gfw.font.load('res/CookieRun Regular.ttf', 35)
    score = 0

    global runfast, fast_time
    runfast = False
    fast_time = None

paused = False
def update():
    if paused:
        return
    gfw.world.update()

    dx = -300 * gfw.delta_time
    global runfast, fast_time
    for layer in range(gfw.layer.platform, gfw.layer.item + 1):
        for obj in gfw.world.objects_at(layer):
            if runfast:
                obj.move(dx * 2)
            else:
                obj.move(dx)
    if fast_time != None and get_time() - fast_time >= 3.5:
       runfast = False

    check_items()
    check_obstacles()
    stage_gen.update(dx)
    check_game_over()

def check_game_over():
    fall = player.get_fall()
    hp_over = False
    if ui.width < 67:
        hp_over = True
    if fall or hp_over:
        print(fall, hp_over)
        gfw.quit()

def check_items():
    for item in gfw.world.objects_at(gfw.layer.item):
        if gobj.collides_box(player, item):
            if item.get_type() < 4:
                global score
                score += 100
            elif item.get_type() == 4:
                global runfast, fast_time
                runfast = True
                fast_time = get_time()
                pass
            elif item.get_type() == 5:
                player.magnify()
                pass
            elif item.get_type() == 6:
                ui.hp()
                pass
            #elif item.get_type() == 7:
            #    pass
            #elif item.get_type() == 8:
            #    pass
            gfw.world.remove(item)
            break

def check_obstacles():
    for enemy in gfw.world.objects_at(gfw.layer.enemy):
        if enemy.hit: continue
        if gobj.collides_box(player, enemy):
            if not player.state == 5:
                if not player.get_super():
                    player.state = 5
                    ui.player_colide()
                enemy.hit = True

def draw():
    gfw.world.draw()
    gobj.draw_collision_box()
    score_pos = 30, get_canvas_height() - 30
    global score
    font.draw(*score_pos, 'Score : %0d' % score, SCORE_TEXT_COLOR)

def handle_event(e):
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
            return
        elif e.key == SDLK_a:
            # player.pos = 150,650
            # for x, y in [(100,400),(400,300),(650,250),(900,200)]:
            for i in range(10):
                x = random.randint(100, 900)
                y = random.randint(200, 400)
                pf = Platform(Platform.T_3x1, x, y)
                gfw.world.add(gfw.layer.platform, pf)
        elif e.key == SDLK_p:
            global paused
            paused = not paused

    if player.handle_event(e):
        return

def exit():
    pass



if __name__ == '__main__':
    gfw.run_main()
