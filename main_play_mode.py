from pico2d import *
import game_framework
from characterBase import XCharacter, ZeroCharacter, SigmaCharacter, VileCharacter, UltimateArmorXCharacter


player1_index = 0
player2_index = 0
battle_mode = 'vs_player'

player1 = None
player2 = None


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
    global player1_index, player2_index, battle_mode
    player1_index = p1_index
    player2_index = p2_index
    battle_mode = mode


# 모드 초기화 시 프린트로 확인
def init():
    global player1, player2

    print(f"Player1 Index: {player1_index}")
    print(f"Player2 Index: {player2_index}")
    print(f"Battle Mode: {battle_mode}")

    player1 = create_character(player1_index, 350, 300, 1)
    player2 = create_character(player2_index, 1244, 300, 2)


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.quit()


def update():
    player1.update()
    player2.update()


def draw():
    clear_canvas()

    player1.draw()
    player2.draw()

    update_canvas()


def finish():
    pass


def pause():
    pass


def resume():
    pass