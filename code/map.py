from pico2d import *


class StageMap:
    def __init__(self, file_name, x, y, w, h, scale=3.0):
        self.image = load_image(file_name)
        self.src_x, self.src_y = x, y
        self.src_w, self.src_h = w, h
        self.scale = scale

        # 확대된 맵의 실제 월드 크기
        self.world_w = int(w * scale)
        self.world_h = int(h * scale)

    def update(self):
        pass

    def draw(self, camera):
        sx = int(camera.left)

        # 스크롤 범위 제한 (0 ~ 맵 끝)
        max_scroll = self.world_w - camera.canvas_width
        sx = max(0, min(sx, max_scroll))

        # 화면 너비만큼 원본에서 가져올 폭 계산
        view_w = camera.canvas_width / self.scale
        clip_x = self.src_x + (sx / self.scale)

        # 화면 바닥에 맵을 붙여서 그리기 위한 Y 중심좌표
        draw_y = self.world_h // 2

        self.image.clip_draw(
            int(clip_x), int(self.src_y), int(view_w), int(self.src_h),
            camera.canvas_width // 2, draw_y,
            camera.canvas_width, self.world_h
        )