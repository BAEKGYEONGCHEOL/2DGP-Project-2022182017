from pico2d import *

running = True
gameModeSelectMode = True
characterSelectMode = True
playGameMode = True

open_canvas()
while running:
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