from pico2d import*

class House():
    def __init__(self):
        self.x, self.y = 750, 550
        self.image = load_image('House.png')

    def update(self):
        pass

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def draw_hitbox(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        draw_rectangle(*self.get_bb())
        self.image.draw(self.x,self.y,200,200)