from pico2d import*
import Base_object

class Wolf(Base_object):
    def __init__(self,x,y):
        super(Wolf,self).__init__(x,y)
        self.dest_x, self.dest_y = x,y
        self.image = load_image('moster.png')

