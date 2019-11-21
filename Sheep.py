from pico2d import*
import main_state
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Sheep():
    image = None
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.frame = 0
        self.speed = RUN_SPEED_PPS
        self.dest_x, self.dest_y = x, y
        if Sheep.image == None:
            Sheep.image = load_image('llama_walk_0.png')

    def update(self):
        self.find_sheep_dest()

    def draw(self):
        self.image.clip_draw(int(self.frame) * 128,0,128,128,self.x,self.y)

    def find_sheep_dest(self):
        cowboy = main_state.get_cowboy()

        if ((cowboy.x - self.x) ** 2 + (cowboy.y - self.y) ** 2 < 10000):
            self.dest_x += self.x - cowboy.x
            self.dest_y += self.y - cowboy.y
            self.move_sheep()
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        else:
            self.frame = 2

        self.dest_x = clamp(0, self.dest_x, 800)
        self.dest_y = clamp(0, self.dest_y, 600)

    def move_sheep(self):
        vector_size = ((self.x - self.dest_x) ** 2 + (self.y - self.dest_y) ** 2) ** 0.5

        if(vector_size >= 80):
            self.x += (self.dest_x - self.x) / vector_size * self.speed * game_framework.frame_time
            self.y += (self.dest_y - self.y) / vector_size * self.speed * game_framework.frame_time

        self.x = clamp(0, self.x, 800)
        self.y = clamp(0, self.y, 600)
