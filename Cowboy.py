from pico2d import*
import Base_object

class Cowboy(Base_object.Base_object):
    def __init__(self,x,y):
        super (Cowboy,self).__init__(x,y)
        self.frame = 0
        self.anisheet_dir = 9
        self.dir = 0
        self.speed = 5
        self.image = load_image('cowboy.png')

    def move(self,a,b):
        self.x += a
        self.y += b

    def find_anisheet_dir(self):
        if self.dir == 1:
            self.anisheet_dir = 9
        if self.dir == -1:
            self.anisheet_dir = 8
        if self.dir == 3:
            self.anisheet_dir = 4
        if self.dir == -3:
            self.anisheet_dir = 0
        if self.dir == 2:
            self.anisheet_dir = 3
        if self.dir == 4:
            self.anisheet_dir = 5
        if self.dir == -4:
            self.anisheet_dir = 1
        if self.dir == -2:
            self.anisheet_dir = 7

    def move_by_dir(self):
        if self.dir == 1:
            self.move(self.speed, 0)
        if self.dir == -1:
            self.move(-1 * self.speed, 0)
        if self.dir == 3:
            self.move(0, 1 * self.speed)
        if self.dir == -3:
            self.move(0, -1 * self.speed)
        if self.dir == 2:
            self.move(-1 * self.speed / 2**0.5, self.speed / 2**0.5)
        if self.dir == 4:
            self.move(self.speed / 2**0.5, self.speed / 2**0.5)
        if self.dir == -4:
            self.move(-1 * self.speed / 2**0.5, -1 * self.speed / 2**0.5)
        if self.dir == -2:
            self.move(self.speed / 2**0.5, -1 * self.speed / 2**0.5)

    def update(self):
        self.find_anisheet_dir()
        self.move_by_dir()
        if (self.dir == 0):
            self.frame = 0
        else:
            self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame*128,self.anisheet_dir*128, 128, 128, self.x, self.y)
        delay(0.03)
