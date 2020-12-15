from abc import ABC, abstractmethod

class Solver(ABC):
    @abstractmethod
    def solve(self, image, ra_h=None, dec_d=None, radius_d=None): pass
