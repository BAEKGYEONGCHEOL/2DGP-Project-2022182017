from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_g, SDLK_v, SDLK_e, SDLK_r, SDLK_t, SDLK_c
from spriteSheet import mmx_x4_x_sheet, zerox4sheet, x5sigma4, Dynamox56sheet, ultimate_armor_x
import game_framework
import game_world
from all_buster import NormalBuster, PowerBuster, Sphere, Wave

from state_machine import StateMachine

def time_out(e):
    return e[0] == 'TIME_OUT'

def land_walk(e):
    return e[0] == 'LAND_WALK'

def land_idle(e):
    return e[0] == 'LAND_IDLE'

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

def g_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g

def v_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_v

def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r

def t_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_t

def t_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_t

def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c

def hit(e):
    return e[0] == 'HIT'

def defeat(e):
    return e[0] == 'DEFEAT'


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel == 30 cm

# 걷기 속도
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 점프 초기 속도
JUMP_SPEED_KMPH = 50.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

# 중력 가속도 (픽셀 단위, 아래 방향)
GRAVITY_PPS2 = 9.8 * 30

# 대쉬 속도
DASH_SPEED_KMPH = 50.0
DASH_SPEED_MPM = (DASH_SPEED_KMPH * 1000.0 / 60.0)
DASH_SPEED_MPS = (DASH_SPEED_MPM / 60.0)
DASH_SPEED_PPS = (DASH_SPEED_MPS * PIXEL_PER_METER)


