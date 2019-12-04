from pico2d import*

class Background():
    def __init__(self):
        self.image = load_image('Dirt_Field.png')

    def update(self):
        pass

    def draw_hitbox(self):
        pass

    def draw(self):
        self.image.draw(1280//2,800//2,1280,800)