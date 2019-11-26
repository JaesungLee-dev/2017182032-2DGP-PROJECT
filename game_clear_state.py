import game_framework
from pico2d import *
import start_state

import main_state

name = "game_clear_state"
image = None
background_image = None

def enter():
    global image, background_image
    image = load_image('Result Screen.png')
    background_image = load_image('Dirt_Field.png')

def exit():
    global image, background_image
    del(image)
    del(background_image)

def update():
    pass

def draw():
    global image, background_image
    clear_canvas()

    background_image.draw(400,300)

    if main_state.safe_sheeps == 1:
        image.clip_draw(250,400,190,210,300,300,100,100)
        image.clip_draw(420, 100, 160, 160, 400, 350, 100, 100)
        image.clip_draw(420, 100, 160, 160, 500, 300, 100, 100)
    elif main_state.safe_sheeps == 2:
        image.clip_draw(250,400,190,210,300,300,100,100)
        image.clip_draw(250,400,190,210,400,350,100,100)
        image.clip_draw(420, 100, 160, 160, 500, 300, 100, 100)
    else:
        image.clip_draw(250,400,190,210,300,300,100,100)
        image.clip_draw(250, 400, 190, 210, 400, 350, 100, 100)
        image.clip_draw(250, 400, 190, 210, 500, 300, 100, 100)

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(start_state)

def pause(): pass

def resume(): pass