from pico2d import *
import game_framework
from Cowboy import Cowboy
from Sheep import Sheep
from Wolf import Wolf
from Background import Background
from House import House
import game_world
import game_over_state
import game_clear_state

name = "MainState"

voadsf = None

cowboy = None
sheeps = None
wolfs = None
background = None
house = None
game_clear = None
safe_sheeps = None

moving_sheep = True

def enter():
    global cowboy, sheeps, wolfs, background,house, game_clear, safe_sheeps
    game_clear = False
    safe_sheeps = 0

    house = House()
    cowboy = Cowboy(20,64)
    sheeps = [Sheep() for i in range(3)]
    wolfs = [Wolf() for i in range(8)]
    background = Background()

    game_world.add_object(background,0)
    game_world.add_object(house,0)
    game_world.add_object(cowboy, 1)
    game_world.add_objects(sheeps, 1)
    game_world.add_objects(wolfs, 1)

def exit():
    a = 10
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
    global game_clear, safe_sheeps, house
    for game_object in game_world.all_objects():
        game_object.update()

    for wolf in wolfs:
        if collide(wolf,cowboy):
            game_framework.change_state(game_over_state)
        for sheep in sheeps:
            if collide(wolf, sheep):
                sheeps.remove(sheep)
                game_world.remove_object(sheep)

    for sheep in sheeps:
        if collide(sheep, house):
            sheeps.remove(sheep)
            game_world.remove_object(sheep)
            game_clear = True
            safe_sheeps += 1

    for bullet in game_world.objects[2]:
        for animal in game_world.objects[1]:
            if isinstance(animal,Wolf):
                if collide(animal, bullet):
                    wolfs.remove(animal)
                    game_world.remove_object(bullet)
                    game_world.remove_object(animal)
            if isinstance(animal,Sheep):
                if collide(animal, bullet):
                    sheeps.remove(animal)
                    game_world.remove_object(bullet)
                    game_world.remove_object(animal)


    if len(sheeps) ==0:
        if game_clear == True:
            game_framework.change_state(game_clear_state)
        else:
            game_framework.change_state(game_over_state)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
        #game_object.draw_hitbox()
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