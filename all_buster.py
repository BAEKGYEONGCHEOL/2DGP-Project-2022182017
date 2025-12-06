from pico2d import *
import game_world
import game_framework
from spriteSheet import x5_x_ultimate_x_buster, x5sigma4_buster

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel


class NormalBuster:
    image = None

    def __init__(self, x, y, facing, thrower, speed = 15):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.thrower = thrower

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
        draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            if self in self.thrower.active_bullets:
                self.thrower.active_bullets.remove(self)
            self.thrower.buster_locked = False
            game_world.remove_object(self)

    def get_bb(self):
        # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
        if self.facing == 1:
            return self.x - 30, self.y - 30, self.x + 60, self.y + 30
        else:
            return self.x - 60, self.y - 30, self.x + 30, self.y + 30

    def get_attack_damage(self):
        return self.thrower.get_wave_damage(type(self))

    def handle_collision(self, group, other):
        if self in self.thrower.active_bullets:
            self.thrower.active_bullets.remove(self)

        self.thrower.buster_locked = False

        # 투사체는 충돌 시 사라지도록 삭제!
        game_world.remove_object(self)

    def reflect(self, other_thrower):
        self.facing *= -1

        game_world.remove_collision_object(self)

        if other_thrower.player == 1:
            game_world.add_collision_pair('p1_wave:p2_body', self, None)
            game_world.add_collision_pair('p2_reflect:p1_wave', None, self)
        else:
            game_world.add_collision_pair('p2_wave:p1_body', self, None)
            game_world.add_collision_pair('p1_reflect:p2_wave', None, self)

class PowerBuster:
    image = None

    def __init__(self, x, y, facing, thrower, speed = 30):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.thrower = thrower

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
        draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            if self in self.thrower.active_bullets:
                self.thrower.active_bullets.remove(self)
            self.thrower.buster_locked = False
            game_world.remove_object(self)

    def get_bb(self):
        # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
        if self.facing == 1:
            return self.x - 45, self.y - 40, self.x + 75, self.y + 40
        else:
            return self.x - 75, self.y - 40, self.x + 45, self.y + 40

    def get_attack_damage(self):
        return self.thrower.get_wave_damage(type(self))

    def handle_collision(self, group, other):
        if self in self.thrower.active_bullets:
            self.thrower.active_bullets.remove(self)

        self.thrower.buster_locked = False

        # 투사체는 충돌 시 사라지도록 삭제!
        game_world.remove_object(self)

    def reflect(self, other_thrower):
        self.facing *= -1

        game_world.remove_collision_object(self)

        if other_thrower.player == 1:
            game_world.add_collision_pair('p1_wave:p2_body', self, None)
            game_world.add_collision_pair('p2_reflect:p1_wave', None, self)
        else:
            game_world.add_collision_pair('p2_wave:p1_body', self, None)
            game_world.add_collision_pair('p1_reflect:p2_wave', None, self)

class Sphere:
    image = None

    def __init__(self, x, y, facing, thrower, speed = 15):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.thrower = thrower

        self.TIME_PER_ACTION = 0.25
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.frame = 0
        self.frames = x5sigma4_buster[0]
        self.image = load_image('x5sigma4_buster.png')

    def draw(self):
        x, y, w, h = self.frames[int(self.frame)]

        if self.facing == -1:
            flip = 'h'
        else:
            flip = ''

        self.image.clip_composite_draw(x, y, w, h, 0, flip, self.x, self.y, w * 3, h * 3)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            if self in self.thrower.active_bullets:
                self.thrower.active_bullets.remove(self)
            self.thrower.buster_locked = False
            game_world.remove_object(self)

    def get_bb(self):
        # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
        if self.facing == 1:
            return self.x - 35, self.y - 35, self.x + 35, self.y + 35
        else:
            return self.x - 35, self.y - 35, self.x + 35, self.y + 35

    def get_attack_damage(self):
        return self.thrower.get_wave_damage(type(self))

    def handle_collision(self, group, other):
        if self in self.thrower.active_bullets:
            self.thrower.active_bullets.remove(self)

        self.thrower.buster_locked = False

        # 투사체는 충돌 시 사라지도록 삭제!
        game_world.remove_object(self)

    def reflect(self, other_thrower):
        self.facing *= -1

        game_world.remove_collision_object(self)

        if other_thrower.player == 1:
            game_world.add_collision_pair('p1_wave:p2_body', self, None)
            game_world.add_collision_pair('p2_reflect:p1_wave', None, self)
        else:
            game_world.add_collision_pair('p2_wave:p1_body', self, None)
            game_world.add_collision_pair('p1_reflect:p2_wave', None, self)


class Wave:
    image = None

    def __init__(self, x, y, facing, thrower, speed = 20):
        self.x, self.y = x, y
        self.xv = speed

        self.facing = facing

        self.thrower = thrower

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        self.frame = 0
        self.frames = x5sigma4_buster[1]
        self.image = load_image('x5sigma4_buster.png')

    def draw(self):
        x, y, w, h = self.frames[int(self.frame)]

        if self.facing == -1:
            flip = ''
        else:
            flip = 'h'

        self.image.clip_composite_draw(x, y, w, h, 0, flip, self.x, self.y, w * 3, h * 3)
        # draw_rectangle(): 좌상단(x1, y1), 우하단(x2, y2) 2개의 점을 가지고 빨간색 사각형을 그려준다.
        # 튜플은 하나의 파라미터로 간주가 되기 때문에 *를 붙여서 튜플을 풀어준다. -> 4개의 인자로 변환
        draw_rectangle(*self.get_bb())

    def update(self):
        dt = game_framework.frame_time

        # 위치 업데이트
        self.x += self.facing * self.xv * game_framework.frame_time * PIXEL_PER_METER

        self.frame = (self.frame + len(self.frames) * self.ACTION_PER_TIME * dt) % len(self.frames)

        # 화면 밖으로 나가면 제거!
        if self.x > 1650 or self.x < 0:
            if self in self.thrower.active_bullets:
                self.thrower.active_bullets.remove(self)
            self.thrower.buster_locked = False
            game_world.remove_object(self)

    def get_bb(self):
        # ball의 바운더리 박스를 튜플 형태로 반환하여 사각형의 범위를 알려준다.
        if self.facing == 1:
            return self.x - 50, self.y - 160, self.x + 80, self.y + 160
        else:
            return self.x - 80, self.y - 160, self.x + 50, self.y + 160

    def get_attack_damage(self):
        return self.thrower.get_wave_damage(type(self))

    def handle_collision(self, group, other):
        if self in self.thrower.active_bullets:
            self.thrower.active_bullets.remove(self)

        self.thrower.buster_locked = False

        # 투사체는 충돌 시 사라지도록 삭제!
        game_world.remove_object(self)

    def reflect(self, other_thrower):
        self.facing *= -1

        game_world.remove_collision_object(self)

        if other_thrower.player == 1:
            game_world.add_collision_pair('p1_wave:p2_body', self, None)
            game_world.add_collision_pair('p2_reflect:p1_wave', None, self)
        else:
            game_world.add_collision_pair('p2_wave:p1_body', self, None)
            game_world.add_collision_pair('p1_reflect:p2_wave', None, self)