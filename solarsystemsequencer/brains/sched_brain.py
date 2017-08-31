import math
import datetime
import json
from typing import List
import pandas as pd
import appglobals
from computetargets import ComputeTargets


def generate(targets: List[str], date: str, start_time: str, end_time: str, max_sun_ele: int, min_ele: int,
             max_ele: int, interval: int, preference: str, target_pref: str, no_target_action: str, end_action: str):
    time_range = list(pd.date_range(date + " " + start_time, date + " " + end_time,
                                    freq=str(interval) + "min").to_pydatetime())

    schedule = {}
    for r in reversed(time_range):
        compute = ComputeTargets(r, appglobals.location["Latitude"], appglobals.location["Longitude"])
        sun_alt = compute.object_alt("Sun")["alt"] * 180 / math.pi
        if sun_alt > max_sun_ele:
            time_range.remove(r)

    for r in time_range:
        compute = ComputeTargets(r, appglobals.location["Latitude"], appglobals.location["Longitude"])
        # Limit altitude of targets
        candidates = [t for t in targets if min_ele <= compute.object_alt(t)["alt"] * 180 / math.pi <= max_ele]

        # Stay on one side of meridian if set
        if preference == "East":
            candidates = [t for t in candidates if 0 <= compute.object_alt(t)["az"] * 180 / math.pi < 180]
        elif preference == "West":
            candidates = [t for t in candidates if 180 <= compute.object_alt(t)["az"] * 180 / math.pi < 360]
        schedule[r] = candidates

    final = {}
    prev = None
    # TODO: Meridian flips
    for l in schedule:
        compute = ComputeTargets(l, appglobals.location["Latitude"], appglobals.location["Longitude"])
        target = None
        if target_pref == "Less for longer":
            lowest = max_ele
            for t in schedule.get(l):
                if min_ele < compute.object_alt(t)["alt"] * 180 / math.pi < lowest:
                    pass
                    '''target = t
                    lowest = compute.object_alt(t)["alt"] * 180 / math.pi'''
        elif target_pref == "Prefer highest":
            highest = min_ele
            for t in schedule.get(l):
                if max_ele > compute.object_alt(t)["alt"] * 180 / math.pi > highest:
                    target = t
                    highest = compute.object_alt(t)["alt"] * 180 / math.pi
            else:
                if target is None and highest == min_ele:
                    target = no_target_action
        # Add to final if it wasn't previously added
        if target != prev:
            final[l] = target
            prev = target
    date_list = [int(i) for i in date.split("/")]
    time_list = [int(i) for i in end_time.split(":")]
    final[datetime.datetime(date_list[0], date_list[1], date_list[2], time_list[0], time_list[1])] = end_action
    appglobals.schedule[date] = [{"Target": final.get(t), "Time": str(t.time()), "Filter": "", "Exposure": "0",
                                  "Gain": "0", "Integration": "0"} for t in final]
    with open("schedule.json", "w") as f:
        json.dump(appglobals.schedule, f, indent=4)
