from pico2d import *
import game_framework
import character_select_mode  # 다음 모드 예시

banner = None
gameTitle = None
directionIcon = None
vsCPUButton = None
vsPlayer2Button = None
quitGame = None
icon_x = 350


def init():
    global banner, gameTitle, directionIcon, vsCPUButton, vsPlayer2Button, quitGame, icon_x

    banner = load_image('banner.png')  # 배경
    gameTitle = load_image('game_title.png')  # 게임 제목
    directionIcon = load_image('icon_direction.png')  # 게임 모드 화살표
    vsCPUButton = load_image('vs_CPU_button.png')  # vs CPU 버튼
    vsPlayer2Button = load_image('vs_player2_button.png')  # vs 2P 버튼
    quitGame = load_image('quit_game_button.png')  # 게임 종료 버튼

    icon_x = 350


def finish():
    global banner, gameTitle, directionIcon, vsCPUButton, vsPlayer2Button, quitGame
    del banner, gameTitle, directionIcon, vsCPUButton, vsPlayer2Button, quitGame


def handle_events():
    global icon_x
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT and icon_x > 350:
                icon_x -= 447
            elif e.key == SDLK_RIGHT and icon_x < 1244:
                icon_x += 447
            elif e.key == SDLK_RETURN:
                if icon_x == 350:
                    # vs CPU
                    character_select_mode.set_battle_mode('vs_cpu')
                    game_framework.change_mode(character_select_mode)
                elif icon_x == 797:
                    # vs 2P
                    character_select_mode.set_battle_mode('vs_player')
                    game_framework.change_mode(character_select_mode)
                elif icon_x == 1244:
                    # 종료
                    game_framework.quit()


def update():
    pass


def draw():
    clear_canvas()
    banner.clip_draw(0, 0, 1594, 894, 1594 // 2, 894 // 2)
    gameTitle.clip_draw(0, 0, 1189, 148, 625, 800)
    vsCPUButton.clip_draw(0, 0, 400, 225, 350, 300)
    vsPlayer2Button.clip_draw(0, 0, 400, 225, 797, 300)
    quitGame.clip_draw(0, 0, 400, 225, 1244, 300)
    directionIcon.clip_draw(0, 0, 100, 73, icon_x, 475)
    update_canvas()


def pause():
    pass


def resume():
    pass