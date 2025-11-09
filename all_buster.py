from pico2d import *
import game_world
import game_framework
from spriteSheet import x5_x_ultimate_x_buster, x5sigma4_buster

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel


class NormalBuster:
    image = None

    def __init__(self, x, y, facing, speed = 15):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.frame = 0
        self.frames = x5_x_ultimate_x_buster[0]
        self.image = load_image('x5_x_ultimate_x_buster.png')

    def draw(self):
        x, y, w, h = self.frames[int(self.frame)]

        if self.facing == -1:
            flip = 'h'
        else:
            flip = ''

        self.image.clip_composite_draw(x, y, w, h, 0, flip, self.x, self.y, w * 3, h * 3)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        # draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            game_world.remove_object(self)

    # def get_bb(self):
    #     # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
    #     return self.x - 10, self.y - 10, self.x + 10, self.y + 10
    #
    # def handle_collision(self, group, other):
    #     # group이 소년과 볼 사이의 충돌이라면
    #     if group == 'boy:ball':
    #         # 아래처럼 작성하면 지울 수 없는 에러가 발생!
    #         # game_worl d에서는 ball 이 사라졌지만 collision_pairs 에는 여전히 남아 있기 때문이다.
    #         # collision_pairs 에서는 계속해서 비교를 시도하게 되고, 이미 지워진 ball 객체에 접근하려고 하면서 에러가 발생한다.
    #         # 해결 방법은 collision_pairs 에서도 해당 객체를 제거해 주어야 한다.
    #         # 이 작업은 game_world.py 의 game_world.remove_object() 함수에서 처리해 준다.
    #         game_world.remove_object(self)
    #     # group이 잔디와 볼 사이의 충돌이라면
    #     elif group == 'grass:ball' and self.stop_state == False:
    #         # 볼이 잔디 위에서 멈춘다.
    #         self.stopped = True
    #         self.stop_state = True
    #     elif group == 'zombie:ball' and self.stop_state == False:
    #         # 볼이 좀비와 충돌하면 제거한다.
    #         game_world.remove_object(self)


class PowerBuster:
    image = None

    def __init__(self, x, y, facing, speed = 30):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.frame = 0
        self.frames = x5_x_ultimate_x_buster[1]
        self.image = load_image('x5_x_ultimate_x_buster.png')

    def draw(self):
        x, y, w, h = self.frames[int(self.frame)]

        if self.facing == -1:
            flip = 'h'
        else:
            flip = ''

        self.image.clip_composite_draw(x, y, w, h, 0, flip, self.x, self.y, w * 3, h * 3)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        # draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            game_world.remove_object(self)

    # def get_bb(self):
    #     # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
    #     return self.x - 10, self.y - 10, self.x + 10, self.y + 10
    #
    # def handle_collision(self, group, other):
    #     # group이 소년과 볼 사이의 충돌이라면
    #     if group == 'boy:ball':
    #         # 아래처럼 작성하면 지울 수 없는 에러가 발생!
    #         # game_worl d에서는 ball 이 사라졌지만 collision_pairs 에는 여전히 남아 있기 때문이다.
    #         # collision_pairs 에서는 계속해서 비교를 시도하게 되고, 이미 지워진 ball 객체에 접근하려고 하면서 에러가 발생한다.
    #         # 해결 방법은 collision_pairs 에서도 해당 객체를 제거해 주어야 한다.
    #         # 이 작업은 game_world.py 의 game_world.remove_object() 함수에서 처리해 준다.
    #         game_world.remove_object(self)
    #     # group이 잔디와 볼 사이의 충돌이라면
    #     elif group == 'grass:ball' and self.stop_state == False:
    #         # 볼이 잔디 위에서 멈춘다.
    #         self.stopped = True
    #         self.stop_state = True
    #     elif group == 'zombie:ball' and self.stop_state == False:
    #         # 볼이 좀비와 충돌하면 제거한다.
    #         game_world.remove_object(self)