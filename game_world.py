world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)


def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


# game_world 에서만 제거하는 것이 아닌
# collision_pairs 에 들어있는 모든 객체(o)를 제거
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            # collision_pairs에서 해당 객체를 제거하는 작업도 필요하다.
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    global world

    for layer in world:
        layer.clear()

    # 충돌 박스도 제거
    collision_pairs.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    # 일단 사각형의 모든 방향을 비교해서 충돌이 아닌 경우를 먼저 걸러낸다.
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    # 충돌이 아닌 경우를 다 걸러냈으면 충돌한 것이다.
    return True


# 공격 판정용 충돌 함수
def collide_attack(attacker, defender):
    left_a, bottom_a, right_a, top_a = attacker.get_attack_bb()
    left_b, bottom_b, right_b, top_b = defender.get_bb()

    # 공격이 없는 프레임이면 패스!(사각형의 크기가 0!)
    if left_a == right_a and bottom_a == top_a:
        return False

    # 일단 사각형의 모든 방향을 비교해서 충돌이 아닌 경우를 먼저 걸러낸다.
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    # 충돌이 아닌 경우를 다 걸러냈으면 충돌한 것이다.
    return True

# 공격 판정용 충돌 함수
def collide_reflect(reflect, wave):
    # 반사체의 get_reflect_bb 함수가 없으면 충돌하지 않음!
    if not hasattr(reflect, 'get_reflect_bb'):
        return False

    left_a, bottom_a, right_a, top_a = reflect.get_reflect_bb()
    left_b, bottom_b, right_b, top_b = wave.get_bb()

    # 공격이 없는 프레임이면 패스!(사각형의 크기가 0!)
    if left_a == right_a and bottom_a == top_a:
        return False

    # 일단 사각형의 모든 방향을 비교해서 충돌이 아닌 경우를 먼저 걸러낸다.
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    # 충돌이 아닌 경우를 다 걸러냈으면 충돌한 것이다.
    return True


# collision_pairs 딕셔너리에는 충돌 검사가 필요한 객체 쌍에 대한 정보가 저장된다.
collision_pairs = {}

def add_collision_pair(group, a, b):
    # 맨 처음에는 그룹이 없다.
    if group not in collision_pairs:    # 처음 추가하는 그룹이면
        collision_pairs[group] = [[], [], []]   # 해당 그룹을 만든다.
    if a:   # a의 경우 1번째 리스트에 추가
        collision_pairs[group][0].append(a)
    if b:   # b의 경우 2번째 리스트에 추가
        collision_pairs[group][1].append(b)


def handle_collision():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:  # a 리스트의 모든 객체에 대해서
            for b in pairs[1]:  # b 리스트의 모든 객체에 대해서
                # 근접 공격 충돌!
                if group in ('p1_attack:p2_body', 'p2_attack:p1_body'):
                    if collide_attack(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

                # 일반 wave 충돌!
                elif group in ('p1_wave:p2_body', 'p2_wave:p1_body'):
                    if collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)

                # 반사 투사체 충돌!
                elif group in ('p1_reflect:p2_wave', 'p2_reflect:p1_wave'):
                    if collide_reflect(a, b):
                        # a = reflect 캐릭터, b = wave
                        b.reflect(a)

                # 지면과 캐릭터의 충돌!
                elif group == 'ground:p1_body' or group == 'ground:p2_body':
                    if collide(a, b):
                        a.handle_collision(group, b)
                        b.handle_collision(group, a)