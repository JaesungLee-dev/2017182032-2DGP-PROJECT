from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 50.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Bullet:
    image = None
    def __init__(self, x = 800, y = 300, direction = 1):
        if Bullet.image == None:
            Bullet.image = load_image('./Resource/bullet.png')
        self.x, self.y, self.dir = x, y, direction

    def draw(self):
        self.image.draw(self.x, self.y,60,60)

    def draw_hitbox(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        self.move_by_dir()
        if self.x < 0 or self.x > 1280 or self.y > 800 or self.y < 0:
            game_world.remove_object(self)

    def move(self,a,b):
        self.x += a
        self.y += b

    def get_bb(self):
        return self.x - 5, self.y - 5, self.x + 5, self.y + 5

    def move_by_dir(self):
        if self.dir == 1:
            self.move(RUN_SPEED_PPS * game_framework.frame_time , 0)
        if self.dir == -1:
            self.move(-1 * RUN_SPEED_PPS* game_framework.frame_time, 0)
        if self.dir == 3:
            self.move(0, 1 * RUN_SPEED_PPS* game_framework.frame_time)
        if self.dir == -3:
            self.move(0, -1 * RUN_SPEED_PPS* game_framework.frame_time)
        if self.dir == 2:
            self.move(-1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if self.dir == 4:
            self.move(RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if self.dir == -4:
            self.move(-1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, -1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
        if self.dir == -2:
            self.move(RUN_SPEED_PPS / 2**0.5* game_framework.frame_time, -1 * RUN_SPEED_PPS / 2**0.5* game_framework.frame_time)
