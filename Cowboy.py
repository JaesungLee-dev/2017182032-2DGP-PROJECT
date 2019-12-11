from pico2d import*
import game_framework
import game_world
from Bullet import Bullet
import main_state

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

dir_to_action_table = {
    1: 9, -1: 8, 3: 4, -3: 0, 2: 3, 4: 5, -4: 1, -2: 7
}

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, NO_DIR, SPACE = range(10)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN,SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN,SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,

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
    DOWN_UP: 3,

    SPACE: 0
}

class IdleState:
    @staticmethod
    def enter(cowboy, event):
        pass
    @staticmethod
    def exit(cowboy, event):
        if event == SPACE:
            cowboy.frame = 11
            cowboy.fire_bullet()

    @staticmethod
    def do(cowboy):
        cowboy.frame = 11
        pass

    @staticmethod
    def draw(cowboy):
        cowboy.image.clip_draw(int(cowboy.frame) * 128, cowboy.action * 128, 128, 128, cowboy.x, cowboy.y)

class RunState:
    @staticmethod
    def enter(cowboy, event):
        pass
    @staticmethod
    def exit(cowboy, event):
        if event == SPACE:
            cowboy.fire_bullet()

    @staticmethod
    def do(cowboy):
        if (cowboy.dir == 0):
            cowboy.add_event(NO_DIR)
        cowboy.frame = (cowboy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        RunState.move_by_dir(cowboy)
    @staticmethod
    def draw(cowboy):
        cowboy.image.clip_draw(int(cowboy.frame) * 128, cowboy.action * 128, 128, 128, cowboy.x, cowboy.y)

    def move(cowboy,a,b):
        cowboy.x += a
        cowboy.y += b

    def move_by_dir(cowboy):
        if cowboy.dir == 1:
            RunState.move(cowboy,RUN_SPEED_PPS * game_framework.frame_time , 0)
        if cowboy.dir == -1:
            RunState.move(cowboy,-1 * RUN_SPEED_PPS* game_framework.frame_time, 0)
        if cowboy.dir == 3:
            RunState.move(cowboy,0, 1 * RUN_SPEED_PPS* game_framework.frame_time)
        if cowboy.dir == -3:
            RunState.move(cowboy,0, -1 * RUN_SPEED_PPS* game_framework.frame_time)
        if cowboy.dir == 2:
            RunState.move(cowboy,-1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if cowboy.dir == 4:
            RunState.move(cowboy,RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if cowboy.dir == -4:
            RunState.move(cowboy,-1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, -1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if cowboy.dir == -2:
            RunState.move(cowboy,RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, -1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)

next_state_table = {
    IdleState:
        {
            RIGHT_UP: RunState, LEFT_UP: RunState,
            RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
            UP_DOWN: RunState, DOWN_DOWN: RunState,
            UP_UP: RunState, DOWN_UP: RunState,
            NO_DIR: IdleState, SPACE: IdleState
        },
    RunState:
        {
            RIGHT_UP: RunState, LEFT_UP: RunState,
            LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
            UP_UP: RunState, DOWN_UP: RunState,
            UP_DOWN: RunState, DOWN_DOWN: RunState,
            NO_DIR: IdleState, SPACE: RunState
        }
}

class Cowboy():
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.frame = 0
        self.action = 9
        self.dir = 0
        self.now_dir = 1
        self.speed = 5
        self.image = load_image('./Resource/cowboy.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.sound = load_wav('./Resource/gun.wav')
        self.sound.set_volume(80)


    def get_bb(self):
        return self.x - 32, self.y - 64, self.x + 32, self.y + 36

    def draw_hitbox(self):
        draw_rectangle(*self.get_bb())

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

            if key_event == SPACE:
                self.sound.play()
                self.add_event(key_event)
                return

            prev_dir = self.dir
            self.dir += dir_by_event_table[key_event]
            if self.dir != 0:
                self.now_dir = self.dir
                self.action = dir_to_action_table[self.dir]
            else:
                self.now_dir = prev_dir
                self.action = dir_to_action_table[prev_dir]
            self.add_event(key_event)

    def fire_bullet(self):
        bullet = Bullet(self.x, self.y, self.now_dir)
        game_world.add_object(bullet, 2)
