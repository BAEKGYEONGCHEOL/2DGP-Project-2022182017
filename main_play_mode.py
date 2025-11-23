from pico2d import *
import game_framework
import game_world
import mode_select_mode  # 다시 모드 선택 모드로
from characterBase import XCharacter, ZeroCharacter, SigmaCharacter, VileCharacter, UltimateArmorXCharacter
from ground import FirstGround, SecondGround
import random


player1_index = 0
player2_index = 0
battle_mode = 'vs_player'

player1 = None
player2 = None

battle_background1 = None
battle_background2 = None


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
    # character.state_machine.cur_state = character.INTRO

    return character



# 플레이어 캐릭터 및 모드 설정 함수
def set_characters(p1_index, p2_index, mode):
    global player1_index, player2_index, battle_mode, battle_background1, battle_background2
    player1_index = p1_index
    player2_index = p2_index
    battle_mode = mode


# 모드 초기화 시 프린트로 확인
def init():
    global current_map, player1, player2

    print(f"Player1 Index: {player1_index}")
    print(f"Player2 Index: {player2_index}")
    print(f"Battle Mode: {battle_mode}")

    # 맵 2개중 하나 랜덤으로 생성!
    map_list = [FirstGround, SecondGround]
    current_map = random.choice(map_list)()

    game_world.add_object(current_map, 0)

    player1 = create_character(player1_index, 350, 225, 1)
    player2 = create_character(player2_index, 1244, 225, 2)

    game_world.add_object(player1, 1)
    game_world.add_object(player2, 1)

    game_world.add_collision_pair('ground:p1_body', current_map, player1)
    game_world.add_collision_pair('ground:p2_body', current_map, player2)

    game_world.add_collision_pair('p1_attack:p2_body', player1, player2)
    game_world.add_collision_pair('p2_attack:p1_body', player2, player1)

    game_world.add_collision_pair('p1_wave:p2_body', None, player2)
    game_world.add_collision_pair('p2_wave:p1_body', None, player1)

    game_world.add_collision_pair('p1_reflect:p2_wave', player1, None)
    game_world.add_collision_pair('p2_reflect:p1_wave', player2, None)


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                # game_framework.quit()
                game_framework.change_mode(mode_select_mode)

        player1.handle_event(e)
        player2.handle_event(e)


def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()

    game_world.render()

    update_canvas()


def finish():
    game_world.clear()


def pause():
    pass


def resume():
    pass