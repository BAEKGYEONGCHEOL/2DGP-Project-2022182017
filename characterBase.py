from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP

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

    def __init__(self, character, max_frame):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = 0.1   # 프레임 상태마다 다르게 구현
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

    def __init__(self, character, max_frame):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = 0.1  # 프레임 상태마다 다르게 구현
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

    def __init__(self, character, max_frame):
        self.character = character
        self.frame = 0
        self.max_frame = max_frame
        self.delay = 0.1  # 프레임 상태마다 다르게 구현
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


class Character:
    def __init__(self, image_path, x, y, speed, sheet_data, player, change_facing_right):
        self.image = load_image(image_path)    # 캐릭터 이미지 로드
        self.x = x
        self.y = y
        self.frame = {
            'intro': sheet_data[0],
            'idle': sheet_data[1],
            'walk': sheet_data[2],
        }
        self.current_frame = 0  # 현재 프레임 인덱스
        self.face_dir = 1
        self.dir = 0
        self.speed = speed

        self.player = player
        self.change_facing_right = change_facing_right  # 캐릭터의 기본 방향은 우측 방향!

        self.INTRO = Intro(self, len(sheet_data[0]))
        self.IDLE = Idle(self, len(sheet_data[1]))
        self.WALK = Walk(self, len(sheet_data[2]))

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

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))