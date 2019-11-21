from pico2d import*
import Base_object

class Wolf():
    image = None
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.speed = 3
        self.frame = 0
        if Wolf.image == None:
            Wolf.image = load_image('monster.png')

    def update(self):
        self.frame = (self.frame + 1) % 6

    def draw(self):
        self.image.clip_draw(self.frame*80,280,80,56,self.x,self.y)
