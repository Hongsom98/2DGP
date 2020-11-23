from pico2d import *
import gfw
import gobj
from gobj import *


class Hpui:
    def __init__(self, reductionratio):
        self.image = gfw.image.load(gobj.res('HpUi.png'))
        self.width = 500
        self.drawLoc = 500
        self.reduction = reductionratio
        self.count = 0
    def update(self):
        self.count += self.reduction
        if self.count >= 1:
            self.count = 0
            self.width -= 1
            self.drawLoc -= 0.5
        pass
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, width):
        self.__width = width

    def hp(self):
        self.width += 20

    def draw(self):
        self.image.clip_draw(0, 0, self.width, 90, self.drawLoc, 590)

    def handle_event(self, e):
        pass

    def player_colide(self):
        self.width -= 20
        self.drawLoc -= 10

    def exit(self):
        global image
        del image


