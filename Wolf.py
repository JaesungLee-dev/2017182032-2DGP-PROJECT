from pico2d import*
import main_state
import game_framework
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Wolf():
    image = None
    def __init__(self):
        self.x, self.y = random.randint(1300,1500), random.randint(0,650)
        self.speed = RUN_SPEED_PPS
        self.timer = 0
        self.frame = 0
        if Wolf.image == None:
            Wolf.image = load_image('./Resource/monster.png')
        self.target_x, self.target_y = None, None
        self.dir = random.random() * 2 * math.pi

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 32, self.y + 19

    def update(self):
        self.bt.run()

    def draw_hitbox(self):
        draw_rectangle(*self.get_bb())

    def draw(self):
        if math.cos(self.dir) < 0:
            self.image.clip_draw(int(self.frame) * 80, 280, 80, 56, self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame)*80,280,80,56,3.141592 * 2,'h',self.x,self.y,80,56)

    def move_wolf(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()

        return BehaviorTree.SUCCESS

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        #self.x = clamp(50, self.x, 1280 - 50)
        #self.y = clamp(50, self.y, 800 - 50)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random() * 2 * math.pi
        return BehaviorTree.SUCCESS

    def find_nearest_sheep(self):
        sheeps = main_state.get_sheeps()

        nearest = float("inf")
        nearest_sheep = None
        for sheep in sheeps:
            if ((sheep.x - self.x) ** 2 + (sheep.y - self.y) ** 2) < nearest:
                nearest = ((sheep.x - self.x) ** 2 + (sheep.y - self.y) ** 2)
                nearest_sheep = sheep

        #if (nearest_sheep.x - self.x) ** 2 + (nearest_sheep.y - self.y) ** 2 > 90000:
            #return BehaviorTree.FAIL

        self.target_x, self.target_y = nearest_sheep.x, nearest_sheep.y
        self.dir = math.atan2(self.target_y - self.y, self.target_x - self.x)

        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        find_nearest_sheep = LeafNode("find_nearest_sheep",self.find_nearest_sheep)
        move_wolf = LeafNode("move_wolf",self.move_wolf)

        chase_sheep = SequenceNode("chase_sheep")
        chase_sheep.add_children(find_nearest_sheep,move_wolf)

        #wander = LeafNode("wander",self.wander)

        #wanderNchase = SelectorNode("wander and chase")
        #wanderNchase.add_children(chase_sheep,wander)
        #wanderNchase.add_child(wander)

        self.bt = BehaviorTree(chase_sheep)