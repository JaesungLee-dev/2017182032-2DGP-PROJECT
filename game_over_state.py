import game_framework
from pico2d import *


name = "gameover"
image = None
background_image = None
logo_time = 0.0


def enter():
    global image, background_image
    image = load_image('gameover.png')
    background_image = load_image('Dirt_Field.png')


def exit():
    global image, background_image
    del(image)
    del(background_image)


def update():
    pass




def draw():
    global image
    clear_canvas()
    background_image.draw(400,300)
    image.draw(400,300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.quit()


def pause(): pass


def resume(): pass
