import subprocess
from io import BytesIO
from pathlib import Path
import tempfile
import numpy as np
from astropy.wcs import WCS
from .solver import Solver


class AstapSolver(Solver):
    def __init__(self, path: str):
        self.program = Path(path)
    
    def solve(self, image, ra_h=None, dec_d=None, radius_d=None, fov_d=None, down_sample=None, debug=False):
        tmp = tempfile.TemporaryDirectory()

        output = BytesIO()
        output.write(
            b'RAW1' + image.size[0].to_bytes(4, 'little') + image.size[1].to_bytes(4, 'little') + np.asarray(image).tobytes()
        )

        name = Path(f'{tmp.name}/stdin').as_posix()

        command = [
            self.program.name, '-f', 'stdin', '-o', name
        ]

        if ra_h is not None:
            command.extend(['-ra', str(ra_h)])
        if dec_d is not None:
            command.extend(['-spd', str(dec_d + 90)])
        if radius_d is not None:
            command.extend(['-r', str(radius_d)])
        if fov_d is not None:
            command.extend(['-fov', str(fov_d)])
        if down_sample is not None:
            command.extend(['-z', str(down_sample)])
        if debug == True:
            command.append('-debug')
        
        proc = subprocess.Popen(command, executable=self.program, stdin=subprocess.PIPE, bufsize=0)
        proc.communicate(input=output.getvalue())

        with open(f'{name}.wcs', 'r') as result:
            d = {}
            for l in result:
                if l.rstrip() and 'PLTSOLVD' not in l and 'COMMENT' not in l:
                    k, v = l.split('=')
                    v = v.split('/')[0]
                    try:
                        d[k.rstrip(' ')] = float(v)
                    except ValueError:
                        d[k.rstrip(' ')] = v.replace('\'', ' ').strip()

        w = WCS(naxis=2)
        w.wcs.crpix = [d['CRPIX1'], d['CRPIX2']]
        w.wcs.crval = [d['CRVAL1'], d['CRVAL2']]
        w.wcs.cdelt = [d['CDELT1'], d['CDELT2']]
        w.wcs.crota = [d['CROTA1'], d['CROTA2']]
        w.wcs.cd = [[d['CD1_1'], d['CD1_2']], [d['CD2_1'], d['CD2_2']]]
        
        sky = w.pixel_to_world(image.size[0] // 2, image.size[1] // 2)
        
        output.close()
        tmp.cleanup()
