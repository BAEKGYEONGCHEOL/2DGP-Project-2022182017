from pico2d import *

def run():
    banner = load_image('banner.png')  # 배경
    gameTitle = load_image('game_title.png')  # 게임 제목
    directionIcon = load_image('icon_direction.png')  # 게임 모드 화살표
    vsCPUButton = load_image('vs_CPU_button.png')  # vs CPU 버튼
    vsPlayer2Button = load_image('vs_player2_button.png')  # vs 2P 버튼
    quitGame = load_image('quit_game_button.png')  # 게임 종료 버튼

    icon_x = 350  # 초기 화살표 아이콘 x 좌표

    while True:
        clear_canvas()

        banner.clip_draw(0, 0, 1594, 894, 1594 // 2, 894 // 2)
        gameTitle.clip_draw(0, 0, 1189, 148, 625, 800)
        vsCPUButton.clip_draw(0, 0, 400, 225, 350, 300)
        vsPlayer2Button.clip_draw(0, 0, 400, 225, 797, 300)
        quitGame.clip_draw(0, 0, 400, 225, 1244, 300)

        directionIcon.clip_draw(0, 0, 100, 73, icon_x, 475)

        update_canvas()

        events = get_events()
        for e in events:
            if e.type == SDL_QUIT:
                return 'QUIT'
            elif e.type == SDL_KEYDOWN:
                if icon_x > 350 and e.key == SDLK_LEFT:
                    icon_x -= 447
                elif icon_x < 1244 and e.key == SDLK_RIGHT:
                    icon_x += 447