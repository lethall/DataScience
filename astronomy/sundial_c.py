from skyfield.api import load, N, W, wgs84, utc, Angle
from skyfield import almanac
from datetime import datetime, timedelta
from pytz import timezone

est = timezone("US/Eastern")
ts = load.timescale()
de421 = load("de421.bsp")
earth, sun, moon = de421["earth"], de421["sun"], de421["moon"]
# 40°37′55″ N  82°58′37″ W
caledonia_wsg = wgs84.latlon(40.63194 * N, 82.9769 * W)
caledonia = earth + caledonia_wsg

def print_observe(from_obj, obj, tt):
    pos = from_obj.at(tt).observe(obj)
    alt, az, d = pos.apparent().altaz()
    ra, dec, d = pos.radec()
    print(f"""{obj.target_name.split()[-1]}
    alt: {alt.degrees:.1f}\t az: {az.degrees:.1f}
    ra: {ra.hours:.1f}h\tdec: {dec.degrees:.1f}""")

#a = ts.from_datetime(datetime.strptime("2025-11-14 00:00 UTC", "%Y-%m-%d %H:%M %Z").replace(tzinfo=utc))
#b = ts.from_datetime(datetime.strptime("2025-11-28 00:00 UTC", "%Y-%m-%d %H:%M %Z").replace(tzinfo=utc))
t = datetime.now(tz=est)
a = ts.from_datetime(t + timedelta(-2))
b = ts.from_datetime(t + timedelta(7))
t, y = almanac.find_discrete(a, b, almanac.moon_phases(de421))

for tm, ty, ph in zip(t.astimezone(est),y,[almanac.MOON_PHASES[yi] for yi in y]):
    print(f"{tm.isoformat(' ', 'seconds')} {ph}")
# almanac.moon_phases([a,b])
print("Rise/Set/Daylight")
rt, y = almanac.find_risings(caledonia, sun, a, b)
st, y = almanac.find_settings(caledonia, sun, a, b)
offset = 0
for rtm, stm in zip(rt,st):
    if offset == 2:
        print("---")
    offset += 1
    dayhrs = (stm-rtm)*24
    daylight = f"{int(dayhrs)}:{int((dayhrs-int(dayhrs))*60):02d}"
    print(f"{rtm.astimezone(est).date()} {rtm.astimezone(est).time().isoformat('seconds')}/{stm.astimezone(est).time().isoformat('seconds')}/{daylight}")

t = ts.now()
#t = ts.from_datetime(datetime.strptime("2025-08-23 06:06 UTC", "%Y-%m-%d %H:%M %Z").replace(tzinfo=utc))
lst = caledonia_wsg.lst_hours_at(t)
print(f"{t.tt_strftime()}\nLST: {Angle(hours=lst)} ({lst:.2f}h)")
print_observe(caledonia, sun, t)
print_observe(caledonia, moon, t)
