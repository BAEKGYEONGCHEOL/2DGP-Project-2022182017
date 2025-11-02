from pico2d import *
from characterBase import XCharacter, ZeroCharacter, SigmaCharacter, VileCharacter, UltimateArmorXCharacter


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


def run(battle_mode):
    background = load_image('select_character_background.png')  # 배경
    characterSelectViewSlot = load_image('character_select_view_slot.png')  # 캐릭터 선택 뷰 슬롯
    player1IconDirection = load_image('player1_icon_direction.png') # 플레이어1 방향 아이콘
    player2IconDirection = load_image('player2_icon_direction.png') # 플레이어2 방향 아이콘
    slot1 = load_image('character_select_slot_1.png')   # 캐릭터 슬롯1
    slot2 = load_image('character_select_slot_2.png')   # 캐릭터 슬롯2
    slot3 = load_image('character_select_slot_3.png')   # 캐릭터 슬롯3
    slot4 = load_image('character_select_slot_4.png')   # 캐릭터 슬롯4
    slot5 = load_image('character_select_slot_5.png')   # 캐릭터 슬롯5

    player1_icon_x = 174
    player2_icon_x = 312

    # 플레이어 별 캐릭터 뷰 위치
    player1_character_view_x = 444
    player1_character_view_y = 645
    player2_character_view_x = 1150
    player2_character_view_y = 645

    # 플레이어 캐릭터 인덱스
    player1_index = 0
    player2_index = 0

    # 플레이어1 캐릭터 객체 생성
    player1_character = draw_character_select_screen(player1_index, player1_character_view_x,
                                                     player1_character_view_y, 0, 1)
    # 플레이어2 캐릭터 객체 생성
    player2_character = draw_character_select_screen(player2_index, player2_character_view_x,
                                                     player2_character_view_y, 0, 2)

    while True:
        clear_canvas()

        background.clip_draw(0, 0, 1594, 894, 1594 // 2, 894 // 2)
        characterSelectViewSlot.clip_draw(0, 0, 600, 426, 444, 645)
        characterSelectViewSlot.clip_draw(0, 0, 600, 426, 1150, 645)
        slot1.clip_draw(0, 0, 276, 276, 243, 190)
        slot2.clip_draw(0, 0, 276, 276, 519, 190)
        slot3.clip_draw(0, 0, 276, 276, 795, 190)
        slot4.clip_draw(0, 0, 276, 276, 1071, 190)
        slot5.clip_draw(0, 0, 276, 276, 1347, 190)

        player1IconDirection.clip_draw(0, 0, 100, 73, player1_icon_x, 375)
        player2IconDirection.clip_draw(0, 0, 100, 73, player2_icon_x, 375)

        # 플레이어에 따라 캐릭터 객체 업데이트 및 그리기
        player1_character.update()
        player1_character.draw()
        player2_character.update()
        player2_character.draw()

        update_canvas()

        events = get_events()
        for e in events:
            if e.type == SDL_QUIT:
                return 'QUIT'
            elif e.type == SDL_KEYDOWN:
                # 플레이어 1 캐릭터 선택 아이콘 이동
                if player1_icon_x > 174 and e.key == SDLK_LEFT:
                    player1_icon_x -= 276
                    player1_index -= 1
                    # 플레이어1 캐릭터 객체 생성
                    player1_character = draw_character_select_screen(player1_index,
                                                                     player1_character_view_x,
                                                                     player1_character_view_y, 0, 1)
                elif player1_icon_x < 1278 and e.key == SDLK_RIGHT:
                    player1_icon_x += 276
                    player1_index += 1
                    # 플레이어1 캐릭터 객체 생성
                    player1_character = draw_character_select_screen(player1_index,
                                                                     player1_character_view_x,
                                                                     player1_character_view_y, 0, 1)
                # 플레이어 2 캐릭터 선택 아이콘 이동
                if player2_icon_x > 312 and e.key == SDLK_KP_4:
                    player2_icon_x -= 276
                    player2_index -= 1
                    # 플레이어2 캐릭터 객체 생성
                    player2_character = draw_character_select_screen(player2_index,
                                                                     player2_character_view_x,
                                                                     player2_character_view_y, 0, 2)
                elif player2_icon_x < 1416 and e.key == SDLK_KP_6:
                    player2_icon_x += 276
                    player2_index += 1
                    # 플레이어2 캐릭터 객체 생성
                    player2_character = draw_character_select_screen(player2_index,
                                                                     player2_character_view_x,
                                                                     player2_character_view_y, 0, 2)

                if e.key == SDLK_ESCAPE:
                    return 'mode_select'


        if battle_mode == 'vs_cpu':
            pass
        elif battle_mode == 'vs_player2':
            pass