from pico2d import *
from code import game_world, game_framework
from code.map import StageMap
from code.player import Player
from code.camera import Camera
from code.dummy import DummyObject
from code.player_about.player_base import check_collision_3d  # 충돌 함수 필요

# ====================================================
# [1] 스테이지 데이터 정의 (여기에 맵 정보를 다 적으세요)
# ====================================================
stage_data = {
    'stage1': {
        'map_image': 'sprite/map/stage1.png',
        'src_rect': (23, 27, 1997, 257),  # 이미지 내 (x, y, w, h)
        'bound': (50, 300),  # 이동 가능 깊이 (z_min, z_max)
        'start_pos': (100, 150),  # 플레이어 시작 위치
        'portals': [  # 포탈 목록 (x, z, 이동할 스테이지 이름)
            (1800, 150, 'stage2')
        ]
    },
    'stage2': {
        'map_image': 'sprite/map/test_road.png',
        'src_rect': (0, 0, 2000, 257),  # 테스트 로드는 (0,0)부터 시작
        'bound': (50, 200),
        'start_pos': (100, 150),
        'portals': [
            (500, 150, 'stage1')  # 다시 1스테이지로 돌아가는 포탈 (필요시)
        ]
    }
}
# ====================================================

CANVAS_WIDTH, CANVAS_HEIGHT = 800, 600
player = None
camera = None
road = None


def change_stage(stage_name):
    global player, camera, road

    # 1. 기존 객체 싹 비우기
    game_world.clear()

    # 2. 새 스테이지 데이터 가져오기
    if stage_name not in stage_data:
        print(f"Error: {stage_name} does not exist!")
        return

    data = stage_data[stage_name]

    # 3. 맵 생성
    src_x, src_y, src_w, src_h = data['src_rect']
    road = StageMap(data['map_image'], src_x, src_y, src_w, src_h, scale=3.0)
    road.set_boundary(*data['bound'])

    # 4. 포탈 배치
    for px, pz, next_name in data['portals']:
        road.add_portal(px, pz, next_name)

    # 5. 플레이어 생성 및 위치 설정
    player = Player()
    player.x, player.z = data['start_pos']

    # 6. 게임 월드 등록
    game_world.add_object(road, 0)
    game_world.add_object(player, 1)

    # (테스트용 몬스터)
    if stage_name == 'stage1':
        game_world.add_object(DummyObject(800, 150), 1)
    elif stage_name == 'stage2':
        game_world.add_object(DummyObject(1200, 100), 1)

    # 7. 카메라 설정
    camera = Camera(CANVAS_WIDTH, CANVAS_HEIGHT)
    camera.world_size(road.world_w, road.world_h)


def init():
    change_stage('stage1')  # 게임 시작 시 stage1 로드


def update():
    game_world.update()
    camera.update(player)

    # [포탈 충돌 체크] - play_mode에서 직접 관리
    # 맵에 있는 모든 포탈을 검사
    for portal in road.portals:
        if check_collision_3d(player.get_bb_3d(), portal.get_bb_3d()):
            print(f"Portal Activated! -> {portal.next_stage_name}")
            change_stage(portal.next_stage_name)  # 스테이지 변경 함수 호출
            break  # 변경되었으므로 루프 종료


def draw():
    clear_canvas()
    game_world.render(camera)
    update_canvas()


def finish():
    game_world.clear()


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)