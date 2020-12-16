import subprocess
from pathlib import Path
from solver import Solver


class AstapSolver(Solver):
    def __init__(self, path: str):
        self.program = Path(path)
    
    def solve(self, image, ra_h=None, dec_d=None, radius_d=None, down_sample=None, debug=False):
        path = Path(image)
        command = [
            str(self.program), '-wcs',
            '-f', str(path),
        ]

        if ra_h is not None:
            command.extend(['-ra', str(ra_h)])
        if dec_d is not None:
            command.extend(['-spd', str(dec_d + 90)])
        if radius_d is not None:
            command.extend(['-r', str(radius_d)])
        if down_sample is not None:
            command.extend(['-z', str(down_sample)])
        if debug == True:
            command.append('-debug')
        
        subprocess.run(command)
