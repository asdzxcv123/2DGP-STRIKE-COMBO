world=[[]]

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

def render():
    for layer in world:
        for o in layer:
            o.draw()

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
