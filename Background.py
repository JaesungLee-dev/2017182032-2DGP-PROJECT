from pico2d import*

class Background():
    def __init__(self):
        self.image = load_image('./Resource/Dirt_Field.png')
        self.bgm = load_music('./Resource/Western.mp3')
        self.bgm.set_volume(200)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw_hitbox(self):
        pass

    def draw(self):
        self.image.draw(1280//2,800//2,1280,800)