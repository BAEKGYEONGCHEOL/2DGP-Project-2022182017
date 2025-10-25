from pico2d import *
import mode_select_mode
import character_select_mode
import main_play_mode

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

running = True              # 게임 루프
game_mode_state = 'mode_select' # 현재 게임 모드 상태

open_canvas(1594, 894)
while running:
    handle_events()
    # 게임 모드 선택(vs 2P, vs AI, quit)
    if game_mode_state == 'mode_select':
        cur_state = mode_select_mode.run()
    # 캐릭터 선택 모드
    elif game_mode_state == 'character_select':
        cur_state = character_select_mode.run()
    # 게임 플레이 모드
    elif game_mode_state == 'main_play':
        cur_state = main_play_mode.run()

    game_mode_state = cur_state
    if game_mode_state == 'QUIT':
        running = False

    delay(0.01)
close_canvas()