from math import gamma

from code import game_world
from code.player import Player
from pico2d import *


player=None

def handle_events():
    global running
    global player
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def reset_world():
    global player
    player = Player()
    game_world.add_object(player, 0)

def update_world():
    game_world.update()
    pass

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

running = True

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)