from pico2d import *
import gfw
import Scene_Menu

canvas_width = 1120
canvas_height = 630
SCORE_TEXT_COLOR = (255, 255, 255)
fidxCnt = 0

def enter(select):
    global player, playerx, playery, playersize, playerfidx
    global bg
    global score, font, targetscore
    global bgm
    if select == -1:
        player = load_image('./res/Menu_cookie_01.png')
        playerx = 0
        playery = 270
        playerfidx = 272
        playersize = (270, 270)
    elif select == 0:
        player = load_image('./res/Menu_cookie_02.png')
        playerx = 0
        playery = 288
        playerfidx = 290
        playersize = (288, 288)
    elif select == 5:
        player = load_image('./res/Menu_cookie_03.png')
        playerx = 0
        playery = 360
        playerfidx = 362
        playersize = (360, 360)
    elif select == 14:
        player = load_image('./res/Menu_cookie_04.png')
        playerx = 0
        playery = 320
        playerfidx = 322
        playersize = (320, 320)
    elif select == 3:
        player = load_image('./res/Menu_cookie_05.png')
        playerx = 0
        playery = 344
        playerfidx = 346
        playersize = (344, 344)
    bg = load_image('./res/finish.png')
    score = 0
    font = gfw.font.load('res/CookieRun Regular.ttf', 35)

    bgm = load_music('./res/finish 2.mp3')
    bgm.get_volume()
    bgm.play()

def draw():
    bg.draw(canvas_width / 2, canvas_height / 2, 1120, 630)
    player.clip_draw(playerx, playery, *playersize, canvas_width / 2, canvas_height / 2 + 50)
    font.draw(canvas_width / 2 - 100, canvas_height - 200, 'Score : %0d' % score, SCORE_TEXT_COLOR)
    print(score, targetscore)
    delay(0.05)

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_RETURN:
            gfw.change(Scene_Menu, 0)
        elif e.key == SDLK_ESCAPE:
            gfw.quit()

def update():
    global playerx, playerfidx, fidxCnt
    global score
    playerx += playerfidx
    fidxCnt += 1
    if fidxCnt > 3:
        playerx = 0
        fidxCnt = 0
    if score < targetscore:
        if targetscore < 5000:
            score += 69
        elif targetscore < 10000:
            score += 169
        elif targetscore < 20000:
            score += 569
        elif targetscore < 30000:
            score += 769
        elif targetscore < 40000:
            score += 987
    if score > targetscore:
        score = targetscore

def set_score(pscore):
    global targetscore
    targetscore = pscore

def exit():
    global player, bgm
    del player
    del bgm

