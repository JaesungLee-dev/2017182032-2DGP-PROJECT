from pico2d import*
import Base_object

class Sheep(Base_object.Base_object):
    def __init__(self,x,y):
        super(Sheep,self).__init__(x,y)
        self.frame = 0
        self.image = load_image('llama_walk_0.png')
        self.goto_x = 400
        self.goto_y = 400

    def update(self):
        self.x = self.x * 0.95 + self.goto_x * 0.05
        self.y = self.y * 0.95 + self.goto_y * 0.05

        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame*128,0,128,128,self.x,self.y)