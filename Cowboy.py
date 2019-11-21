from pico2d import*
import Base_object

dir_to_action_table = {
    1: 9, -1: 8, 3: 4, -3: 0, 2: 3, 4: 5, -4: 1, -2: 7
}

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, NO_DIR= range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN,SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN,SDLK_DOWN): DOWN_DOWN,

    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP,SDLK_UP): UP_UP,
    (SDL_KEYUP,SDLK_DOWN): DOWN_UP
}

dir_by_event_table = {
    RIGHT_DOWN: 1,
    LEFT_DOWN: -1,
    UP_DOWN: 3,
    DOWN_DOWN: -3,

    RIGHT_UP: -1,
    LEFT_UP: +1,
    UP_UP: -3,
    DOWN_UP: 3
}

class IdleState:
    @staticmethod
    def enter(cowboy, event):
        pass
    @staticmethod
    def exit(cowboy, event):
        pass
    @staticmethod
    def do(cowboy):
        cowboy.frame = 0
    @staticmethod
    def draw(cowboy):
        cowboy.image.clip_draw(cowboy.frame * 128, cowboy.action * 128, 128, 128, cowboy.x, cowboy.y)
        delay(0.03)

class RunState:
    @staticmethod
    def enter(cowboy, event):
        pass
    @staticmethod
    def exit(cowboy, event):
        pass

    @staticmethod
    def do(cowboy):
        if (cowboy.dir == 0):
            cowboy.add_event(NO_DIR)
            #cowboy.curr_state = IdleState
        cowboy.frame = (cowboy.frame + 1) % 8
        #cowboy.x = clamp(25, cowboy.x, 800 - 25)
        RunState.move_by_dir(cowboy)
    @staticmethod
    def draw(cowboy):
        cowboy.image.clip_draw(cowboy.frame * 128, cowboy.action * 128, 128, 128, cowboy.x, cowboy.y)
        delay(0.03)

    def move(cowboy,a,b):
        cowboy.x += a
        cowboy.y += b

    def move_by_dir(cowboy):
        if cowboy.dir == 1:
            RunState.move(cowboy,cowboy.speed, 0)
        if cowboy.dir == -1:
            RunState.move(cowboy,-1 * cowboy.speed, 0)
        if cowboy.dir == 3:
            RunState.move(cowboy,0, 1 * cowboy.speed)
        if cowboy.dir == -3:
            RunState.move(cowboy,0, -1 * cowboy.speed)
        if cowboy.dir == 2:
            RunState.move(cowboy,-1 * cowboy.speed / 2**0.5, cowboy.speed / 2**0.5)
        if cowboy.dir == 4:
            RunState.move(cowboy,cowboy.speed / 2**0.5, cowboy.speed / 2**0.5)
        if cowboy.dir == -4:
            RunState.move(cowboy,-1 * cowboy.speed / 2**0.5, -1 * cowboy.speed / 2**0.5)
        if cowboy.dir == -2:
            RunState.move(cowboy,cowboy.speed / 2**0.5, -1 * cowboy.speed / 2**0.5)

next_state_table = {
    IdleState:
        {
            RIGHT_UP: RunState, LEFT_UP: RunState,
            RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
            UP_DOWN: RunState, DOWN_DOWN: RunState,
            UP_UP: RunState, DOWN_UP: RunState,
            NO_DIR: IdleState
        },
    RunState:
        {
            RIGHT_UP: RunState, LEFT_UP: RunState,
            LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
            UP_UP: RunState, DOWN_UP: RunState,
            UP_DOWN: RunState, DOWN_DOWN: RunState,
            NO_DIR: IdleState
        }
}


class Cowboy():
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.frame = 0
        self.action = 9
        self.dir = 0
        self.speed = 5
        self.image = load_image('cowboy.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self,event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]

            prev_dir = self.dir
            self.dir += dir_by_event_table[key_event]
            if self.dir != 0:
                self.action = dir_to_action_table[self.dir]
            else:
                self.action = dir_to_action_table[prev_dir]

            self.add_event(key_event)