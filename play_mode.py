from pico2d import *
from code import game_world, game_framework
from code.map import StageMap
from code.player import Player
from code.camera import Camera
from code.dummy import DummyObject
from code.player_about.player_base import check_collision_3d  # 충돌 함수 필요
from code.monster import Monster  # Monster 클래스 추가


stage_data = {
    'stage1': {
        'map_image': 'sprite/map/stage1.png',
        'src_rect': (23, 27, 1997, 257),  # 이미지 내 (x, y, w, h)
        'bound': (50, 300),  # 이동 가능 깊이 (z_min, z_max)
        'start_pos': (100, 150),  # 플레이어 시작 위치
        'portals': [  # 포탈 목록 (x, z, 이동할 스테이지 이름)
            (1800, 100, 'stage2')
        ],
        'monsters': [  # 몬스터 배치 목록 (x, z)
            (800, 150),
            (1200, 250)
        ]
    },
    'stage2': {
        'map_image': 'sprite/map/test_road.png',
        'src_rect': (0, 0, 2000, 257),  # 테스트 로드는 (0,0)부터 시작
        'bound': (50, 200),
        'start_pos': (100, 150),
        'portals': [
            (500, 150, 'stage1')
        ],
        'monsters': [
            (1500, 150),
            (300, 100)
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
        # road.add_portal 함수가 portal 객체를 road.portals에 추가한다고 가정
        road.add_portal(px, pz, next_name)

        # 5. 플레이어 생성 및 위치 설정
    player = Player()
    player.x, player.z = data['start_pos']

    # 6. 게임 월드 등록 및 충돌 그룹 등록
    game_world.add_object(road, 0)
    game_world.add_object(player, 1)

    # 7. 몬스터 생성 및 그룹 등록
    # 몬스터는 플레이어 공격의 대상(B) 그룹에 속합니다.
    # game_world.add_collision_pair('player:monster', A:플레이어, B:몬스터)
    game_world.add_collision_pair('player:monster', player, None)  # A 그룹에 플레이어 등록

    for mx, mz in data.get('monsters', []):
        monster = Monster(mx, mz)
        game_world.add_object(monster, 1)
        game_world.add_collision_pair('player:monster', None, monster)  # B 그룹에 몬스터 등록

    # 8. 카메라 설정
    camera = Camera(CANVAS_WIDTH, CANVAS_HEIGHT)
    camera.world_size(road.world_w, road.world_h)


def init():
    change_stage('stage1')  # 게임 시작 시 stage1 로드


def update():
    game_world.update()
    camera.update(player)

    # 1. 포탈 충돌 체크 (기존 로직 유지)
    for portal in road.portals:
        if check_collision_3d(player.get_bb_3d(), portal.get_bb_3d()):
            print(f"Portal Activated! -> {portal.next_stage_name}")
            change_stage(portal.next_stage_name)
            return  # 스테이지 변경 시 업데이트 종료

    # 2. 플레이어 공격 vs 몬스터 충돌 체크 (그룹 기반)
    # 플레이어가 공격 상태이고, 히트박스가 활성화되었을 때만 검사
    if player.active_hitbox:
        # 'player:monster' 그룹의 B 리스트(몬스터)를 가져옴
        monsters = game_world.collision_pairs.get('player:monster', [[], []])[1]

        # 몬스터들을 순회하며 공격 히트박스와 충돌 검사
        for monster in monsters:
            # Monster가 이미 사망했거나 제거 대상인지 확인 (필요시)
            if monster not in game_world.world[1]:
                continue

            # 충돌 검사: 플레이어 히트박스 vs 몬스터 허트박스
            if check_collision_3d(player.active_hitbox, monster.get_bb_3d()):
                # 중복 타격 방지: 해당 몬스터가 이번 공격에 이미 맞았는지 확인
                if monster not in player.hit_list:
                    # 몬스터에게 데미지 전달
                    monster.on_hit(10)
                    # 타격 성공 리스트에 추가하여 중복 타격 방지
                    player.hit_list.append(monster)
    pass


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