from pico2d import *
import game_framework
import Cowboy
import Sheep

name = "MainState"

cowboy = None
sheep = None
dirt_field = None

def enter():
    global cowboy, sheep, dirt_field
    cowboy = Cowboy.Cowboy(20,64)
    sheep = Sheep.Sheep(300,300)
    dirt_field = load_image('Dirt_Field.png')

def exit():
    global cowboy,sheep,dirt_field
    del(cowboy)
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
    find_sheep_goto()
    cowboy.update()
    sheep.update()


def draw():
    clear_canvas()
    dirt_field.draw(400,300)
    cowboy.draw()
    sheep.draw()
    update_canvas()

def find_sheep_goto():
    global cowboy,sheep
    if(((cowboy.x - sheep.x)**2+(cowboy.y-sheep.y)**2)**0.5 < 100):
        sheep.goto_x += sheep.x - cowboy.x
        sheep.goto_y += sheep.y - cowboy.y
    if(sheep.goto_x>800):
        sheep.goto_x = 800
    if (sheep.goto_x < 0):
        sheep.goto_x = 0
    if(sheep.goto_y>600):
        sheep.goto_y = 600
    if (sheep.goto_y < 0):
        sheep.goto_y = 0




