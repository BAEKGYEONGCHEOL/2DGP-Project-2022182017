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


class Intro:
    pass


class Idle:
    pass


class Walk:
    pass


class Character:
    def __init__(self, image_path, x, y, speed):
        self.image = load_image(image_path)    # 캐릭터 이미지 로드
        self.x = 400
        self.y = 300
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.speed = speed

        self.INTRO = Intro(self)
        self.IDLE = Idle(self)
        self.WALK = Walk(self)

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