import random
import gfw
from pico2d import *
import gobj
from player import Player
from background import HorzScrollBackground
from floor import Platform
import HPui
import stage_gen
import Scene_Result

canvas_width = 1120
canvas_height = 630
SCORE_TEXT_COLOR = (255, 255, 255)

def enter(select):
    gfw.world.init(['bg', 'platform', 'enemy', 'item', 'player', 'ui'])
    global bgm, effect_j, effect_s, effect_jelly, effect_hp, effect_obs
    bgm = load_music('./res/Cookie Run Ovenbreak - Theme Song Breakout 1.mp3')
    if select == -1:
        effect_j = load_wav('res/ch02jump.wav')
        effect_s = load_wav('res/ch01slide.wav')
    elif select == 0:
        effect_j = load_wav('res/ch02jump.wav')
        effect_s = load_wav('res/ch02slide.wav')
    elif select == 5:
        effect_j = load_wav('res/ch07jump.wav')
        effect_s = load_wav('res/ch07slide.wav ')
    elif select == 14:
        effect_j = load_wav('res/ch02jump.wav')
        effect_s = load_wav('res/ch01slide.wav')
    elif select == 3:
        effect_j = load_wav('res/ch05jump.wav')
        effect_s = load_wav('res/ch05slide.wav')
    effect_jelly = load_wav('res/g_jelly.wav')
    effect_hp = load_wav('res/i_small_energy.wav')
    effect_obs = load_wav('res/g_obs1.wav')

    effect_s.get_volume()
    effect_j.get_volume()
    effect_jelly.get_volume()
    effect_hp.get_volume()
    effect_obs.get_volume()
    bgm.get_volume()

    bgm.repeat_play()

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
    if player.select == 3:
        ui.set_dwidth(1, 0.05)
    gfw.world.add(gfw.layer.ui, ui)

    stage_gen.load(gobj.res('stage_01.txt'))
    global font, score, targetscore
    font = gfw.font.load('res/CookieRun Regular.ttf', 35)
    score = 0
    targetscore = 0

    global runfast, fast_time
    runfast = False
    fast_time = None



paused = False
def update():
    global score, targetscore
    if player.state == 6:
        for pobj in gfw.world.objects_at(gfw.layer.player):
            pobj.update()
            #print(pobj.get_gameover())
            if pobj.get_gameover() == 20:
                Scene_Result.set_score(score)
                gfw.change(Scene_Result, player.select)
        return
    gfw.world.update()

    dx = -300 * gfw.delta_time
    global runfast, fast_time
    for layer in range(gfw.layer.platform, gfw.layer.item + 1):
        for obj in gfw.world.objects_at(layer):
            if runfast:
                obj.move(dx * 2)
            elif player.select == 5:
                obj.move(dx * 1.5)
            else:
                obj.move(dx)
    if fast_time != None and get_time() - fast_time >= 3.5:
       runfast = False

    if score < targetscore:
        score += 9

    if player.magnet == True:
        magnet_activate(500, 0.05)
    if player.select == 14:
        magnet_activate(300, 0.01)

    check_items()
    check_obstacles()
    if runfast:
        stage_gen.update(dx * 2)
    elif player.select == 5:
        stage_gen.update(dx * 1.5)
    else:
        stage_gen.update(dx)
    check_game_over()

def check_game_over():
    fall = player.get_fall()
    hp_over = False
    if ui.width < 67:
        Player.state = 6
    if fall:
        Scene_Result.set_score(score)
        gfw.change(Scene_Result, player.select)

def check_items():
    for item in gfw.world.objects_at(gfw.layer.item):
        if gobj.collides_box(player, item):
            if item.get_type() < 4:
                global targetscore
                targetscore += 100
                effect_jelly.play(1)
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
                effect_hp.play(1)
                pass
            elif item.get_type() == 7:
                player.magnet = True
                player.magnet_time = get_time()

            #elif item.get_type() == 7:
            #    pass
            #elif item.get_type() == 8:
            #    pass
            gfw.world.remove(item)
            break

def magnet_activate(a, b):
    for jelly in gfw.world.objects_at(gfw.layer.item):
        if jelly.get_type() < 4:
            dx, dy = player.pos[0] - jelly.x, player.pos[1] - jelly.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance == 0:
                return
            elif distance <= a:
                jelly.x -= b * player.pos[0]
                jelly.y += b * ( dy - 40)
                #print(player.pos[1])

def check_obstacles():
    for enemy in gfw.world.objects_at(gfw.layer.enemy):
        if enemy.hit: continue
        if gobj.collides_box(player, enemy):
            if not player.state == 5:
                if not player.get_super():
                    player.state = 5
                    ui.player_colide()
                    effect_obs.play(1)
                enemy.hit = True

def draw():
    gfw.world.draw()
    #gobj.draw_collision_box()
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
            Scene_Result.set_score(score)
            gfw.change(Scene_Result, player.select)
            return
        elif e.key == SDLK_RETURN:
            effect_s.play(1)
        elif e.key == SDLK_SPACE:
            effect_j.play(1)
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
    global bgm
    del bgm
    pass



if __name__ == '__main__':
    gfw.run_main()
