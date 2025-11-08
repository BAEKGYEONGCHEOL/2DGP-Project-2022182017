from pico2d import *
import game_framework
import mode_select_mode  # 다시 모드 선택 모드로
import main_play_mode    # 선택 후 플레이 모드로
from characterBase import XCharacter, ZeroCharacter, SigmaCharacter, VileCharacter, UltimateArmorXCharacter

background = None   # 배경
characterSelectViewSlot = None  # 캐릭터 선택 뷰 슬롯
player1IconDirection = None # 플레이어1 방향 아이콘
player2IconDirection = None # 플레이어2 방향 아이콘
slot_images = None  # 캐릭터 슬롯 1~5


player1_icon_x, player2_icon_x = 174, 312
# 플레이어 캐릭터 인덱스
player1_index, player2_index = 0, 0
# 플레이어1, 2 캐릭터 객체
player1_character, player2_character = None, None


# 플레이어 객체 생성 함수
def draw_character_select_screen(index, x, y, speed, player):
    if index == 0:
        player_character = XCharacter(x, y, speed, player)
    elif index == 1:
        player_character = ZeroCharacter(x, y, speed, player)
    elif index == 2:
        player_character = SigmaCharacter(x, y, speed, player)
    elif index == 3:
        player_character = VileCharacter(x, y, speed, player)
    elif index == 4:
        player_character = UltimateArmorXCharacter(x, y, speed, player)

    # 초기 상태 INTRO로 설정
    player_character.state_machine.cur_state = player_character.INTRO

    return player_character


def init():
    global background, characterSelectViewSlot, player1IconDirection, player2IconDirection, slot_images, player1_icon_x, player2_icon_x, player1_index, player2_index, player1_character, player2_character

    open_canvas(1594, 894)

    background = load_image('select_character_background.png')
    characterSelectViewSlot = load_image('character_select_view_slot.png')
    player1IconDirection = load_image('player1_icon_direction.png')
    player2IconDirection = load_image('player2_icon_direction.png')
    slot_images = [
        load_image('character_select_slot_1.png'),
        load_image('character_select_slot_2.png'),
        load_image('character_select_slot_3.png'),
        load_image('character_select_slot_4.png'),
        load_image('character_select_slot_5.png')
    ]

    player1_icon_x, player2_icon_x = 174, 312
    player1_index, player2_index = 0, 0

    # 캐릭터 표시 위치
    player1_character = draw_character_select_screen(player1_index, 444, 645, 0, 1)
    player2_character = draw_character_select_screen(player2_index, 1150, 645, 0, 2)


def finish():
    global background, characterSelectViewSlot, player1IconDirection, player2IconDirection, slot_images
    del background, characterSelectViewSlot, player1IconDirection, player2IconDirection
    for s in slot_images:
        del s
    close_canvas()


def handle_events():
    global player1_icon_x, player2_icon_x
    global player1_index, player2_index
    global player1_character, player2_character

    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()

        elif e.type == SDL_KEYDOWN:
            # 다시 모드 선택 모드로
            if e.key == SDLK_ESCAPE:
                game_framework.change_mode(mode_select_mode)

            # 플레이어 1 캐릭터 선택 아이콘 이동
            elif e.key == SDLK_LEFT and player1_icon_x > 174:
                player1_icon_x -= 276
                player1_index -= 1
                # 플레이어1 캐릭터 객체 생성
                player1_character = draw_character_select_screen(player1_index, 444, 645, 0, 1)
            elif e.key == SDLK_RIGHT and player1_icon_x < 1278:
                player1_icon_x += 276
                player1_index += 1
                # 플레이어1 캐릭터 객체 생성
                player1_character = draw_character_select_screen(player1_index, 444, 645, 0, 1)

            # 플레이어 2 캐릭터 선택 아이콘 이동
            elif e.key == SDLK_KP_4 and player2_icon_x > 312:
                player2_icon_x -= 276
                player2_index -= 1
                # 플레이어2 캐릭터 객체 생성
                player2_character = draw_character_select_screen(player2_index, 1150, 645, 0, 2)
            elif e.key == SDLK_KP_6 and player2_icon_x < 1416:
                player2_icon_x += 276
                player2_index += 1
                # 플레이어2 캐릭터 객체 생성
                player2_character = draw_character_select_screen(player2_index, 1150, 645, 0, 2)

            # Enter → 다음 모드로 진입
            elif e.key == SDLK_RETURN:
                import main_play
                main_play.set_characters(player1_index, player2_index, battle_mode)
                game_framework.change_mode(main_play)


def update():
    player1_character.update()
    player2_character.update()


def draw():
    clear_canvas()
    background.clip_draw(0, 0, 1594, 894, 1594 // 2, 894 // 2)
    characterSelectViewSlot.clip_draw(0, 0, 600, 426, 444, 645)
    characterSelectViewSlot.clip_draw(0, 0, 600, 426, 1150, 645)

    # 슬롯 5개 이동
    x = 243
    for slot in slot_images:
        slot.clip_draw(0, 0, 276, 276, x, 190)
        x += 276

    # 아이콘 위치
    player1IconDirection.clip_draw(0, 0, 100, 73, player1_icon_x, 375)
    player2IconDirection.clip_draw(0, 0, 100, 73, player2_icon_x, 375)

    # 캐릭터 미리보기
    player1_character.draw()
    player2_character.draw()
    update_canvas()


def pause():
    pass


def resume():
    pass