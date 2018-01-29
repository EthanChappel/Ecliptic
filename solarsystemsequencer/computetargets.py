from typing import List
from datetime import datetime
import ephem
import appglobals


def _get_observer(time: datetime, latitude: List[int] = appglobals.location["Latitude"],
                  longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Observer:
    observer = ephem.Observer()
    observer.date = time
    observer.lat = str(latitude[0]) + ":" + str(latitude[1]) + ":" + str(latitude[2])
    observer.lon = str(longitude[0]) + ":" + str(longitude[1]) + ":" + str(longitude[2])
    
    return observer


def _get_target(obj: str, time: datetime, latitude: List[int] = appglobals.location["Latitude"],
                longitude: List[int] = appglobals.location["Longitude"]):
    observer = _get_observer(time, latitude, longitude)
    if obj == "Sun":
        sun = ephem.Sun()
        sun.compute(observer)
        return sun
    elif obj == "Mercury":
        mercury = ephem.Mercury()
        mercury.compute(observer)
        return mercury
    elif obj == "Venus":
        venus = ephem.Venus()
        venus.compute(observer)
        return venus
    elif obj == "Mars":
        mars = ephem.Mars()
        mars.compute(observer)
        return mars
    elif obj == "Jupiter":
        jupiter = ephem.Jupiter()
        jupiter.compute(observer)
        return jupiter
    elif obj == "Saturn":
        saturn = ephem.Saturn()
        saturn.compute(observer)
        return saturn
    elif obj == "Uranus":
        uranus = ephem.Uranus()
        uranus.compute(observer)
        return uranus
    elif obj == "Neptune":
        neptune = ephem.Neptune()
        neptune.compute(observer)
        return neptune
    else:
        return None


def get_ra(obj: str, time: datetime, latitude: List[int] = appglobals.location["Latitude"],
           longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Angle:
    return _get_target(obj, time, latitude, longitude).ra


def get_dec(obj: str, time: datetime, latitude: List[int] = appglobals.location["Latitude"],
            longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Angle:
    return _get_target(obj, time, latitude, longitude).dec


def get_alt(obj: str, time: datetime, latitude: List[int] = appglobals.location["Latitude"],
            longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Angle:
    return _get_target(obj, time, latitude, longitude).alt


def get_az(obj: str, time: datetime, latitude: List[int] = appglobals.location["Latitude"],
           longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Angle:
    return _get_target(obj, time, latitude, longitude).az


def previous_rise(obj: str, time: datetime, horizon: int = 0, latitude: List[int] = appglobals.location["Latitude"],
                  longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Date:
    observer = _get_observer(time, latitude, longitude)
    target = _get_target(obj, time, latitude, longitude)

    observer.horizon = str(horizon)
    try:
        object_rise = observer.previous_rising(target)
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        object_rise = e

    return object_rise


def next_set(obj: str, time: datetime, horizon: int = 0, latitude: List[int] = appglobals.location["Latitude"],
             longitude: List[int] = appglobals.location["Longitude"]) -> ephem.Date:
    observer = _get_observer(time, latitude, longitude)
    target = _get_target(obj, time, latitude, longitude)

    observer.horizon = str(horizon)
    try:
        object_set = observer.next_setting(target)
    except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
        object_set = e

    return object_set
