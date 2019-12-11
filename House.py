from pico2d import*

class House():
    def __init__(self):
        self.x, self.y = 1180, 700
        self.image = load_image('./Resource/House.png')

    def update(self):
        pass

    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def draw_hitbox(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.draw(self.x,self.y,200,200)