import game_framework
import main_state
from pico2d import*

pause = None

def enter():
    global pause
    pause = load_image('pause.png')

def exit():
    global pause
    del(pause)

def update():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()

def draw():
    clear_canvas()
    main_state.draw()
    pause.draw(400,300,200,200)
    update_canvas()