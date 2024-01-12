
import numpy as np
# import math
from Distance import cal_3Ddistance as distance

def tour_cost(ant, model):
    n_agent = model.N

    L1 = 0
    L3_max = 0
    L3_min = np.inf

    n = 0       # the current agent
    icre = 0    # the current position in tour 
    len_atour = np.zeros(model.N)

    while n <= model.N and icre < len(ant.Tour):
        # print('icre = ', icre, ', n = ', n)
        if ant.Tour[icre] == -1:

            if icre != 0:
                len_atour[n-1] = len_atour[n-1] + distance(model.agents[n-1],model.tasks[ant.Tour[icre-1]-1])     
            n += 1
            
        else:   
            if ant.Tour[icre-1] == -1: 
                len_atour[n-1] = len_atour[n-1] + distance(model.agents[n-1],model.tasks[ant.Tour[icre]-1])

            else:   
                len_atour[n-1] = len_atour[n-1] + distance(model.tasks[ant.Tour[icre]-1], model.tasks[ant.Tour[icre-1]-1])

                if icre == len(ant.Tour)-1:
                    len_atour[n-1] = len_atour[n-1] + distance(model.agents[n-1], model.tasks[ant.Tour[icre]-1])
        icre += 1

    L1 = np.sum(len_atour)
    n_task_total = len(ant.Tour)-model.N

    L2 = model.M - n_task_total
    L3 = L3_max - L3_min

    # L = L1 + 120 * L2 + 2 * L3
    L = L1 + 120*L2

    return L