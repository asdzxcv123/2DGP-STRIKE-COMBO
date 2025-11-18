
world=[[],[]]
collision_pairs = {}
def add_object(o, depth=0):
    world[depth].append(o)
    pass

def add_objects(ol, depth=0):
    world[depth] += ol

    pass

def update():
    for layer in world:
        for o in layer:
            o.update()
    pass

def render(camera):
    for layer in world:
        for o in layer:
            o.draw(camera)

    pass

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    pass

def clear():
    global world
    for layer in world:
        layer.clear()
    pass

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def get_group(group):
    """특정 그룹의 객체 리스트를 반환하는 헬퍼 함수"""
    if group in collision_pairs:
        # group이 'player:monster' 형태라면 a, b 리스트가 섞여있으므로 용도에 맞게 사용
        return collision_pairs[group]
    return [[], []]