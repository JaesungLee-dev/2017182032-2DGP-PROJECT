from pico2d import*
import Base_object

class Wolf(Base_object.Base_object):
    def __init__(self,x,y):
        super(Wolf,self).__init__(x,y)
        self.dest_x, self.dest_y = x, y
        self.image = load_image('monster.png')
        self.frame = 0
    def update(self):
        self.x = self.x * 0.99 + self.dest_x * 0.01
        self.y = self.y * 0.99 + self.dest_y * 0.01

        self.frame = (self.frame + 1) % 6
    def draw(self):
        self.image.clip_draw(self.frame*80,280,80,56,self.x,self.y)
