import pico2d as Pico

Pico.open_canvas()

Grass = Pico.load_image('../res/grass.png')
Character = Pico.load_image('../res/run_animation.png')

x = 0
FrameIndex = 0

while x < 800 :
    Pico.clear_canvas()
    Grass.draw(400,30)
    Character.clip_draw(100 * FrameIndex, 0, 100, 100, x, 85)
    Pico.update_canvas()

    Pico.get_events()

    x += 4

    #FrameIndex += 1
    #if FrameIndex >= 8 :
    #    FrameIndex = 0

    FrameIndex = (FrameIndex + 1) % 8

    Pico.delay(0.05)


Pico.close_canvas()