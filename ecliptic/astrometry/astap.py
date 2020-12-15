import subprocess
from solver import Solver


class AstapSolver(Solver):
    def __init__(self, path: str):
        self.path = path
    
    def solve(self, image, ra_h=None, dec_d=None, radius_d=None):
        command = [
            self.path, '-wcs', '-annotate',
            '-f', image.filename,
        ]

        if ra_h:
            command.extend(['-ra', str(ra_h)])
        if dec_d:
            command.extend(['-spd', str(dec_d + 90)])
        if radius_d:
            command.extend(['-r', str(radius_d)])
        
        subprocess.Popen(command)
