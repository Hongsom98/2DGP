import random
from pico2d import *
import gfw
import gobj

JELLY_BORDER = 2
JELLY_SIZE = 66
BB_RADIUS = JELLY_SIZE / 4



def get_jelly_rect(index):
    ix, iy = index % 30, index // 30
    x = ix * (JELLY_BORDER + JELLY_SIZE) + JELLY_BORDER
    y = iy * (JELLY_BORDER + JELLY_SIZE) + JELLY_BORDER
    return x, y, JELLY_SIZE, JELLY_SIZE


class Jelly:
    TYPE_1, TYPE_2, TYPE_3, TYPE_F, TYPE_B, TYPE_HP, TYPE_C, TYPE_BJ, TYPE_RC = range(9)
    def __init__(self, type, x, y):
        self.x, self.y = x, y
        self.set_image(type)
        index = random.randint(3, 60)
        self.rect = get_jelly_rect(index)
        self.type = type
    def set_image(self, type):
        if type < 4:
            self.image = gfw.image.load(gobj.res('jelly.png'))
        elif type == 4:
            self.image = gfw.image.load(gobj.res('runfast.png'))
        elif type == 5:
            self.image = gfw.image.load(gobj.res('runbig.png'))
        elif type == 6:
            self.image = gfw.image.load(gobj.res('smallhp.png'))
        elif type == 7:
            self.image = gfw.image.load(gobj.res('jellytocoin.png'))
        elif type == 8:
            self.image = gfw.image.load(gobj.res('coin.png'))
    def update(self): pass
    def draw(self):
        if self.type < 4:
            self.image.clip_draw(*self.rect, self.x, self.y, JELLY_SIZE / 2, JELLY_SIZE / 2)
        else:
            self.image.clip_draw(0, 0, 66, 66, self.x, self.y, 50, 50)
    def move(self, dx):
        self.x += dx
        if self.x + JELLY_SIZE < 0:
            gfw.world.remove(self)
    def get_bb(self):
        return (
            self.x - BB_RADIUS, self.y - BB_RADIUS, 
            self.x + BB_RADIUS, self.y + BB_RADIUS
        )
    def get_type(self):
        return self.type
