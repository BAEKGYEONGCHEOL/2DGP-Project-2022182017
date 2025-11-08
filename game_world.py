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


