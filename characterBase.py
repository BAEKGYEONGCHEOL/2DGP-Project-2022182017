from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP
from spriteSheet import mmx_x4_x_sheet, zerox4sheet, x5sigma4, Dynamox56sheet, ultimate_armor_x

from state_machine import StateMachine

def time_out(e):
    return e[0] == 'TIME_OUT'

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].type == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].type == SDLK_RIGHT


# Intro 상태
class Intro:

    def __init__(self, character, max_frame, delay):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = delay   # 프레임 상태마다 다르게 구현
        self.last_update_time = get_time()  # 마지막 업데이트 시간(현재 시간에서 마지막 시간을 빼서 딜레이 보다 크면 다음 프레임으로!)

    def enter(self, e):
        self.frame = 0
        self.character.current_frame = 0    # current_frame 초기화!

    def exit(self, e):
        pass

    def do(self):
        time = get_time()
        if time - self.last_update_time >= self.delay:
            self.frame += 1
            self.last_update_time = time

            if self.frame >= len(self.character.frame['intro']):
                self.character.state_machine.handle_state_event(('TIME_OUT', None))
            else:
                self.character.current_frame = self.frame

    def draw(self):
        frame_data = self.character.frame['intro'][self.character.current_frame]
        x_data, y_data, w_data, h_data = frame_data
        # 플레이어 1(기본 방향: 우측)
        # 캐릭터의 사진이 좌측 방향을 보고 있어서 우측 방향으로 바꾸어야 한다면!
        if self.character.player == 1:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
        # 플레이어 2(기본 방향: 좌측)
        # 캐릭터의 사진이 우측 방향을 보고 있어서 좌측 방향으로 바꾸어야 한다면!
        elif self.character.player == 2:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)


# Idle 상태
class Idle:

    def __init__(self, character, max_frame, delay):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = delay   # 프레임 상태마다 다르게 구현
        self.last_update_time = get_time()  # 마지막 업데이트 시간(현재 시간에서 마지막 시간을 빼서 딜레이 보다 크면 다음 프레임으로!)

    def enter(self, e):
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        pass

    def do(self):
        time = get_time()
        if time - self.last_update_time >= self.delay:
            self.frame = (self.frame + 1) % len(self.character.frame['idle'])
            self.last_update_time = time
            self.character.current_frame = self.frame

    def draw(self):
        frame_data = self.character.frame['idle'][self.character.current_frame]
        x_data, y_data, w_data, h_data = frame_data
        # 플레이어 1(기본 방향: 우측)
        # 캐릭터의 사진이 좌측 방향을 보고 있어서 우측 방향으로 바꾸어야 한다면!
        if self.character.player == 1:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
        # 플레이어 2(기본 방향: 좌측)
        # 캐릭터의 사진이 우측 방향을 보고 있어서 좌측 방향으로 바꾸어야 한다면!
        elif self.character.player == 2:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)


# Walk 상태
class Walk:

    def __init__(self, character, max_frame, delay):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = delay   # 프레임 상태마다 다르게 구현
        self.last_update_time = get_time()  # 마지막 업데이트 시간(현재 시간에서 마지막 시간을 빼서 딜레이 보다 크면 다음 프레임으로!)

    def enter(self, e):
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        pass

    def do(self):
        time = get_time()
        if time - self.last_update_time >= self.delay:
            self.frame = (self.frame + 1) % len(self.character.frame['walk'])
            self.last_update_time = time
            self.character.current_frame = self.frame

    def draw(self):
        frame_data = self.character.frame['walk'][self.character.current_frame]
        x_data, y_data, w_data, h_data = frame_data
        # 플레이어 1(기본 방향: 우측)
        # 캐릭터의 사진이 좌측 방향을 보고 있어서 우측 방향으로 바꾸어야 한다면!
        if self.character.player == 1:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
        # 플레이어 2(기본 방향: 좌측)
        # 캐릭터의 사진이 우측 방향을 보고 있어서 좌측 방향으로 바꾸어야 한다면!
        elif self.character.player == 2:
            if self.character.change_facing_right:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, '', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)
            else:
                self.character.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, 'h', self.character.x,
                                                    self.character.y, w_data * 3, h_data * 3)


# Jump 상태
class Jump:
    pass


# Base Attack 상태
class BaseAttack:
    pass


# Power Attack 상태
class PowerAttack:
    pass


# Dash 상태
class Dash:
    pass


# Hit 상태
class Hit:
    pass


# Defeat 상태
class Defeat:
    pass


class Character:
    def __init__(self, image_path, x, y, speed, sheet_data, player, change_facing_right):
        self.image = load_image(image_path)    # 캐릭터 이미지 로드
        self.x = x
        self.y = y
        self.player = player
        self.change_facing_right = change_facing_right  # 캐릭터의 기본 방향은 우측 방향!

        self.current_frame = 0  # 현재 프레임 인덱스
        self.speed = speed

        # 자식 클래스 생성 시 프레임, 딜레이 데이터를 딕셔너리 형태로 저장
        self.frame = {}
        self.delay = {}

        self.state_machine = None

    def update(self):
        if self.state_machine:
            self.state_machine.update()

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()

    def handle_event(self, event):
        if self.state_machine:
            self.state_machine.handle_state_event(('INPUT', event))


