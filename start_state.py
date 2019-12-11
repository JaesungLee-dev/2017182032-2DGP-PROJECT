import game_framework
from pico2d import *
import game_clear_state

import main_state

name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('./Resource/kpu_credit.png')


def exit():
    global image
    del(image)


def update():
    global logo_time

    if logo_time > 1.0:
        logo_time = 0
        game_framework.change_state(main_state)
    delay(0.01)
    logo_time += 0.01



def draw():
    global image
    clear_canvas()
    image.draw(640,400,1280,800)
    update_canvas()


def handle_events():
    pass


def pause(): pass


def resume(): pass




