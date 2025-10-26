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

    while True:
        clear_canvas()

        update_canvas()

        if battle_mode == 'vs_cpu':
            pass
        elif battle_mode == 'vs_player2':
            pass