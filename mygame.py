import game_framework
from pico2d import*
import start_state
import os

pico2d.open_canvas(1280,800)
game_framework.run(start_state)
pico2d.clear_canvas()