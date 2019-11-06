from pico2d import*
import Base_object

class Sheep(Base_object.Base_object):
    image = None

    def __init__(self,x,y):
        super(Sheep,self).__init__(x,y)
        self.frame = 0
        self.dest_x = x
        self.dest_y = y
        if Sheep.image == None:
            Sheep.image = load_image('llama_walk_0.png')

    def update(self):
        self.x = self.x * 0.95 + self.dest_x * 0.05
        self.y = self.y * 0.95 + self.dest_y * 0.05

        self.frame = (self.frame + 1) % 4

    def draw(self):
        self.image.clip_draw(self.frame*128,0,128,128,self.x,self.y)