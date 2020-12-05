from pico2d import *
import gfw
import Scene_Menu
import gobj

canvas_width = 1120
canvas_height = 630

def enter(select):
    global image, loading, loading_x, previous_time, speed
    global bgm
    hide_cursor()
    image = load_image('./res/title.png')
    loading = load_image('./res/title_loading.png')

    loading_x = -512.0
    speed = 3.5

    bgm = load_music('./res/loading sound - cutting2.mp3')
    bgm.get_volume()
    bgm.repeat_play()

    previous_time = get_time()
    pass

def exit():
    global  image, loading
    global bgm
    del image
    del loading
    del bgm
    pass

def update():
    global start_time, loading_x, previous_time, speed
    current = get_time()
    loading_x += speed * (current - previous_time)
    if current - previous_time >= 2.7:
        gfw.change(Scene_Menu , None)
    pass

def draw():
    global image, loading
    image.clip_draw(0, 0, 1400, 800, 500, 250)
    loading.clip_draw(0, 0, 1027, 16, loading_x, 8)
    pass

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
        return
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.quit()
            return
    pass

def pause():
    pass

def resume():
    pass

if __name__ == '__main__':
    gfw.run_main()
