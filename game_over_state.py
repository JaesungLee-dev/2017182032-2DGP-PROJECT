import game_framework
from pico2d import *
import start_state


name = "gameover"
image = None
background_image = None
logo_time = 0.0


def enter():
    global image, background_image
    image = load_image('./Resource/gameover.png')
    background_image = load_image('./Resource/Dirt_Field.png')


def exit():
    global image, background_image
    del(image)
    del(background_image)


def update():
    pass




def draw():
    global image
    clear_canvas()
    background_image.draw(640,400,1280,800)
    image.draw(640,400,400,300)
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
