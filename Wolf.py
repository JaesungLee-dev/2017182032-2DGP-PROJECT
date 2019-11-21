from pico2d import*
import main_state
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Wolf():
    image = None
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed = RUN_SPEED_PPS
        self.frame = 0
        if Wolf.image == None:
            Wolf.image = load_image('monster.png')

    def update(self):
        self.find_nearest_sheep()
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        self.image.clip_draw(int(self.frame)*80,280,80,56,self.x,self.y)

    def move_wolf(self, i):
        sheep = main_state.get_sheep()

        vector_size = ((sheep[i].x - self.x) ** 2 + (sheep[i].y - self.y) ** 2) ** 0.5

        self.x += (sheep[i].x - self.x) / vector_size * self.speed * game_framework.frame_time
        self.y += (sheep[i].y - self.y) / vector_size * self.speed * game_framework.frame_time

    def find_nearest_sheep(self):
        sheep = main_state.get_sheep()
        nearest = float("inf")
        nearest_index = 0
        for i in range(3):
            if ((sheep[i].x - self.x) ** 2 + (sheep[i].y - self.y) ** 2) < nearest:
                nearest = ((sheep[i].x - self.x) ** 2 + (sheep[i].y - self.y) ** 2)
                nearest_index = i
        self.move_wolf(nearest_index)