# Intro 상태
class Intro:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 1.25
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.frame = 0
        self.character.current_frame = 0    # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['intro']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['intro']):
            self.character.state_machine.handle_state_event(('TIME_OUT', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['intro'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Idle 상태
class Idle:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        pass

    def do(self):
        self.frame = (self.frame + len(self.character.frame['idle']) * self.ACTION_PER_TIME * game_framework.frame_time) % len(self.character.frame['idle'])
        self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['idle'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Walk 상태(한 번 대기 후 걷기 반복)
class Walk:

    def __init__(self, character, speed, prepare_frame_count):
        self.character = character
        self.frame = 0
        self.speed = speed
        self.prepare_frame_count = prepare_frame_count
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.character.is_walking = True  # 걷는 중 표시

    def exit(self, e):
        self.character.is_walking = False  # 걷기 종료

    def do(self):
        dt = game_framework.frame_time

        self.frame += len(self.character.frame['walk']) * self.ACTION_PER_TIME * game_framework.frame_time

        # 준비 구간: 0 ~ prepare_frame_count-1
        if self.frame < self.prepare_frame_count:
            # 준비 중일 때는 그대로 진행 (한 번만)
            self.character.current_frame = int(self.frame)

        else:
            # 반복 구간 계산 (loop_frames이 0이 되지 않도록!)
            loop_start = self.prepare_frame_count
            total_frames = len(self.character.frame['walk'])
            loop_frames = max(1, total_frames - loop_start)

            # 반복 구간 계산
            loop_frame = int((self.frame - loop_start)) % loop_frames + loop_start
            self.character.current_frame = min(loop_frame, total_frames - 1)

        # facing 방향으로 이동!
        self.character.x += self.character.facing * self.speed * dt

        # 화면 밖으로 나가지 않도록 제한!
        if self.character.x < 50:
            self.character.x = 50
        elif self.character.x > 1544:
            self.character.x = 1544

    def draw(self):
        frame_data = self.character.frame['walk'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Jump 상태
class Jump:

    def __init__(self, character):
        self.character = character
        self.frame = 0

        self.vertical_speed = 0.0

        self.start_y = 0.0
        self.max_height = 0.0  # 점프 높이 추적

        # 커스텀 파라미터 (록맨 느낌용)
        self.JUMP_UP_SPEED = 800.0  # 빠른 상승 속도
        self.GRAVITY_UP = 800.0  # 상승 중 중력 (약함)
        self.GRAVITY_DOWN = 2400.0  # 하강 중 중력 (강함)

        self.start_y = 0.0
        self.jumping_up = True  # 상승 중인지 여부
        self.jump_height = 180.0  # 최고 높이
        self.total_height = 0.0

        # 애니메이션 타이밍
        self.TIME_PER_ACTION = 0.8  # 전체 점프 중 프레임 재생 시간
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.total_frames = 0.0  # 시간 기반으로 0~1 진행률 계산용

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.total_frames = 0.0
        self.start_y = self.character.y

        # 위로 튕겨 오름
        self.vertical_speed = self.JUMP_UP_SPEED

        self.jumping_up = True

        # 제자리 점프
        self.horizontal_speed = 0.0

        # 실제 최고 높이 계산 (포물선 공식: v^2 / 2g)
        self.jump_height = (self.JUMP_UP_SPEED ** 2) / (2 * self.GRAVITY_UP)

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time
        self.total_frames += self.ACTION_PER_TIME * dt  # 애니메이션 진행률 (0~1)
        self.frame += len(self.character.frame['jump']) * self.ACTION_PER_TIME * dt

        # 물리 처리
        if self.jumping_up:
            self.vertical_speed -= self.GRAVITY_UP * dt
            if self.vertical_speed <= 0:
                self.jumping_up = False
        else:
            self.vertical_speed -= self.GRAVITY_DOWN * dt

        self.character.y += self.vertical_speed * dt
        self.character.x += self.horizontal_speed * dt

        # 화면 밖으로 나가지 않도록 제한!
        if self.character.x < 50:
            self.character.x = 50
        elif self.character.x > 1544:
            self.character.x = 1544

        # 착지
        GROUND_Y = 225
        if self.character.y <= GROUND_Y:
            self.character.y = GROUND_Y

            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))

            return

        # --- 프레임 계산 (위치 기반 진행률) ---
        total_frames = len(self.character.frame['jump'])

        # 상승 -> 하강 전체 구간을 0~1로 나눔
        # 상승 중: (현재 y - 시작 y) / 점프 높이 * 0.5
        # 하강 중: 0.5 + (시작 높이 + jump_height - 현재 y) / jump_height * 0.5
        if self.jumping_up:
            progress = (self.character.y - self.start_y) / self.jump_height * 0.5
        else:
            fall_dist = max(0.0, (self.start_y + self.jump_height) - self.character.y)
            progress = 0.5 + (fall_dist / self.jump_height * 0.5)

        # 진행률을 0~1로 제한
        progress = max(0.0, min(1.0, progress))

        # progress 비율로 프레임 인덱스 계산
        frame_index = int(progress * (total_frames - 1))
        self.character.current_frame = frame_index

    def draw(self):
        frame_data = self.character.frame['jump'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# WalkJump 상태
class WalkJump:

    def __init__(self, character):
        self.character = character
        self.frame = 0

        self.vertical_speed = 0.0

        self.start_y = 0.0
        self.max_height = 0.0  # 점프 높이 추적

        # 커스텀 파라미터 (록맨 느낌용)
        self.JUMP_UP_SPEED = 800.0  # 빠른 상승 속도
        self.GRAVITY_UP = 800.0  # 상승 중 중력 (약함)
        self.GRAVITY_DOWN = 2400.0  # 하강 중 중력 (강함)

        self.start_y = 0.0
        self.jumping_up = True  # 상승 중인지 여부
        self.jump_height = 180.0  # 최고 높이
        self.total_height = 0.0

        # 애니메이션 타이밍
        self.TIME_PER_ACTION = 0.8  # 전체 점프 중 프레임 재생 시간
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.total_frames = 0.0  # 시간 기반으로 0~1 진행률 계산용

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.total_frames = 0.0
        self.start_y = self.character.y

        # 위로 튕겨 오름
        self.vertical_speed = self.JUMP_UP_SPEED

        self.jumping_up = True

        # 점프 직전 이동 속도 유지
        self.horizontal_speed = self.character.speed * self.character.facing

        # 실제 최고 높이 계산 (포물선 공식: v^2 / 2g)
        self.jump_height = (self.JUMP_UP_SPEED ** 2) / (2 * self.GRAVITY_UP)

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time
        self.total_frames += self.ACTION_PER_TIME * dt  # 애니메이션 진행률 (0~1)
        self.frame += len(self.character.frame['jump']) * self.ACTION_PER_TIME * dt

        # 물리 처리
        if self.jumping_up:
            self.vertical_speed -= self.GRAVITY_UP * dt
            if self.vertical_speed <= 0:
                self.jumping_up = False
        else:
            self.vertical_speed -= self.GRAVITY_DOWN * dt

        self.character.y += self.vertical_speed * dt
        self.character.x += self.horizontal_speed * dt

        # 화면 밖으로 나가지 않도록 제한!
        if self.character.x < 50:
            self.character.x = 50
        elif self.character.x > 1544:
            self.character.x = 1544

        # 착지
        GROUND_Y = 225
        if self.character.y <= GROUND_Y:
            self.character.y = GROUND_Y

            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))

            return

        # --- 프레임 계산 (위치 기반 진행률) ---
        total_frames = len(self.character.frame['jump'])

        # 상승 -> 하강 전체 구간을 0~1로 나눔
        # 상승 중: (현재 y - 시작 y) / 점프 높이 * 0.5
        # 하강 중: 0.5 + (시작 높이 + jump_height - 현재 y) / jump_height * 0.5
        if self.jumping_up:
            progress = (self.character.y - self.start_y) / self.jump_height * 0.5
        else:
            fall_dist = max(0.0, (self.start_y + self.jump_height) - self.character.y)
            progress = 0.5 + (fall_dist / self.jump_height * 0.5)

        # 진행률을 0~1로 제한
        progress = max(0.0, min(1.0, progress))

        # progress 비율로 프레임 인덱스 계산
        frame_index = int(progress * (total_frames - 1))
        self.character.current_frame = frame_index

    def draw(self):
        frame_data = self.character.frame['jump'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Teleport 상태
class Teleport:

    def __init__(self, character):
        self.character = character
        self.frame = 0

        self.TIME_PER_ACTION = 0.8
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.teleport_distance = 400    # 순간이동 거리
        self.teleport_done = False      # 실제 순간이동 발생 여부 변수!
        self.is_visible = True          # 사라짐 여부!

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0
        self.teleport_done = False
        self.is_visible = True

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False
        self.is_visible = True

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time
        total_frames = len(self.character.frame['teleport'])

        # 프레임 계산!
        self.frame += total_frames * self.ACTION_PER_TIME * dt
        if self.frame >= total_frames:
            # 종료 시점 -> Idle/Walk 복귀
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))

            return

        # 현재 진행률 (0.0 ~ 1.0)
        progress = self.frame / total_frames

        # 순간이동 처리
        if not self.teleport_done and progress >= 0.5:
            self.teleport_done = True
            self.is_visible = False  # 사라짐

            # 방향에 따라 이동
            if self.character.facing == 1:
                self.character.x += self.teleport_distance
            else:
                self.character.x -= self.teleport_distance

            # 화면 밖으로 나가지 않도록 제한!
            if self.character.x < 50:
                self.character.x = 50
            elif self.character.x > 1544:
                self.character.x = 1544

        # 사라짐/등장 구간 제어!
        if progress < 0.5:
            self.is_visible = True  # 사라지는 중이지만 보이게!
        elif progress < 0.75:
            self.is_visible = False  # 완전히 사라진 구간!
        else:
            self.is_visible = True  # 다시 등장 구간!

        # 프레임 인덱스 갱신
        self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['teleport'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Arm Attack 상태
class ArmAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.4
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = True
        self.attack_name = 'arm_attack'

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['arm_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['arm_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['arm_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Dash Attack 상태
class DashAttack:

    def __init__(self, character, speed):
        self.character = character
        self.frame = 0
        self.speed = speed
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = True
        self.attack_name = 'dash_attack'

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time

        self.character.x += self.character.facing * self.speed * dt  # 약간 앞으로 이동

        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['dash_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        # 화면 밖 제한
        if self.character.x < 50:
            self.character.x = 50
        elif self.character.x > 1544:
            self.character.x = 1544

        if self.frame >= len(self.character.frame['dash_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['dash_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Dash Attack Wall상태
class DashAttackWall:

    def __init__(self, character, speed, prepare_frame_count):
        self.character = character
        self.frame = 0
        self.speed = speed
        self.prepare_frame_count = prepare_frame_count
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = True
        self.attack_name = 'dash_attack_wall'

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time

        self.character.x += self.character.facing * self.speed * dt  # 약간 앞으로 이동

        self.frame += len(self.character.frame['dash_attack_wall']) * self.ACTION_PER_TIME * dt

        # 준비 구간: 0 ~ prepare_frame_count-1
        if self.frame < self.prepare_frame_count:
            # 준비 중일 때는 그대로 진행 (한 번만)
            self.character.current_frame = int(self.frame)

        else:
            # 반복 구간 계산 (loop_frames이 0이 되지 않도록!)
            loop_start = self.prepare_frame_count
            total_frames = len(self.character.frame['dash_attack_wall'])
            loop_frames = max(1, total_frames - loop_start)

            # 반복 구간 계산
            loop_frame = int((self.frame - loop_start)) % loop_frames + loop_start
            self.character.current_frame = min(loop_frame, total_frames - 1)

        # 화면 밖으로 나가지 않도록 제한!
        if self.character.x < 50:
            self.character.x = 50
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        elif self.character.x > 1544:
            self.character.x = 1544
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))

    def draw(self):
        frame_data = self.character.frame['dash_attack_wall'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Power Attack 상태
class PowerAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.fired = False

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.fired = False

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['power_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        current = int(self.frame)
        self.character.current_frame = current
        if current == 4 and not self.fired:
            self.character.fire_power_buster()
            self.fired = True

        if self.frame >= len(self.character.frame['power_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['power_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Sphere Attack 상태
class SphereAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.fired = False

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.fired = False

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['sphere_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        current = int(self.frame)
        self.character.current_frame = current
        if current == 1 and not self.fired:
            self.character.fire_sphere()
            self.fired = True

        if self.frame >= len(self.character.frame['sphere_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['sphere_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Wave Attack 상태
class WaveAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.fired = False

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.fired = False

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['wave_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        current = int(self.frame)
        self.character.current_frame = current
        if current == 2 and not self.fired:
            self.character.fire_wave()
            self.fired = True

        if self.frame >= len(self.character.frame['wave_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['wave_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Reflex Attack 상태
class ReflexAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.2
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time

        self.frame += len(self.character.frame['reflex_attack']) * self.ACTION_PER_TIME * game_framework.frame_time

        if self.frame >= len(self.character.frame['reflex_attack']):
            if self.character.is_t_pressed:
                self.frame = 0
                self.character.current_frame = 0
            else:
                # 평소처럼 Idle/Walk 복귀
                if self.character.is_left_pressed or self.character.is_right_pressed:
                    self.character.state_machine.handle_state_event(('LAND_WALK', None))
                else:
                    self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['reflex_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Ambient Wave Attack 상태
class AmbientWaveAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 1.15
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = True
        self.attack_name = 'ambient_wave_attack'

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['ambient_wave_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['ambient_wave_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['ambient_wave_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Base Sword Attack 상태
class BaseSwordAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.7
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = True
        self.attack_name = 'base_sword_attack'

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['base_sword_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['base_sword_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['base_sword_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Base Buster Attack 상태
class BaseBusterAttack:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.fired = False  # Buster 발사 여부 변수

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!
        self.fired = False  # Buster 발사 여부 변수

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['base_buster_attack']) * self.ACTION_PER_TIME * game_framework.frame_time)

        current = int(self.frame)
        self.character.current_frame = current
        if current == 4 and not self.fired:
            self.character.fire_normal_buster()
            self.fired = True

        if self.frame >= len(self.character.frame['base_buster_attack']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['base_buster_attack'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Dash 상태
class Dash:

    def __init__(self, character, speed):
        self.character = character
        self.frame = 0
        self.speed = speed
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        dt = game_framework.frame_time

        self.character.x += self.character.facing * self.speed * dt  # 약간 앞으로 이동

        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(
            self.character.frame['dash']) * self.ACTION_PER_TIME * game_framework.frame_time)

        # 화면 밖 제한
        if self.character.x < 50:
            self.character.x = 50
        elif self.character.x > 1544:
            self.character.x = 1544

        if self.frame >= len(self.character.frame['dash']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['dash'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Hit 상태
class Hit:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['hit']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['hit']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['hit'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# Defeat 상태
class Defeat:

    def __init__(self, character):
        self.character = character
        self.frame = 0
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.is_attack = False
        self.attack_name = None

    def enter(self, e):
        self.character.action_doing = True
        self.character.facing_lock = True
        self.frame = 0
        self.character.current_frame = 0  # current_frame 초기화!

    def exit(self, e):
        self.character.action_doing = False
        self.character.facing_lock = False

        if not self.character.is_left_pressed and self.character.is_right_pressed:
            self.character.facing = 1
        elif not self.character.is_right_pressed and self.character.is_left_pressed:
            self.character.facing = -1

    def do(self):
        # 한 번만 실행하기 위해 % 연산 제거
        self.frame = (self.frame + len(self.character.frame['defeat']) * self.ACTION_PER_TIME * game_framework.frame_time)

        if self.frame >= len(self.character.frame['defeat']):
            if self.character.is_left_pressed or self.character.is_right_pressed:
                self.character.state_machine.handle_state_event(('LAND_WALK', None))
            else:
                self.character.state_machine.handle_state_event(('LAND_IDLE', None))
        else:
            self.character.current_frame = int(self.frame)

    def draw(self):
        frame_data = self.character.frame['defeat'][self.character.current_frame]
        self.character.draw_frame(frame_data)


# ===================================================================
# 캐릭터 베이스 클래스 구현!
# ===================================================================

# 기본 베이스 캐릭터 클래스 구현
class Character:
    def __init__(self, image_path, x, y, speed, dash_speed, sheet_data, player, change_facing_right):
        self.image = load_image(image_path)    # 캐릭터 이미지 로드
        self.hp = 100   # 기본 체력 설정
        self.x = x
        self.y = y
        self.player = player
        self.change_facing_right = change_facing_right  # 캐릭터의 기본 방향은 우측 방향!

        if self.player == 1:
            self.facing = 1
        else:
            self.facing = -1

        self.current_frame = 0  # 현재 프레임 인덱스
        self.speed = speed
        self.dash_speed = dash_speed

        # 자식 클래스 생성 시 프레임 데이터를 딕셔너리 형태로 저장
        self.frame = {}

        self.state_machine = None

        self.is_walking = False  # 기본은 걷지 않음!
        self.is_t_pressed = False  # 기본은 T키 누르지 않음!

        # 좌/우 방향키 입력 상태
        self.is_left_pressed = False
        self.is_right_pressed = False

        self.action_doing = False
        self.facing_lock = False

    def update(self):
        if self.state_machine:
            self.state_machine.update()

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()

    def handle_event(self, event):
        if self.state_machine:
            self.state_machine.handle_state_event(('INPUT', event))

        # 좌/우 방향키 상태 업데이트
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.is_left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.is_right_pressed = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.is_left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.is_right_pressed = False

        # t 키 상태 업데이트
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_t:
                self.is_t_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_t:
                self.is_t_pressed = False

        # 키가 떼인 후에도 반대 방향키가 눌려 있으면 즉시 방향 갱신!
        if self.facing_lock == False:
            if not self.is_left_pressed and self.is_right_pressed:
                self.facing = 1
            elif not self.is_right_pressed and self.is_left_pressed:
                self.facing = -1

        if self.action_doing == True:
            return


    # 프레임 그리기 함수
    def draw_frame(self, frame_data):
        x_data, y_data, w_data, h_data = frame_data

        if self.player == 1:
            base_facing = 1
        else:
            base_facing = -1

        # 현재 바라보는 방향과 기본 방향이 다르면 뒤집기!
        facing_flip = (self.facing != base_facing)

        # 현재 바라보는 방향(facing)
        # 시트 방향과 바라보는 방향에 따라 flip 계산
        if self.change_facing_right:
            # 시트가 오른쪽을 보고 있다면, 오른쪽일 때 그대로, 왼쪽일 때 뒤집기
            if self.facing == 1:
                flip = 'h'
            else:
                flip = ''

        else:
            # 시트가 왼쪽을 보고 있다면, 왼쪽일 때 그대로, 오른쪽일 때 뒤집기
            if self.facing == -1:
                flip = 'h'
            else:
                flip = ''

        # 해당 프레임 그리기!
        self.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, flip, self.x, self.y, w_data * 3, h_data * 3)


# ===================================================================
# 각자 개인 캐릭터 클래스 구현!
# ===================================================================

# X 캐릭터 클래스
class XCharacter(Character):
    X_speed = 1.5

    def __init__(self, x, y, player):
        # 실제 이동 속도
        real_speed = RUN_SPEED_PPS * self.X_speed
        real_dash_speed = DASH_SPEED_PPS * self.X_speed

        super().__init__('mmx_x4_x_sheet.png', x, y, real_speed, real_dash_speed, mmx_x4_x_sheet, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': mmx_x4_x_sheet[0],
            'idle': mmx_x4_x_sheet[1],
            'walk': mmx_x4_x_sheet[2],
            'jump': mmx_x4_x_sheet[3],
            'base_buster_attack': mmx_x4_x_sheet[4],
            'power_attack': mmx_x4_x_sheet[5],
            'dash': mmx_x4_x_sheet[6],
            'hit': mmx_x4_x_sheet[7],
            'defeat': mmx_x4_x_sheet[8],
        }

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self, self.speed, 0)
        self.JUMP = Jump(self)
        self.WALK_JUMP = WalkJump(self)
        self.BASE_BUSTER_ATTACK = BaseBusterAttack(self)
        self.POWER_ATTACK = PowerAttack(self)
        self.DASH = Dash(self, self.dash_speed)
        self.HIT = Hit(self)
        self.DEFEAT = Defeat(self)

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                # INTRO 상태에서 해당 INTRO 프레임이 끝나는 이벤트(time_out)가 발생하면 IDLE 상태가 됨
                self.INTRO: {time_out: self.IDLE},
                # IDLE 상태(RUN 상태에서 양쪽 방향키를 동시에 눌렀을 때)에서 한 쪽 방향키를 떼었을 때 반대 방향으로 달리게 하기 위해서 right_down, right_up, left_down, left_up 이벤트도 추가, a키를 누르면 AUTO_RUN 상태로 변환!
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK, a_down: self.BASE_BUSTER_ATTACK, s_down: self.JUMP, d_down: self.POWER_ATTACK, g_down: self.DASH, hit: self.HIT, defeat: self.DEFEAT},
                # 여기서 right_down 과 left_down 은 RUN 상태에서 반대 방향키를 눌렀을 때 IDLE 상태로 가게 되는 경우이다.
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.BASE_BUSTER_ATTACK, s_down: self.WALK_JUMP, d_down: self.POWER_ATTACK, g_down: self.DASH, hit: self.HIT, defeat: self.DEFEAT},
                self.JUMP: {land_idle: self.IDLE, land_walk: self.WALK, hit: self.HIT, defeat: self.DEFEAT},
                self.WALK_JUMP: {land_idle: self.IDLE, land_walk: self.WALK, hit: self.HIT, defeat: self.DEFEAT},
                self.BASE_BUSTER_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK, hit: self.HIT, defeat: self.DEFEAT},
                self.POWER_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK, hit: self.HIT, defeat: self.DEFEAT},
                self.DASH: {land_idle: self.IDLE, land_walk: self.WALK, hit: self.HIT, defeat: self.DEFEAT},
                self.HIT: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DEFEAT: {},
            }
        )

        # 공격 데미지
        self.attack_damage_table = {
            'base_buster_attack': 4,
            'power_attack': 8,
        }

    # normal buster 발사 함수
    def fire_normal_buster(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = NormalBuster(self.x + 50 * facing, self.y + 25, facing, 15)

        game_world.add_object(buster, 2)

    # power buster 발사 함수
    def fire_power_buster(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = PowerBuster(self.x + 50 * facing, self.y + 20, facing, 25)

        game_world.add_object(buster, 2)

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state

        if self.facing == 1:
            if state == self.DASH:
                return self.x - 60, self.y - 70, self.x + 70, self.y + 70
            else:
                return self.x - 50, self.y - 70, self.x + 50, self.y + 70
        else:
            if state == self.DASH:
                return self.x - 70, self.y - 70, self.x + 60, self.y + 70
            else:
                return self.x - 50, self.y - 70, self.x + 50, self.y + 70

    def get_attack_bb(self):
        # X는 근접 공격이 없으므로 공격 박스는 없음!
        return 0, 0, 0, 0

    def handle_collision(self, group, other):
        # 1P가 2P를 때리는 경우
        if group == 'p1_attack:p2_body' and self.player == 2:
            self.take_damage(other.get_attack_damage())

        # 2P가 1P를 때리는 경우
        if group == 'p2_attack:p1_body' and self.player == 1:
            self.take_damage(other.get_attack_damage())

    def take_damage(self, damage):
        # 이미 죽었으면 무시!
        if self.hp <= 0:
            return

        # 체력 감소!
        self.hp -= damage

        # 체력 0 이하로 떨어지면 죽음 상태로 전환
        if self.hp <= 0:
            self.hp = 0

            self.state_machine.handle_state_event(('DEFEAT', None))
            return

        # 아직 살아있으면 히트 상태로 전환
        else:
            self.state_machine.handle_state_event(('HIT', None))
            return

    def get_attack_damage(self):
        return self.attack_damage_table.get(self.state_machine.cur_state, 0)



# Zero 캐릭터 클래스
class ZeroCharacter(Character):
    Zero_speed = 2.2

    def __init__(self, x, y, player):
        # 실제 이동 속도
        real_speed = RUN_SPEED_PPS * self.Zero_speed
        real_dash_speed = DASH_SPEED_PPS * self.Zero_speed

        super().__init__('zerox4sheet.png', x, y, real_speed, real_dash_speed, zerox4sheet, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': zerox4sheet[0],
            'idle': zerox4sheet[1],
            'walk': zerox4sheet[2],
            'jump': zerox4sheet[3],
            'base_sword_attack': zerox4sheet[4],
            'dash_attack': zerox4sheet[5],
            'dash': zerox4sheet[6],
            'hit': zerox4sheet[7],
            'defeat': zerox4sheet[8],
        }

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self, self.speed, 0)
        self.JUMP = Jump(self)
        self.WALK_JUMP = WalkJump(self)
        self.BASE_SWORD_ATTACK = BaseSwordAttack(self)
        self.DASH_ATTACK = DashAttack(self, self.dash_speed)
        self.DASH = Dash(self, self.dash_speed)
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK, a_down: self.BASE_SWORD_ATTACK, s_down: self.JUMP, g_down: self.DASH, v_down: self.DASH_ATTACK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.BASE_SWORD_ATTACK, s_down: self.WALK_JUMP, g_down: self.DASH, v_down: self.DASH_ATTACK},
                self.JUMP: {land_idle: self.IDLE, land_walk: self.WALK},
                self.WALK_JUMP: {land_idle: self.IDLE, land_walk: self.WALK},
                self.BASE_SWORD_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DASH_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DASH: {land_idle: self.IDLE, land_walk: self.WALK},
            }
        )

        # 공격 데미지
        self.attack_damage_table = {
            'base_sword_attack': 5,
            'dash_attack': 8,
        }

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state

        if self.facing == 1:
            if state == self.DASH:
                return self.x - 60, self.y - 70, self.x + 70, self.y + 70
            elif state == self.BASE_SWORD_ATTACK:
                return self.x - 70, self.y - 85, self.x + 80, self.y + 85
            elif state == self.DASH_ATTACK:
                return self.x - 75, self.y - 70, self.x + 60, self.y + 70
            else:
                return self.x - 55, self.y - 70, self.x + 55, self.y + 70
        else:
            if state == self.DASH:
                return self.x - 70, self.y - 70, self.x + 60, self.y + 70
            elif state == self.BASE_SWORD_ATTACK:
                return self.x - 70, self.y - 85, self.x + 80, self.y + 85
            elif state == self.DASH_ATTACK:
                return self.x - 60, self.y - 70, self.x + 75, self.y + 70
            else:
                return self.x - 55, self.y - 70, self.x + 55, self.y + 70

    def get_attack_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state
        # 현재 프레임 불러오기
        frame = self.current_frame

        if state == self.BASE_SWORD_ATTACK:
            if frame >= 3 and frame <= 6:
                if self.facing == 1:
                    return self.x - 40, self.y - 70, self.x + 150, self.y + 100
                else:
                    return self.x - 150, self.y - 70, self.x + 40, self.y + 100
            else:
                return 0, 0, 0, 0
        elif state == self.DASH_ATTACK:
            if frame >= 3 and frame <= 4:
                if self.facing == 1:
                    return self.x - 40, self.y - 70, self.x + 150, self.y + 80
                else:
                    return self.x - 150, self.y - 70, self.x + 40, self.y + 80
            else:
                return 0, 0, 0, 0
        else:
            return 0, 0, 0, 0

    def handle_collision(self, group, other):
        # 1P가 2P를 때리는 경우
        if group == 'p1_attack:p2_body' and self.player == 2:
            self.take_damage(other.get_attack_damage())

        # 2P가 1P를 때리는 경우
        if group == 'p2_attack:p1_body' and self.player == 1:
            self.take_damage(other.get_attack_damage())

    def take_damage(self, damage):
        # 이미 죽었으면 무시!
        if self.hp <= 0:
            return

        # 체력 감소!
        self.hp -= damage

        # 체력 0 이하로 떨어지면 죽음 상태로 전환
        if self.hp <= 0:
            self.hp = 0

            self.state_machine.handle_state_event(('DEFEAT', None))
            return

        # 아직 살아있으면 히트 상태로 전환
        else:
            self.state_machine.handle_state_event(('HIT', None))
            return

    def get_attack_damage(self):
        return self.attack_damage_table.get(self.state_machine.cur_state, 0)


# Sigma 캐릭터 클래스
class SigmaCharacter(Character):
    Sigma_speed = 1.5

    def __init__(self, x, y, player):
        # 실제 속도
        real_speed = RUN_SPEED_PPS * self.Sigma_speed
        real_dash_speed = DASH_SPEED_PPS * self.Sigma_speed

        super().__init__('x5sigma4.png', x, y, real_speed, real_dash_speed, x5sigma4, player, True)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': x5sigma4[0],
            'idle': x5sigma4[1],
            'walk': x5sigma4[2],
            'teleport': x5sigma4[3],
            'arm_attack': x5sigma4[4],
            'sphere_attack': x5sigma4[5],
            'wave_attack': x5sigma4[6],
            'dash_attack_wall': x5sigma4[7],
            'hit': x5sigma4[8],
            'defeat': x5sigma4[9],
        }

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self, self.speed, 3)
        self.TELEPORT = Teleport(self)
        self.ARM_ATTACK = ArmAttack(self)
        self.SPHERE_ATTACK = SphereAttack(self)
        self.WAVE_ATTACK = WaveAttack(self)
        self.DASH_ATTACK_WALL = DashAttackWall(self, self.dash_speed, 3)
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK, a_down: self.ARM_ATTACK, s_down: self.TELEPORT, v_down: self.DASH_ATTACK_WALL, e_down: self.SPHERE_ATTACK, r_down: self.WAVE_ATTACK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.ARM_ATTACK, s_down: self.TELEPORT, v_down: self.DASH_ATTACK_WALL, e_down: self.SPHERE_ATTACK, r_down: self.WAVE_ATTACK},
                self.TELEPORT: {land_idle: self.IDLE, land_walk: self.WALK},
                self.ARM_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.SPHERE_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.WAVE_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DASH_ATTACK_WALL: {land_idle: self.IDLE, land_walk: self.WALK},
            }
        )

        # 공격 데미지
        self.attack_damage_table = {
            'arm_attack': 8,
            'sphere_attack': 8,
            'wave_attack': 10,
            'dash_attack_wall': 12,
        }

    # sphere 발사 함수
    def fire_sphere(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = Sphere(self.x + 50 * facing, self.y + 25, facing, 15)

        game_world.add_object(buster, 2)

    # wave 발사 함수
    def fire_wave(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = Wave(self.x + 50 * facing, self.y + 50, facing, 25)

        game_world.add_object(buster, 2)

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state

        if self.facing == 1:
            if state == self.WALK or state == self.DASH_ATTACK_WALL:
                return self.x - 100, self.y - 75, self.x + 115, self.y + 85
            elif state == self.ARM_ATTACK or state == self.WAVE_ATTACK:
                return self.x - 65, self.y - 120, self.x + 75, self.y + 120
            else:
                return self.x - 65, self.y - 120, self.x + 60, self.y + 120
        else:
            if state == self.WALK or state == self.DASH_ATTACK_WALL:
                return self.x - 115, self.y - 75, self.x + 100, self.y + 85
            elif state == self.ARM_ATTACK or state == self.WAVE_ATTACK:
                return self.x - 75, self.y - 120, self.x + 65, self.y + 120
            else:
                return self.x - 60, self.y - 120, self.x + 65, self.y + 120

    def get_attack_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state
        # 현재 프레임 불러오기
        frame = self.current_frame

        if state == self.ARM_ATTACK:
            if frame >= 1 and frame <= 2:
                if self.facing == 1:
                    return self.x - 40, self.y - 120, self.x + 140, self.y + 145
                else:
                    return self.x - 140, self.y - 120, self.x + 40, self.y + 145
            else:
                return 0, 0, 0, 0
        elif state == self.DASH_ATTACK_WALL:
            if frame == 3:
                if self.facing == 1:
                    return self.x - 100, self.y - 75, self.x + 115, self.y + 85
                else:
                    return self.x - 115, self.y - 75, self.x + 100, self.y + 85
            else:
                return 0, 0, 0, 0
        else:
            return 0, 0, 0, 0


# Vile 캐릭터 클래스
class VileCharacter(Character):
    Vile_speed = 1.85

    def __init__(self, x, y, player):
        # 실제 속도
        real_speed = RUN_SPEED_PPS * self.Vile_speed
        real_dash_speed = DASH_SPEED_PPS * self.Vile_speed

        super().__init__('Dynamox56sheet.png', x, y, real_speed, real_dash_speed, Dynamox56sheet, player, True)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': Dynamox56sheet[0],
            'idle': Dynamox56sheet[1],
            'walk': Dynamox56sheet[2],
            'teleport': Dynamox56sheet[3],
            'base_sword_attack': Dynamox56sheet[4],
            'reflex_attack': Dynamox56sheet[5],
            'dash_attack': Dynamox56sheet[6],
            'ambient_wave_attack': Dynamox56sheet[7],
            'hit': Dynamox56sheet[8],
            'defeat': Dynamox56sheet[9],
        }

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self, self.speed, 1)
        self.TELEPORT = Teleport(self)
        self.BASE_SWORD_ATTACK = BaseSwordAttack(self)
        self.REFLEX_ATTACK = ReflexAttack(self)
        self.DASH_ATTACK = DashAttack(self, self.dash_speed)
        self.AMBIENT_WAVE_ATTACK = AmbientWaveAttack(self)
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK, a_down: self.BASE_SWORD_ATTACK, s_down: self.TELEPORT, v_down: self.DASH_ATTACK, t_down: self.REFLEX_ATTACK, c_down: self.AMBIENT_WAVE_ATTACK},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.BASE_SWORD_ATTACK, s_down: self.TELEPORT, v_down: self.DASH_ATTACK, t_down: self.REFLEX_ATTACK, c_down: self.AMBIENT_WAVE_ATTACK},
                self.TELEPORT: {land_idle: self.IDLE, land_walk: self.WALK},
                self.BASE_SWORD_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.REFLEX_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DASH_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.AMBIENT_WAVE_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
            }
        )

        # 공격 데미지
        self.attack_damage_table = {
            'base_sword_attack': 6,
            'dash_attack': 8,
            'ambient_wave_attack': 10,
        }

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state

        if self.facing == 1:
            if state == self.WALK:
                return self.x - 90, self.y - 75, self.x + 95, self.y + 80
            elif state == self.BASE_SWORD_ATTACK:
                return self.x - 70, self.y - 100, self.x + 75, self.y + 100
            elif state == self.DASH_ATTACK:
                return self.x - 80, self.y - 100, self.x + 85, self.y + 100
            else:
                return self.x - 60, self.y - 100, self.x + 60, self.y + 100
        else:
            if state == self.WALK:
                return self.x - 95, self.y - 75, self.x + 90, self.y + 80
            elif state == self.BASE_SWORD_ATTACK:
                return self.x - 85, self.y - 100, self.x + 80, self.y + 100
            elif state == self.DASH_ATTACK:
                return self.x - 70, self.y - 100, self.x + 75, self.y + 100
            else:
                return self.x - 60, self.y - 100, self.x + 60, self.y + 100

    def get_attack_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state
        # 현재 프레임 불러오기
        frame = self.current_frame

        if state == self.BASE_SWORD_ATTACK:
            if frame >= 7 and frame <= 9:
                if self.facing == 1:
                    return self.x - 150, self.y - 100, self.x + 140, self.y + 120
                else:
                    return self.x - 140, self.y - 100, self.x + 150, self.y + 120
            else:
                return 0, 0, 0, 0
        elif state == self.REFLEX_ATTACK:
            if self.facing == 1:
                return self.x - 0, self.y - 110, self.x + 110, self.y + 120
            else:
                return self.x - 110, self.y - 110, self.x + 0, self.y + 120
        elif state == self.DASH_ATTACK:
            if frame == 8:
                if self.facing == 1:
                    return self.x - 250, self.y - 160, self.x + 250, self.y + 160
                else:
                    return self.x - 250, self.y - 160, self.x + 250, self.y + 160
            else:
                return 0, 0, 0, 0
        elif state == self.AMBIENT_WAVE_ATTACK:
            if frame >= 19 and frame <= 22:
                if self.facing == 1:
                    return 0, self.y - 100, 1593, self.y + 25
                else:
                    return 0, self.y - 100, 1593, self.y + 25
            else:
                return 0, 0, 0, 0
        else:
            return 0, 0, 0, 0

    # 프레임 그리기 함수(오버라이드!)
    def draw_frame(self, frame_data):
        x_data, y_data, w_data, h_data = frame_data

        # 현재 바라보는 방향(facing)
        # 시트 방향과 바라보는 방향에 따라 flip 계산
        if self.change_facing_right:
            # 시트가 오른쪽을 보고 있다면, 오른쪽일 때 그대로, 왼쪽일 때 뒤집기
            if self.facing == 1:
                flip = 'h'
            else:
                flip = ''

        else:
            # 시트가 왼쪽을 보고 있다면, 왼쪽일 때 그대로, 오른쪽일 때 뒤집기
            if self.facing == -1:
                flip = 'h'
            else:
                flip = ''

        # Sword 공격 시 flip 반전!
        if self.state_machine.cur_state == self.REFLEX_ATTACK or self.state_machine.cur_state == self.AMBIENT_WAVE_ATTACK:
            if flip == 'h':
                flip = ''
            else:
                flip = 'h'

        # 해당 프레임 그리기!
        self.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, flip, self.x, self.y, w_data * 3, h_data * 3)


# Ultimate Armor X 캐릭터 클래스
class UltimateArmorXCharacter(Character):
    UAX_speed = 2.2

    def __init__(self, x, y, player):
        # 실제 속도
        real_speed = RUN_SPEED_PPS * self.UAX_speed
        real_dash_speed = DASH_SPEED_PPS * self.UAX_speed

        super().__init__('ultimate_armor_x.png', x, y, real_speed, real_dash_speed, ultimate_armor_x, player, False)

        # 캐릭터 별 프레임 및 딜레이 데이터 설정
        self.frame = {
            'intro': ultimate_armor_x[0],
            'idle': ultimate_armor_x[1],
            'walk': ultimate_armor_x[2],
            'jump': ultimate_armor_x[3],
            'base_buster_attack': ultimate_armor_x[4],
            'base_sword_attack': ultimate_armor_x[5],
            'power_attack': ultimate_armor_x[6],
            'dash_attack_wall': ultimate_armor_x[7],
            'hit': ultimate_armor_x[8],
            'defeat': ultimate_armor_x[9],
        }

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self, self.speed, 0)
        self.JUMP = Jump(self)
        self.WALK_JUMP = WalkJump(self)
        self.BASE_SWORD_ATTACK = BaseSwordAttack(self)
        self.BASE_BUSTER_ATTACK = BaseBusterAttack(self)
        self.POWER_ATTACK = PowerAttack(self)
        self.DASH_ATTACK_WALL = DashAttackWall(self, self.dash_speed, 7)
        # self.HIT = Hit(self, len(self.frame['hit']), self.delay['hit'])
        # self.DEFEAT = Defeat(self, len(self.frame['defeat']), self.delay['defeat'])

        self.state_machine = StateMachine(
            self.IDLE,  # 시작 상태는 IDLE 상태
            {
                self.INTRO: {time_out: self.IDLE},
                self.IDLE: {right_down: self.WALK, right_up: self.WALK, left_down: self.WALK, left_up: self.WALK, a_down: self.BASE_SWORD_ATTACK, s_down: self.JUMP, d_down: self.BASE_BUSTER_ATTACK, f_down: self.POWER_ATTACK, v_down: self.DASH_ATTACK_WALL},
                self.WALK: {right_down: self.IDLE, right_up: self.IDLE, left_down: self.IDLE, left_up: self.IDLE, a_down: self.BASE_SWORD_ATTACK, s_down: self.WALK_JUMP, d_down: self.BASE_BUSTER_ATTACK, f_down: self.POWER_ATTACK, v_down: self.DASH_ATTACK_WALL},
                self.JUMP: {land_idle: self.IDLE, land_walk: self.WALK},
                self.WALK_JUMP: {land_idle: self.IDLE, land_walk: self.WALK},
                self.BASE_SWORD_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.BASE_BUSTER_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.POWER_ATTACK: {land_idle: self.IDLE, land_walk: self.WALK},
                self.DASH_ATTACK_WALL: {land_idle: self.IDLE, land_walk: self.WALK},
            }
        )

        # 공격 데미지
        self.attack_damage_table = {
            'base_buster_attack': 6,
            'base_sword_attack': 8,
            'power_attack': 8,
            'dash_attack_wall': 10,
        }

    # normal buster 발사 함수
    def fire_normal_buster(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = NormalBuster(self.x + 50 * facing, self.y + 25, facing, 25)

        game_world.add_object(buster, 2)

    # power buster 발사 함수
    def fire_power_buster(self):
        # 플레이어의 바라보는 방향에 따라 위치와 발사 방향 계산
        facing = self.facing

        buster = PowerBuster(self.x + 50 * facing, self.y + 25, facing, 40)

        game_world.add_object(buster, 2)

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
            draw_rectangle(*self.get_bb())
            draw_rectangle(*self.get_attack_bb())

    def get_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state

        if self.facing == 1:
            if state == self.BASE_SWORD_ATTACK:
                return self.x - 70, self.y - 85, self.x + 80, self.y + 85
            elif state == self.DASH_ATTACK_WALL:
                return self.x - 60, self.y - 85, self.x + 100, self.y + 85
            else:
                return self.x - 50, self.y - 70, self.x + 50, self.y + 70
        else:
            if state == self.BASE_SWORD_ATTACK:
                return self.x - 80, self.y - 85, self.x + 70, self.y + 85
            elif state == self.DASH_ATTACK_WALL:
                return self.x - 100, self.y - 85, self.x + 60, self.y + 85
            else:
                return self.x - 50, self.y - 70, self.x + 50, self.y + 70

    def get_attack_bb(self):
        # 현재 상태 불러오기
        state = self.state_machine.cur_state
        # 현재 프레임 불러오기
        frame = self.current_frame

        if state == self.BASE_SWORD_ATTACK:
            if frame >= 4 and frame <= 7:
                if self.facing == 1:
                    return self.x - 40, self.y - 70, self.x + 150, self.y + 100
                else:
                    return self.x - 150, self.y - 70, self.x + 40, self.y + 100
            else:
                return 0, 0, 0, 0
        elif state == self.DASH_ATTACK_WALL:
            if frame >= 7 and frame <= 8:
                if self.facing == 1:
                    return self.x - 110, self.y - 100, self.x + 170, self.y + 100
                else:
                    return self.x - 170, self.y - 100, self.x + 110, self.y + 100
            else:
                return 0, 0, 0, 0
        else:
            return 0, 0, 0, 0

    # 프레임 그리기 함수(오버라이드!)
    def draw_frame(self, frame_data):
        x_data, y_data, w_data, h_data = frame_data

        # 현재 바라보는 방향(facing)
        # 시트 방향과 바라보는 방향에 따라 flip 계산
        if self.change_facing_right:
            # 시트가 오른쪽을 보고 있다면, 오른쪽일 때 그대로, 왼쪽일 때 뒤집기
            if self.facing == 1:
                flip = 'h'
            else:
                flip = ''

        else:
            # 시트가 왼쪽을 보고 있다면, 왼쪽일 때 그대로, 오른쪽일 때 뒤집기
            if self.facing == -1:
                flip = 'h'
            else:
                flip = ''

        # Sword 공격 시 flip 반전!
        if self.state_machine.cur_state == self.BASE_SWORD_ATTACK:
            if flip == 'h':
                flip = ''
            else:
                flip = 'h'

        # 해당 프레임 그리기!
        self.image.clip_composite_draw(x_data, y_data, w_data, h_data, 0, flip, self.x, self.y, w_data * 3, h_data * 3)