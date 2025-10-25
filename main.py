from pico2d import *


def handle_events():
    global running, gameModeSelectMode, characterSelectMode, playGameMode

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = True              # 게임 루프
gameModeSelectMode = True   # 게임 모드 선택(vs 2P, vs AI, quit)
characterSelectMode = False # 캐릭터 선택 모드
playGameMode = False        # 게임 플레이 모드

open_canvas()
while running:
    handle_events()
    # 게임 모드 선택(vs 2P, vs AI, quit)
    while gameModeSelectMode:
        print('게임 모드 선택')
        break
        pass
    # 캐릭터 선택 모드
    while characterSelectMode:
        print('캐릭터 선택 모드')
        break
        pass
    # 게임 플레이 모드
    while playGameMode:
        print('게임 플레이 모드')
        break
        pass
    delay(0.01)
close_canvas()