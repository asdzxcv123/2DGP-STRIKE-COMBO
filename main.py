from code.player import Player
from pico2d import *

def reset_world():
    global player
    player = Player()

def update_world():
    player.update()
    pass

def render_world():
    clear_canvas()
    player.draw()
    update_canvas()

running = True

open_canvas()
reset_world()

while running:

    update_world()
    render_world()