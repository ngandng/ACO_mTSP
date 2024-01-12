import numpy as np
from CreateAgent import Agent
from CreateTask import Task
import random

class WORLD:
    def __init__(self,clr,xmin,xmax,ymin,ymax,zmin,zmax,max_dis) -> None:
        self.XMAX = xmax
        self.XMIN = xmin
        self.YMAX = ymax
        self.YMIN = ymin
        self.ZMAX = zmax
        self.ZMIN = zmin
        self.MAX_DISTANCE = max_dis
        self.CLR = clr

class Model:
    def __init__(self,N,M) -> None:
        WORLD_CLR = np.random.rand(100, 3)

        WORLD_XMIN, WORLD_XMAX = 0, 250
        WORLD_YMIN, WORLD_YMAX = 0, 250
        WORLD_ZMIN, WORLD_ZMAX = 220, 250
        WORLD_MAX_DISTANCE = np.sqrt((WORLD_XMAX - WORLD_XMIN)**2 + 
                                    (WORLD_YMAX - WORLD_YMIN)**2 + 
                                    (WORLD_ZMAX - WORLD_ZMIN)**2)
        
        myWorld = WORLD(WORLD_CLR,WORLD_XMIN,WORLD_XMAX,WORLD_YMIN,WORLD_YMAX,WORLD_ZMIN,WORLD_ZMAX,WORLD_MAX_DISTANCE)

        centerx = (WORLD_XMAX - WORLD_XMIN) / 2
        centery = (WORLD_YMAX - WORLD_YMIN) / 2
        centerz = (WORLD_ZMAX - WORLD_ZMIN) / 2

        default_nom_vel = 2  # agent cruise velocity (m/s)

        # Create random agents and define parameters for each agent
        agents = []
        for n in range(1, N + 1):
            agents.append(Agent(n, random.uniform(myWorld.XMIN,myWorld.XMAX), random.uniform(myWorld.XMIN,myWorld.XMAX), random.uniform(10,20), default_nom_vel))

        # Create random tasks
        tasks = []
        for m in range(1, M + 1):
            tasks.append(Task(m, 0, myWorld))

        # Calculate distance matrix
        D = np.zeros((M, M))  # distance between two vertices

        for i in range(M - 1):
            for j in range(i + 1, M):
                delta_x = tasks[i].x - tasks[j].x
                delta_y = tasks[i].y - tasks[j].y
                delta_z = tasks[i].z - tasks[j].z

                D[i, j] = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
                D[j, i] = D[i, j]

        self.WORLD = myWorld    # working environment
        self.tasks = tasks      # set of task
        self.agents = agents    # set of agent
        self.N = N              # number of agent
        self.M = M              # number of task
        self.D = D              # heuristic matrix
