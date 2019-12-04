import game_framework
from pico2d import*
import start_state
import os

os.chdir('D:\\공부\\2학년 2학기\\2D 게임프로그래밍\\2017182032-2DGP-PROJECT\\Resource')

pico2d.open_canvas(1280,800)
game_framework.run(start_state)
pico2d.clear_canvas()