# ===================================================================
# 각자 개인 캐릭터 클래스 구현!
# ===================================================================

# X 캐릭터 클래스
class XCharacter(Character):
    def __init__(self, x, y, speed, player):
        super().__init__('mmx_x4_x_sheet.png', x, y, speed, mmx_x4_x_sheet, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': mmx_x4_x_sheet[0],
            'idle': mmx_x4_x_sheet[1],
            'walk': mmx_x4_x_sheet[2],
            'jump': mmx_x4_x_sheet[3],
            'base_attack': mmx_x4_x_sheet[4],
            'power_attack': mmx_x4_x_sheet[5],
            'dash': mmx_x4_x_sheet[6],
            'hit': mmx_x4_x_sheet[7],
            'defeat': mmx_x4_x_sheet[8],
        }

        self.delay = {
            'intro': 0.1,
            'idle': 0.1,
            'walk': 0.1,
            'jump': 0.1,
            'base_attack': 0.1,
            'power_attack': 0.1,
            'dash': 0.1,
            'hit': 0.1,
            'defeat': 0.1,
        }

        self.INTRO = Intro(self, len(self.frame['intro']), self.delay['intro'])
        self.IDLE = Idle(self, len(self.frame['idle']), self.delay['idle'])
        self.WALK = Walk(self, len(self.frame['walk']), self.delay['walk'])
        # self.JUMP = Jump(self, len(self.frame['jump']), self.delay['jump'])
        # self.BASE_ATTACK = BaseAttack(self, len(self.frame['base_attack']), self.delay['base_attack'])
        # self.POWER_ATTACK = PowerAttack(self, len(self.frame['power_attack']), self.delay['power_attack'])
        # self.DASH = Dash(self, len(self.frame['dash']), self.delay['dash'])
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                # INTRO 상태에서 해당 INTRO 프레임이 끝나는 이벤트(time_out)가 발생하면 IDLE 상태가 됨
                self.INTRO: {time_out: self.IDLE},
                # IDLE 상태(RUN 상태에서 양쪽 방향키를 동시에 눌렀을 때)에서 한 쪽 방향키를 떼었을 때 반대 방향으로 달리게 하기 위해서 right_down, right_up, left_down, left_up 이벤트도 추가, a키를 누르면 AUTO_RUN 상태로 변환!
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK},
                # 여기서 right_down 과 left_down 은 RUN 상태에서 반대 방향키를 눌렀을 때 IDLE 상태로 가게 되는 경우이다.
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE},
            }
        )


# Zero 캐릭터 클래스
class ZeroCharacter(Character):
    def __init__(self, x, y, speed, player):
        super().__init__('zerox4sheet.png', x, y, speed, zerox4sheet, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': zerox4sheet[0],
            'idle': zerox4sheet[1],
            'walk': zerox4sheet[2],
            'jump': zerox4sheet[3],
            'base_attack': zerox4sheet[4],
            'dash_attack': zerox4sheet[5],
            'dash': zerox4sheet[6],
            'hit': zerox4sheet[7],
            'defeat': zerox4sheet[8],
        }

        self.delay = {
            'intro': 0.1,
            'idle': 0.1,
            'walk': 0.1,
            'jump': 0.1,
            'base_attack': 0.1,
            'dash_attack': 0.1,
            'dash': 0.1,
            'hit': 0.1,
            'defeat': 0.1,
        }

        self.INTRO = Intro(self, len(self.frame['intro']), self.delay['intro'])
        self.IDLE = Idle(self, len(self.frame['idle']), self.delay['idle'])
        self.WALK = Walk(self, len(self.frame['walk']), self.delay['walk'])
        # self.JUMP = Jump(self, len(self.frame['jump']), self.delay['jump'])
        # self.BASE_ATTACK = BaseAttack(self, len(self.frame['base_attack']), self.delay['base_attack'])
        # self.DASH_ATTACK = DashAttack(self, len(self.frame['dash_attack']), self.delay['dash_attack'])
        # self.DASH = Dash(self, len(self.frame['dash']), self.delay['dash'])
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE},
            }
        )


