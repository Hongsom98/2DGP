from pico2d import *
import gfw

canvas_width = 1120
canvas_height = 630

def enter():
    pass

def exit():
    pass

def update():
    pass

def draw():
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

if __name__ == '__main__':
    gfw.run_main()