from pico2d import *
import game_framework
import game_world
import mode_select_mode  # 다시 모드 선택 모드로
from characterBase import XCharacter, ZeroCharacter, SigmaCharacter, VileCharacter, UltimateArmorXCharacter
from ground import FirstGround, SecondGround
import random
from hp import HPTool, HPBar

player1_index = 0
player2_index = 0
battle_mode = 'vs_player'

player1 = None
player2 = None

battle_background1 = None
battle_background2 = None

# 게임 종료 상태 변수
game_end = False
winner = None     # 1 또는 2
win_timer = 0
WIN_DURATION = 5.0   # 5초
# 승리 및 패배 이미지
player1_win = None  # 1P 승리 이미지
player2_win = None  # 2P 승리 이미지
player1_win_vs_cpu = None  # 1P 승리 이미지 (vs CPU 모드)
player1_lose_vs_cpu = None  # 1P 패배 이미지 (vs CPU 모드)

# bgm 추가!
battle_bgm_map1 = None
battle_bgm_map2 = None
current_bgm = None


class BattleBackground:
    def __init__(self, image_path):
        self.image = load_image(image_path)

    def update(self):
        # 배경은 움직이지 않으므로 로직 없음
        pass

    def draw(self):
        # 배경이 전체 화면을 덮도록 그림
        self.image.draw(797, 447)  # 1594 * 894 해상도 기준 중앙


# 캐릭터 생성 함수
def create_character(index, x, y, player):
    if index == 0:
        character = XCharacter(x, y, player)
    elif index == 1:
        character = ZeroCharacter(x, y, player)
    elif index == 2:
        character = SigmaCharacter(x, y, player)
    elif index == 3:
        character = VileCharacter(x, y, player)
    elif index == 4:
        character = UltimateArmorXCharacter(x, y, player)

    # 초기 상태 INTRO로 설정
    character.state_machine.cur_state = character.INTRO

    return character



# 플레이어 캐릭터 및 모드 설정 함수
def set_characters(p1_index, p2_index, mode):
    global player1_index, player2_index, battle_mode, battle_background1, battle_background2
    player1_index = p1_index
    player2_index = p2_index
    battle_mode = mode


# 모드 초기화 시 프린트로 확인
def init():
    global current_map, player1, player2, player1_win, player2_win, player1_win_vs_cpu, player1_lose_vs_cpu, game_end, winner, win_timer, WIN_DURATION, battle_mode
    global battle_bgm_map1, battle_bgm_map2, current_bgm

    # 게임 종료 상태 변수
    game_end = False
    winner = None  # 1 또는 2
    win_timer = 0
    WIN_DURATION = 5.0  # 5초

    player1_win = load_image('player1_win.png')
    player2_win = load_image('player2_win.png')
    player1_win_vs_cpu = load_image('player1_win_vs_cpu.png')
    player1_lose_vs_cpu = load_image('player1_lose_vs_cpu.png')

    print(f"Player1 Index: {player1_index}")
    print(f"Player2 Index: {player2_index}")
    print(f"Battle Mode: {battle_mode}")

    # 맵 2개중 하나 랜덤으로 생성!
    map_list = [FirstGround, SecondGround]
    current_map = random.choice(map_list)()

    game_world.add_object(current_map, 0)

    player1 = create_character(player1_index, 350, 150, 1)
    player2 = create_character(player2_index, 1244, 150, 2)

    game_world.add_object(player1, 1)
    game_world.add_object(player2, 1)

    hp_tool1 = HPTool(350, 825)
    hp_bar1 = HPBar(player1, 350, 825, 1)
    hp_tool2 = HPTool(1244, 825)
    hp_bar2 = HPBar(player2, 1244, 825, 2)

    game_world.add_object(hp_tool1, 3)
    game_world.add_object(hp_bar1, 3)
    game_world.add_object(hp_tool2, 3)
    game_world.add_object(hp_bar2, 3)

    game_world.add_collision_pair('ground:p1_body', current_map, player1)
    game_world.add_collision_pair('ground:p2_body', current_map, player2)

    game_world.add_collision_pair('p1_attack:p2_body', player1, player2)
    game_world.add_collision_pair('p2_attack:p1_body', player2, player1)

    game_world.add_collision_pair('p1_wave:p2_body', None, player2)
    game_world.add_collision_pair('p2_wave:p1_body', None, player1)

    game_world.add_collision_pair('p1_reflect:p2_wave', player1, None)
    game_world.add_collision_pair('p2_reflect:p1_wave', player2, None)


    # bgm 로드!
    battle_bgm_map1 = load_music('main_bgm_x_and_zero.wav')
    battle_bgm_map2 = load_music('main_bgm_sigma.wav')

    battle_bgm_map1.set_volume(64)
    battle_bgm_map2.set_volume(64)

    # 맵에 따라 bgm 재생
    if isinstance(current_map, FirstGround):
        current_bgm = battle_bgm_map1
    elif isinstance(current_map, SecondGround):
        current_bgm = battle_bgm_map2

    if current_bgm:
        current_bgm.play(-1)


    # CPU 모드면 행동트리 연결!
    if battle_mode == 'vs_cpu':
        player1.target = player2
        player2.target = player1
        player2.build_behavior_tree()  # 행동 트리 생성!

    # 플레이어 모드면 서로 타겟 연결!
    if battle_mode == 'vs_player':
        player1.target = player2
        player2.target = player1


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE and not game_end:
                # game_framework.quit()
                game_framework.change_mode(mode_select_mode)

        player1.handle_event(e)

        if battle_mode == 'vs_player':
            # 2P 모드 -> P2도 직접 조작
            player2.handle_event(e)


def update():
    global game_end, winner, win_timer

    game_world.update()
    game_world.handle_collision()

    if not game_end:
        # CPU 모드일 때 AI 실행!
        if battle_mode == 'vs_cpu' and player2.bt:
            player2.bt.run()

        # 승패 판정
        if player1.current_hp <= 0:
            game_end = True
            winner = 2
        elif player2.current_hp <= 0:
            game_end = True
            winner = 1

    else:
        win_timer += game_framework.frame_time
        if win_timer >= WIN_DURATION:
            game_framework.change_mode(mode_select_mode)


def draw():
    clear_canvas()

    game_world.render()

    if game_end:
        if winner == 1:
            if battle_mode == 'vs_cpu':
                player1_win_vs_cpu.draw(797, 447)
            else:
                player1_win.draw(797, 447)
        else:
            if battle_mode == 'vs_cpu':
                player1_lose_vs_cpu.draw(797, 447)
            else:
                player2_win.draw(797, 447)

    update_canvas()


def finish():
    # 브금 멈추기!
    global current_bgm
    if current_bgm:
        current_bgm.stop()
        current_bgm = None

    game_world.clear()


def pause():
    pass


def resume():
    pass