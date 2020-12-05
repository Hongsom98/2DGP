from pico2d import *
import gfw
import gobj
import json

PLAYER_SIZE = 270

class Player:
    RUNNING, FALLING, JUMPING, DOUBLE_JUMP, SLIDING, HITTING, DIE = range(7)
    ANIMS_11x6 = [
        [ 0x40, 0x41, 0x42, 0x43 ], # RUNNING
        [ 0x50 ],                   # FALLING
        [ 0x57, 0x58 ],             # JUMPING
        [ 0x51, 0x52, 0x53, 0x54 ], # DOUBLE_JUMP
        [ 0x59, 0x5A ],             # SLIDING
        [ 0x10, 0x11, 0x12, 0x13, 0x14],# HITTING
        [ 0x15, 0x16, 0x17, 0x18],# DIE
    ]
    ANIMS_13x6 = [
        [ 0x40, 0x41, 0x42, 0x43 ], # RUNNING
        [ 0x50 ],                   # FALLING
        [ 0x56, 0x57 ],             # JUMPING
        [ 0x51, 0x52, 0x53, 0x54 ], # DOUBLE_JUMP
        [ 0x58, 0x59 ],             # SLIDING
        [ 0x10, 0x11, 0x12, 0x13, 0x14],# HITTING
        [ 0x15, 0x16, 0x17, 0x18],  # DIE
    ]
    MAGNIFIED_RUN_ANIM = [ 0x44, 0x45, 0x46, 0x47 ]
    BB_DIFFS = [
        (-60,-135,60,0),   # RUNNING
        (-60,-135,60,10),  # FALLING
        (-60,-135,60,-20), # JUMPING
        (-60,-135,60,-20), # DOUBLE_JUMP
        (-80,-135,80,-68), # SLIDING
        (-60,-135,60,0), # HITTING
        (-80,-135,80,-68), # DIE
    ]
    SLIDE_DURATION = 1.0

    GRAVITY = 3000
    JUMP = 1000

    #constructor
    def __init__(self, select):
        self.pos = 150, get_canvas_height() // 2
        self.delta = 0, 0
        # self.image = gfw.image.load(gobj.res('cookie.png'))
        self.time = 0
        self.FPS = 10
        self.mag = 1
        self.mag_speed = 0
        # self.anims = Player.ANIMS_11x6
        self.change_image(select + 1)
        self.select = select
        self.state = Player.RUNNING
        self.fall_over = False
        self.mag_time = None
        self.super = False
        self.magnet = False
        self.magnet_time = None
        self.game_over = False


    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self, state):
        self.__state = state
        self.anim = self.anims[state]
        if state == 5:
            self.hit_time = get_time()
    def get_fall(self):
        return self.fall_over
    def get_gameover(self):
        anim = self.anim
        # if self.state == Player.RUNNING and self.mag > 1:
        #     anim = Player.MAGNIFIED_RUN_ANIM
        fidx = round(self.time * self.FPS) % len(anim)
        sprite_num = anim[fidx]
        return sprite_num

    def draw(self):
        anim = self.anim
        # if self.state == Player.RUNNING and self.mag > 1:
        #     anim = Player.MAGNIFIED_RUN_ANIM
        fidx = round(self.time * self.FPS) % len(anim)
        sprite_num = anim[fidx]
        x, y = sprite_num % 0x10, sprite_num // 0x10
        x = x * (PLAYER_SIZE + 2) + 2
        y = y * (PLAYER_SIZE + 2) + 2
        size = PLAYER_SIZE * self.mag, PLAYER_SIZE * self.mag
        self.image.clip_draw(x, y, PLAYER_SIZE, PLAYER_SIZE, *self.pos, *size)

        #if self.state == 6:
        #    delay(0.1)

        if self.cookie_time < 3.0:
            font = gfw.font.load(gobj.res('ENCR10B.TTF'), 30)
            font.draw(20, 20, self.cookie_name)

    def magnify(self):
        self.mag_speed = 1.0
        self.mag_time = get_time()
        self.super = True

    def reduce(self):
        self.mag_speed = -1.0
        self.mag_time = None
        self.super = False

    def jump(self):
        if self.state in [Player.DOUBLE_JUMP]:
            return
        if self.state == Player.RUNNING:
            self.state = Player.JUMPING
        elif self.state == Player.FALLING:
            self.state = Player.JUMPING
        elif self.state == Player.JUMPING:
            self.state = Player.DOUBLE_JUMP
        elif self.state == Player.SLIDING:
            self.state = Player.JUMPING
        self.jump_speed = Player.JUMP * self.mag
    def slide(self):
        if self.state != Player.RUNNING: return
        self.state = Player.SLIDING
    def update(self):
        self.update_mag()
        self.cookie_time += gfw.delta_time
        self.time += gfw.delta_time
        if self.state in [Player.JUMPING, Player.DOUBLE_JUMP, Player.FALLING, Player.HITTING]:
            # print('jump speed:', self.jump_speed)
            if self.mag != 1:
                self.move((0, self.jump_speed // 2* gfw.delta_time))
            else:
                self.move((0, self.jump_speed * gfw.delta_time))
            self.jump_speed -= Player.GRAVITY * self.mag * gfw.delta_time
        _,foot,_,_ = self.get_bb()
        if foot < 0:
            self.fall_over = True
        platform = self.get_platform(foot)
        if platform is not None:
            l,b,r,t = platform.get_bb()
            if self.state in [Player.RUNNING, Player.SLIDING]:
                if foot > t:
                    self.state = Player.FALLING
                    self.jump_speed = 0
            else:
                # print('falling', t, foot)
                if self.jump_speed < 0 and int(foot) <= t:
                    self.move((0, t - foot))
                    self.state = Player.RUNNING
                    self.jump_speed = 0
        if self.state == Player.HITTING:
            self.set_image_alpha(127)
            if  get_time() - self.hit_time > 1.0:
                self.state = Player.FALLING
                self.set_image_alpha(255)
        if self.mag_time != None and get_time() - self.mag_time > 3.5:
            self.reduce()
        if self.magnet_time != None and get_time() - self.magnet_time > 5.0:
            self.magnet = False
            self.magnet_time = None


    def set_image_alpha(self, alpha):
        SDL_SetTextureAlphaMod(self.image.texture, int(alpha))

    def get_platform(self, foot):
        selected = None
        sel_top = 0
        x,y = self.pos
        for platform in gfw.world.objects_at(gfw.layer.platform):
            l,b,r,t = platform.get_bb()
            if x < l or x > r: continue
            mid = (b + t) // 2
            if foot < mid: continue
            if selected is None:
                selected = platform
                sel_top = t
            else:
                if t > sel_top:
                    selected = platform
                    sel_top = t
        # if selected is not None:
        #     print(l,b,r,t, selected)
        return selected

    def move_down_from_platform(self):
        if self.state != Player.RUNNING: return
        _,foot,_,_ = self.get_bb()
        platform = self.get_platform(foot)
        print('can pass:', platform.can_pass)
        if not platform.can_pass: return

        x,y = self.pos
        y -= platform.height / 2 + 1
        self.pos = x,y

    def update_mag(self):
        if self.mag_speed == 0: return

        x,y = self.pos
        _,b,_,_ = self.get_bb()
        diff = y - b
        prev_mag = self.mag

        self.mag += self.mag_speed * gfw.delta_time
        if self.mag > 2.0:
            self.mag = 2.0
            self.mag_speed = 0
        elif self.mag < 1.0:
            self.mag = 1.0
            self.mag_speed = 0

        new_y = b + diff * self.mag / prev_mag
        self.pos = x,new_y

    def move(self, diff):
        self.pos = gobj.point_add(self.pos, diff)

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_RETURN:
                self.slide()
            elif e.key == SDLK_SPACE or e.key == SDLK_UP:
                self.jump()
            elif e.key == SDLK_DOWN:
                self.move_down_from_platform()
            elif e.key == SDLK_m:
                if self.mag == 2 or self.mag_speed > 0:
                    self.reduce()
                else:
                    self.magnify()
            elif e.key == SDLK_LEFTBRACKET:
                self.change_image(-1)
            elif e.key == SDLK_RIGHTBRACKET:
                self.change_image(1)
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RETURN:
                self.state = Player.RUNNING

    def get_bb(self):
        l,b,r,t = Player.BB_DIFFS[self.state]
        b = - PLAYER_SIZE // 2
        x,y = self.pos
        if self.mag != 1:
            l *= self.mag
            b *= self.mag
            r *= self.mag
            t *= self.mag
        return x + l, y + b, x + r, y + t

    def get_super(self):
        return self.super

    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['image']
        return dict

    def __setstate__(self, dict):
        # self.__init__()
        self.__dict__.update(dict)
        self.image = gfw.image.load(gobj.RES_DIR + '/animation_sheet.png')

    def change_image(self, diff):
        if not hasattr(self, 'cookie_chars'):
            with open(gobj.res('cookies.json'), 'r') as f:
                self.cookie_chars = json.load(f)
            self.cookie_index = diff
        else:
            cookie = self.cookie_chars[self.cookie_index]
            sheet = './Cookie/%s_sheet.png' % cookie["id"]
            gfw.image.unload(sheet)
            self.cookie_index = (self.cookie_index + diff) % len(self.cookie_chars)

        cookie = self.cookie_chars[self.cookie_index]
        sheet = './Cookie/%s_sheet.png' % cookie["id"]
        self.image = gfw.image.load(sheet)
        global PLAYER_SIZE
        prev_size = PLAYER_SIZE
        PLAYER_SIZE = cookie["size"]
        self.anims = Player.ANIMS_11x6 if cookie["xcount"] == 11 else Player.ANIMS_13x6

        x,y = self.pos
        diff = (PLAYER_SIZE - prev_size) // 2
        self.pos = x, y+diff
        print(cookie)

        self.cookie_name = cookie["name"]
        self.cookie_time = 0

