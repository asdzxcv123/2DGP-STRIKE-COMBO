
from code import game_world, game_framework
from code.player import Player
from pico2d import *
from code.camera import Camera

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
WORLD_WIDTH = 800  # 맵의 실제 총 너비
WORLD_HEIGHT = 600 # 맵의 실제 총 높이

player=None
camera=None
def handle_events():
    global player

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global player, camera

    camera=Camera(CANVAS_WIDTH,CANVAS_HEIGHT)
    camera.world_size(WORLD_WIDTH, WORLD_HEIGHT)

    player = Player()
    game_world.add_object(player, 0)

def update():
    game_world.update()

    camera.update(player)

    pass

def draw():
    clear_canvas()
    game_world.render(camera)
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
