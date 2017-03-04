import ephem
import time


class ComputeTargets:
    def __init__(self, time, latitude, longitude):
        self.observer = ephem.Observer()
        self.observer.date = time
        self.observer.lat = latitude
        self.observer.lon = longitude

        self.sun = ephem.Sun()
        self.mercury = ephem.Mercury()
        self.venus = ephem.Venus()
        self.mars = ephem.Mars()
        self.jupiter = ephem.Jupiter()
        self.saturn = ephem.Saturn()
        self.uranus = ephem.Uranus()
        self.neptune = ephem.Neptune()

    def compute_targets(self, obj):
        if obj == 'Sun':
            self.sun.compute(self.observer)
        elif obj == 'Mercury':
            self.mercury.compute(self.observer)
        elif obj == 'Venus':
            self.venus.compute(self.observer)
        elif obj == 'Mars':
            self.mars.compute(self.observer)
        elif obj == 'Jupiter':
            self.jupiter.compute(self.observer)
        elif obj == 'Saturn':
            self.saturn.compute(self.observer)
        elif obj == 'Uranus':
            self.uranus.compute(self.observer)
        elif obj == 'Neptune':
            self.neptune.compute(self.observer)

    def object_alt(self, obj):
        self.compute_targets(obj)
        if obj == 'Mercury':
            rascension = self.mercury.ra
            declination = self.mercury.dec
            azimuth = self.mercury.az
            altitude = self.mercury.alt
        elif obj == 'Venus':
            rascension = self.venus.ra
            declination = self.venus.dec
            azimuth = self.venus.az
            altitude = self.venus.alt
        elif obj == 'Mars':
            rascension = self.mars.ra
            declination = self.mars.dec
            azimuth = self.mars.az
            altitude = self.mars.alt
        elif obj == 'Jupiter':
            rascension = self.jupiter.ra
            declination = self.jupiter.dec
            azimuth = self.jupiter.az
            altitude = self.jupiter.alt
        elif obj == 'Saturn':
            rascension = self.saturn.ra
            declination = self.saturn.dec
            azimuth = self.saturn.az
            altitude = self.saturn.alt
        elif obj == 'Uranus':
            rascension = self.uranus.ra
            declination = self.uranus.dec
            azimuth = self.uranus.az
            altitude = self.uranus.alt
        elif obj == 'Neptune':
            rascension = self.neptune.ra
            declination = self.neptune.dec
            azimuth = self.neptune.az
            altitude = self.neptune.alt
        else:
            rascension = 0
            declination = 0
            azimuth = 0
            altitude = 0
        return {'ra': rascension, 'dec': declination, 'az': azimuth, 'alt': altitude, 'date': self.observer.date}

    def twilight(self):
        sun_error = None
        civil_error = None
        nautical_error = None
        astronomical_error = None
        try:
            sun_rise = self.observer.previous_rising(self.sun).tuple()
            sun_set = self.observer.next_setting(self.sun).tuple()
        except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
            sun_rise = None
            sun_set = None
            sun_error = e

        self.observer.horizon = '-6'
        try:
            civtwi_rise = self.observer.previous_rising(self.sun).tuple()
            civtwi_set = self.observer.next_setting(self.sun).tuple()
        except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
            civtwi_rise = None
            civtwi_set = None
            civil_error = e

        self.observer.horizon = '-12'
        try:
            nauttwi_rise = self.observer.previous_rising(self.sun).tuple()
            nauttwi_set = self.observer.next_setting(self.sun).tuple()
        except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
            nauttwi_rise = None
            nauttwi_set = None
            nautical_error = e

        self.observer.horizon = '-18'
        try:
            astrotwi_rise = self.observer.previous_rising(self.sun).tuple()
            astrotwi_set = self.observer.next_setting(self.sun).tuple()
        except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
            astrotwi_rise = None
            astrotwi_set = None
            astronomical_error = e

        self.observer.horizon = '0'
        return sun_rise, civtwi_rise, nauttwi_rise, astrotwi_rise, sun_set, civtwi_set, nauttwi_set, astrotwi_set, \
               sun_error, civil_error, nautical_error, astronomical_error
