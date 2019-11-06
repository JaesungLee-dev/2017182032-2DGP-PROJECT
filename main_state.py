from pico2d import *
import game_framework
import Cowboy
import Sheep
import Wolf
import game_over_state

name = "MainState"

cowboy = None
sheep = None
wolf = None
dirt_field = None

def enter():
    global cowboy, sheep, wolf,dirt_field
    cowboy = Cowboy.Cowboy(20,64)
    sheep = Sheep.Sheep(100,100)
    wolf = Wolf.Wolf(800,600)
    dirt_field = load_image('Dirt_Field.png')

def exit():
    global cowboy,sheep,wolf,dirt_field
    del(cowboy)
    del(wolf)
    del(sheep)
    del(dirt_field)

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                cowboy.dir += 1
            if event.key == SDLK_LEFT:
                cowboy.dir -= 1
            if event.key == SDLK_UP:
                cowboy.dir += 3
            if event.key == SDLK_DOWN:
                cowboy.dir -= 3
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                cowboy.dir -= 1
            if event.key == SDLK_LEFT:
                cowboy.dir += 1
            if event.key == SDLK_UP:
                cowboy.dir -= 3
            if event.key == SDLK_DOWN:
                cowboy.dir += 3


def update():
    find_sheep_dest()
    move_wolf()
    cowboy.update()
    sheep.update()
    wolf.update()
    collide_check()

def draw():
    clear_canvas()
    dirt_field.draw(400,300)
    cowboy.draw()
    sheep.draw()
    wolf.draw()
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
    if(((cowboy.x - sheep.x)**2+(cowboy.y-sheep.y)**2)**0.5 < 100):
        sheep.dest_x += sheep.x - cowboy.x
        sheep.dest_y += sheep.y - cowboy.y

    sheep.dest_x = clamp(0, sheep.dest_x , 800)
    sheep.dest_y = clamp(0,sheep.dest_y,600)