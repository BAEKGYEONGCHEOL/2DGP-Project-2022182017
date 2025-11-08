from pico2d import *
import game_framework


player1_index = 0
player2_index = 0
battle_mode = 'vs_player'


def set_characters(p1_index, p2_index, mode):
    global player1_index, player2_index, battle_mode
    player1_index = p1_index
    player2_index = p2_index
    battle_mode = mode


# 모드 초기화 시 프린트로 확인
def init():
    print(f"Player1 Index: {player1_index}")
    print(f"Player2 Index: {player2_index}")
    print(f"Battle Mode: {battle_mode}")


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.quit()


def update():
    pass


def draw():
    clear_canvas()
    update_canvas()


def finish():
    pass


def pause(): pass
def resume(): pass