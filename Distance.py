
import numpy as np

def cal_3Ddistance(a,b):
    dis = np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2 + (a.z-b.z)**2)
    return dis