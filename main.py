from pico2d import *

import play_mode as start_mode

from code import game_framework

from play_mode import *

open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
game_framework.run(start_mode)
close_canvas()