# Sigma 캐릭터 클래스
class SigmaCharacter(Character):
    def __init__(self, x, y, speed, player):
        super().__init__('x5sigma4.png', x, y, speed, x5sigma4, player, True)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': x5sigma4[0],
            'idle': x5sigma4[1],
            'walk': x5sigma4[2],
            'teleport': x5sigma4[3],
            'base_attack': x5sigma4[4],
            'sphere_attack': x5sigma4[5],
            'wave_attack': x5sigma4[6],
            'dash_attack': x5sigma4[7],
            'hit': x5sigma4[8],
            'defeat': x5sigma4[9],
        }

        self.delay = {
            'intro': 0.1,
            'idle': 0.1,
            'walk': 0.1,
            'teleport': 0.1,
            'base_attack': 0.1,
            'sphere_attack': 0.1,
            'wave_attack': 0.1,
            'dash_attack': 0.1,
            'hit': 0.1,
            'defeat': 0.1,
        }

        self.INTRO = Intro(self, len(self.frame['intro']), self.delay['intro'])
        self.IDLE = Idle(self, len(self.frame['idle']), self.delay['idle'])
        self.WALK = Walk(self, len(self.frame['walk']), self.delay['walk'])
        # self.TELEPORT = Teleport(self, len(self.frame['teleport']), self.delay['teleport'])
        # self.BASE_ATTACK = BaseAttack(self, len(self.frame['base_attack']), self.delay['base_attack'])
        # self.SPHERE_ATTACK = SphereAttack(self, len(self.frame['sphere_attack']), self.delay['sphere_attack'])
        # self.WAVE_ATTACK = WaveAttack(self, len(self.frame['wave_attack']), self.delay['wave_attack'])
        # self.DASH_ATTACK = DashAttack(self, len(self.frame['dash_attack']), self.delay['dash_attack'])
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE},
            }
        )


# Vile 캐릭터 클래스
class VileCharacter(Character):
    def __init__(self, x, y, speed, player):
        super().__init__('Dynamox56sheet.png', x, y, speed, Dynamox56sheet, player, True)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': Dynamox56sheet[0],
            'idle': Dynamox56sheet[1],
            'walk': Dynamox56sheet[2],
            'teleport': Dynamox56sheet[3],
            'base_attack': Dynamox56sheet[4],
            'reflex_attack': Dynamox56sheet[5],
            'dash_attack': Dynamox56sheet[6],
            'ambient_wave_attack': Dynamox56sheet[7],
            'hit': Dynamox56sheet[8],
            'defeat': Dynamox56sheet[9],
        }

        self.delay = {
            'intro': 0.1,
            'idle': 0.1,
            'walk': 0.1,
            'teleport': 0.1,
            'base_attack': 0.1,
            'reflex_attack': 0.1,
            'dash_attack': 0.1,
            'ambient_wave_attack': 0.1,
            'hit': 0.1,
            'defeat': 0.1,
        }

        self.INTRO = Intro(self, len(self.frame['intro']), self.delay['intro'])
        self.IDLE = Idle(self, len(self.frame['idle']), self.delay['idle'])
        self.WALK = Walk(self, len(self.frame['walk']), self.delay['walk'])
        # self.TELEPORT = Teleport(self, len(self.frame['teleport']), self.delay['teleport'])
        # self.BASE_ATTACK = BaseAttack(self, len(self.frame['base_attack']), self.delay['base_attack'])
        # self.REFLEX_ATTACK = ReflexAttack(self, len(self.frame['reflex_attack']), self.delay['reflex_attack'])
        # self.DASH_ATTACK = DashAttack(self, len(self.frame['dash_attack']), self.delay['dash_attack'])
        # self.AMBIENT_WAVE_ATTACK = AmbientWaveAttack(self, len(self.frame['ambient_wave_attack']), self.delay['ambient_wave_attack'])
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE},
            }
        )


# Ultimate Armor X 캐릭터 클래스
class UltimateArmorXCharacter(Character):
    def __init__(self, x, y, speed, player):
        super().__init__('ultimate_armor_x.png', x, y, speed, ultimate_armor_x, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': ultimate_armor_x[0],
            'idle': ultimate_armor_x[1],
            'walk': ultimate_armor_x[2],
            'jump': ultimate_armor_x[3],
            'base_sword_attack': ultimate_armor_x[4],
            'base_buster_attack': ultimate_armor_x[5],  # 기본 공격(base_attack)으로 판단!
            'power_attack': ultimate_armor_x[6],
            'dash': ultimate_armor_x[7],
            'hit': ultimate_armor_x[8],
            'defeat': ultimate_armor_x[9],
        }

        self.delay = {
            'intro': 0.1,
            'idle': 0.1,
            'walk': 0.1,
            'jump': 0.1,
            'base_sword_attack': 0.1,   # 기본 공격(base_attack)으로 판단!
            'base_buster_attack': 0.1,
            'power_attack': 0.1,
            'dash': 0.1,
            'hit': 0.1,
            'defeat': 0.1,
        }

        self.INTRO = Intro(self, len(self.frame['intro']), self.delay['intro'])
        self.IDLE = Idle(self, len(self.frame['idle']), self.delay['idle'])
        self.WALK = Walk(self, len(self.frame['walk']), self.delay['walk'])
        # self.JUMP = Jump(self, len(self.frame['jump']), self.delay['jump'])
        # self.BASE_SWORD_ATTACK = BaseSwordAttack(self, len(self.frame['base_sword_attack']), self.delay['base_sword_attack'])
        # self.BASE_BUSTER_ATTACK = BaseBusterAttack(self, len(self.frame['base_buster_attack']), self.delay['base_buster_attack'])
        # self.POWER_ATTACK = PowerAttack(self, len(self.frame['power_attack']), self.delay['power_attack'])
        # self.DASH = Dash(self, len(self.frame['dash']), self.delay['dash'])
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE},
            }
        )