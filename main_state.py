from pico2d import *
import game_framework
import Cowboy
import Sheep
import Wolf
from Background import Background
import game_world
import game_over_state
import random

name = "MainState"

cowboy = None
sheeps = None
wolfs = None
background = None

moving_sheep = True

def enter():
    global cowboy, sheeps, wolfs, background
    cowboy = Cowboy.Cowboy(20,64)
    sheeps = [Sheep.Sheep(random.randint(0, 200), 200) for i in range(3)]
    wolfs = [Wolf.Wolf(random.randint(600, 800), 600) for i in range(2)]
    background = Background()

    game_world.add_object(background,0)
    game_world.add_object(cowboy, 1)
    game_world.add_objects(sheeps, 1)
    game_world.add_objects(wolfs, 1)

def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass


def handle_events():
    global moving_sheep

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            if moving_sheep:
                moving_sheep = False
            else:
                moving_sheep = True
        else:
            cowboy.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for wolf in wolfs:
        for sheep in sheeps:
            if collide(wolf, sheep):
                sheeps.remove(sheep)
                game_world.remove_object(sheep)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def get_cowboy():
    return cowboy

def get_sheeps():
    return sheeps

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True