from pico2d import *


class Test_Road:
    def __init__(self):
        self.image = load_image('sprite/map/stage1.png')

        self.x = 23
        self.y = 27
        self.w = 1997
        self.h = 257

        # [핵심] 화면에 맞추지 말고, 깔끔하게 3배(또는 화면 해상도에 따라 4배)로 고정
        self.scale = 3.0

    def update(self):
        pass

    def draw(self, camera):
        # 1. 화면에 보여질 실제 크기 (Destination Size)
        dst_w = self.w * self.scale
        dst_h = self.h * self.scale

        # 2. 카메라 위치 계산 (sx)
        # 확대된 상태에서의 스크롤 한계를 계산해야 함
        max_scroll_x = dst_w - camera.canvas_width

        sx = int(camera.left)
        if sx < 0: sx = 0
        if sx > max_scroll_x: sx = max_scroll_x

        # 3. 원본 이미지에서 가져올 영역 계산 (Source Size)
        # 화면 너비(canvas_width)를 배율(scale)로 나누면 원본에서 가져와야 할 폭이 나옴
        view_w_in_image = camera.canvas_width / self.scale

        # 원본 이미지에서의 좌표 (scrolling 적용)
        # sx도 배율로 나눠줘야 원본 이미지상의 x좌표가 됨
        src_x = self.x + (sx / self.scale)
        src_y = self.y
        src_w = view_w_in_image
        src_h = self.h

        # 4. 화면에 그릴 위치 (Destination)
        # 맵을 화면 '아래쪽'에 붙여서 그립니다.
        # clip_draw의 dst_y는 중심점이므로, 바닥에 붙이려면 계산이 필요함

        # 화면 높이
        screen_h = camera.canvas_height

        # 그려질 맵의 높이
        map_draw_height = self.h * self.scale

        # 바닥에 딱 붙이기 위한 Y 중심좌표
        # (화면 바닥 0) + (그려질 맵 높이의 절반)
        dst_center_y = map_draw_height / 2

        # 만약 맵을 화면 '중앙'에 두고 싶으면 아래 주석 해제
        # dst_center_y = screen_h / 2

        self.image.clip_draw(
            int(src_x), int(src_y), int(src_w), int(src_h),  # 원본에서 가져올 부분
            camera.canvas_width // 2, int(dst_center_y),  # 화면에 그릴 중심 위치 (x는 중앙, y는 바닥 기준)
            camera.canvas_width, int(map_draw_height)  # 화면에 그려질 크기
        )

        # (디버깅용) 위쪽 남는 공간 확인
        # draw_rectangle(...)