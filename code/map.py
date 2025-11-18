from pico2d import *
from code import game_world
from code.portal import Portal


class StageMap:
    def __init__(self, file_name, x, y, w, h, scale=3.0):
        self.image = load_image(file_name)
        self.src_x, self.src_y = x, y
        self.src_w, self.src_h = w, h
        self.scale = scale

        # 실제 게임 내 크기
        self.world_w = int(w * scale)
        self.world_h = int(h * scale)

        # 포탈 관리 리스트
        self.portals = []

        # 이동 제한 구역 (기본값)
        self.boundary = {'z_min': 0, 'z_max': 1000}

    def set_boundary(self, z_min, z_max):
        self.boundary['z_min'] = z_min
        self.boundary['z_max'] = z_max

    def add_portal(self, x, z, next_stage_name):
        # 포탈 생성 및 게임 월드 추가
        new_portal = Portal(x, z, next_stage_name)
        game_world.add_object(new_portal, 1)  # 1번 레이어(객체)
        self.portals.append(new_portal)  # 맵 관리 리스트에 추가

    def update(self):
        pass

    def draw(self, camera):
        sx = int(camera.left)
        max_scroll = self.world_w - camera.canvas_width
        sx = max(0, min(sx, max_scroll))

        screen_w = camera.canvas_width
        view_w_in_image = screen_w / self.scale
        clip_x = self.src_x + (sx / self.scale)
        draw_y = self.world_h // 2

        self.image.clip_draw(
            int(clip_x), int(self.src_y), int(view_w_in_image), int(self.src_h),
            screen_w // 2, draw_y,
            screen_w, self.world_h
        )