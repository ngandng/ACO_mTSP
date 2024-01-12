
import numpy as np

class Ant:
    def __init__(self,tour,cost=np.inf) -> None:
        self.Tour = tour
        self.Cost = cost