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
sheep = None
wolf = None
background = None

moving_sheep = True

def enter():
    global cowboy, sheep, wolf, background
    cowboy = Cowboy.Cowboy(20,64)
    sheep = [Sheep.Sheep(random.randint(0,200),200) for i in range(3)]
    wolf = Wolf.Wolf(800,600)
    background = Background()

    game_world.add_object(background,0)
    game_world.add_object(cowboy, 1)
    game_world.add_objects(sheep, 1)
    game_world.add_object(wolf, 1)

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
    #collide_check()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def get_cowboy():
    global cowboy
    return cowboy

def get_sheep():
    global sheep
    return sheep

def collide_check():
    global sheep, wolf
    if(((sheep.x - wolf.x)**2+(sheep.y-wolf.y)**2)**0.5 < 45):
        game_framework.change_state(game_over_state)