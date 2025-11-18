from pico2d import *
from code.player_about.player_base import draw_3d_box


class Portal:
    image = None

    def __init__(self, x, z, target_mode):
        self.x = x
        self.z = z
        self.y = 0  # 높이
        self.target_mode = target_mode

        if Portal.image is None:

            Portal.image = load_image('sprite/map/portal.png')

        # (draw_3d_box가 참조할 임시값)
        self.draw_w = 400
        self.draw_h = 300
        self.scale_x = self.draw_w / 100
        self.scale_y = self.draw_h / 100

        # --- 포탈의 충돌 박스 ---
        self.hurt_w = 100
        self.hurt_h = 250
        self.hurt_d = 100
        self.hurt_offset_x = 0
        self.hurt_offset_y = 0
        self.hurt_offset_z = 0

    def get_bb_3d(self):
        cx = self.x + self.hurt_offset_x
        cy = self.y + self.hurt_offset_y
        cz = self.z + self.hurt_offset_z

        half_w = self.hurt_w / 2
        half_d = self.hurt_d / 2

        x1 = cx - half_w
        x2 = cx + half_w
        y1 = cy
        y2 = cy + self.hurt_h
        z1 = cz - half_d
        z2 = cz + half_d

        return (x1, y1, z1, x2, y2, z2)

    def update(self):
        pass  # 플레이어가 검사

    def draw(self, camera):
        screen_x = self.x - camera.left
        screen_y = (self.z + self.y) - camera.bottom
        self.image.draw(screen_x, screen_y, 200, 200)

        # (H키로 보이도록 박스 그림)
        hurtbox = self.get_bb_3d()
        draw_3d_box(self, hurtbox, camera)