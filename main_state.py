from pico2d import *
import game_framework
import Cowboy
import Sheep
import Wolf
from Background import Background
import game_world
import game_over_state

name = "MainState"

cowboy = None
sheep = None
wolf = None
background = None

def enter():
    global cowboy, sheep, wolf, background
    cowboy = Cowboy.Cowboy(20,64)
    sheep = Sheep.Sheep(100,100)
    wolf = Wolf.Wolf(800,600)
    background = Background()

    game_world.add_object(background,0)
    game_world.add_object(cowboy, 1)
    game_world.add_object(sheep, 1)
    game_world.add_object(wolf, 1)

def exit():
    game_world.clear()

def pause():
    pass

def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            cowboy.handle_event(event)


def update():
    move_wolf()
    find_sheep_dest()

    for game_object in game_world.all_objects():
        game_object.update()
    #collide_check()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide_check():
    global sheep, wolf
    if(((sheep.x - wolf.x)**2+(sheep.y-wolf.y)**2)**0.5 < 45):
        game_framework.change_state(game_over_state)

def move_wolf():
    global sheep, wolf

    vector_size = ((sheep.x - wolf.x)**2+(sheep.y - wolf.y)**2)**0.5

    wolf.x += (sheep.x - wolf.x)/vector_size * wolf.speed
    wolf.y += (sheep.y - wolf.y)/vector_size * wolf.speed

def find_sheep_dest():
    global cowboy,sheep
    if((cowboy.x - sheep.x)**2+(cowboy.y-sheep.y)**2< 10000):
        sheep.dest_x += sheep.x - cowboy.x
        sheep.dest_y += sheep.y - cowboy.y

    sheep.dest_x = clamp(0, sheep.dest_x , 800)
    sheep.dest_y = clamp(0,sheep.dest_y,600)