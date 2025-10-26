from pico2d import *

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

        update_canvas()

        events = get_events()
        for e in events:
            if e.type == SDL_QUIT:
                return 'QUIT'
            elif e.type == SDL_KEYDOWN:
                # 플레이어 1 캐릭터 선택 아이콘 이동
                if player1_icon_x > 174 and e.key == SDLK_LEFT:
                    player1_icon_x -= 276
                elif player1_icon_x < 1278 and e.key == SDLK_RIGHT:
                    player1_icon_x += 276

                # 플레이어 2 캐릭터 선택 아이콘 이동
                if player2_icon_x > 312 and e.key == SDLK_KP_4:
                    player2_icon_x -= 276
                elif player2_icon_x < 1416 and e.key == SDLK_KP_6:
                    player2_icon_x += 276

        if battle_mode == 'vs_cpu':
            pass
        elif battle_mode == 'vs_player2':
            pass