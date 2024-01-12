import random

class Task:

    def __init__(self,id,tc,WORLD) -> None:
        self.id = id
        self.tc = tc
        self.x = random.uniform(WORLD.XMIN,WORLD.XMAX)
        self.y = random.uniform(WORLD.YMIN,WORLD.YMAX)
        self.z = random.uniform(WORLD.ZMIN,WORLD.ZMAX)

