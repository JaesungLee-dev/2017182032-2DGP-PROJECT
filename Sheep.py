from pico2d import*
import main_state
import game_framework
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Sheep():
    image = None
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.frame = 0
        self.speed = 0
        self.dir = random.random() * 2 * math.pi
        self.target_x, self.target_y = x, y

        self.build_behavior_tree()

        if Sheep.image == None:
            Sheep.image = load_image('llama_walk_0.png')

    def update(self):
        self.bt.run()

    def draw(self):
        draw_rectangle(*self.get_bb())
        if math.cos(self.dir) > 0:
            self.image.clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128,3.141592 * 2,'h',self.x,self.y,128, 128)


    def get_bb(self):
        return self.x - 25, self.y - 30, self.x + 25, self.y + 35

    def find_sheep_dest(self):
        cowboy = main_state.get_cowboy()

        if ((cowboy.x - self.x) ** 2 + (cowboy.y - self.y) ** 2 < 10000):
            self.target_x += self.x - cowboy.x
            self.target_y += self.y - cowboy.y

            self.target_x = clamp(30, self.target_x, 800)
            self.target_y = clamp(30, self.target_y, 600)

            self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)
            return BehaviorTree.SUCCESS

        self.speed = 0
        return BehaviorTree.FAIL

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(30, self.x, 800)
        self.y = clamp(30, self.y, 600)

    def move_sheep(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        find_sheep_dest = LeafNode("find_sheep_dest",self.find_sheep_dest)
        move_sheep = LeafNode("move_sheep",self.move_sheep)

        move_to_destination = SequenceNode("move_to_destination")
        move_to_destination.add_children(find_sheep_dest,move_sheep)

        self.bt = BehaviorTree(move_to_destination)