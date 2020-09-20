from helper import *
from pico2d import *

open_canvas()

class Character:
    def __init__(self):
        self.pos = (400,85)
        self.target = (400, 85)
        self.next_target = []
        self.speed = 1
        self.FrameIndex = 0
        self.Delta = (0, 0)
        self.image = load_image('../res/run_animation.png')
    def draw(self):
        self.image.clip_draw(self.FrameIndex * 100, 0, 100, 100, self.pos[0], self.pos[1])
    def update(self):
        self.Delta = delta(self.pos, self.target, self.speed)
        self.pos = move_toward(self.pos, self.Delta, self.target)[0]
        self.FrameIndex = (self.FrameIndex + 1) % 8
        if self.pos == self.target:
            self.speed = 1
            if len(self.next_target) > 0:
                self.target = self.next_target[0]
                del self.next_target[0]


class Grass:
    def __init__(self):
        self.image = load_image('../res/grass.png')
    def draw(self):
        self.image.draw(400, 30)
    def update(self):
        pass

def handle_events():
    global moving
    global boy
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            moving = False
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            moving = False
        elif e.type == SDL_MOUSEBUTTONDOWN:
            boy.speed += 1
            boy.next_target.append((e.x, 600 - 1 - e.y))


boy = Character()
grass = Grass()

moving = True

while moving:
    clear_canvas()

    grass.draw()
    boy.draw()

    update_canvas()

    boy.update()

    handle_events()

close_canvas()
