399# horizons_full.py
# One-file Horizons tool - no external core needed
# Saves: body, body_id, center, date, days, AU, Mkm, miles, km/s, mph

from astroquery.jplhorizons import Horizons
from astropy.time import Time
from astropy import units as u
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- lookups ---
bodies = {
    "mercury":"199","venus":"299","earth":"399","mars":"499",
    "jupiter":"5","saturn":"6","uranus":"7","neptune":"8","pluto":"9",
    "moon":"301","luna":"301",
    "voyager 1":"-31","voyager1":"-31","voyager 2":"-32","voyager2":"-32",
    "199":"199","299":"299","399":"399","499":"499","5":"5","6":"6","7":"7","8":"8","9":"9","301":"301","-31":"-31","-32":"-32"
}
names = {"199":"Mercury","299":"Venus","399":"Earth","499":"Mars","5":"Jupiter","6":"Saturn","7":"Uranus","8":"Neptune","9":"Pluto","301":"Moon","-31":"Voyager 1","-32":"Voyager 2"}
centers = {"1":"399","2":"@sun","3":"301","4":"499","5":"5","6":"6","7":"7","8":"8","9":"9","10":"@0"}
center_names = {"399":"Earth","@sun":"Sun","301":"Moon","499":"Mars","5":"Jupiter","6":"Saturn","7":"Uranus","8":"Neptune","9":"Pluto","@0":"SSB"}

def exact_extreme(dates_iso, values, mode="min"):
    idx = values.index(min(values) if mode=="min" else max(values))
    if idx==0 or idx==len(values)-1:
        return datetime.fromisoformat(dates_iso[idx]), values[idx]
    x = np.array([-1,0,1]); y = np.array(values[idx-1:idx+2])
    a,b,c = np.polyfit(x,y,2); x_ext = -b/(2*a)
    base = datetime.fromisoformat(dates_iso[idx])
    return base + timedelta(days=float(x_ext)), a*x_ext**2 + b*x_ext + c

# --- input ---
print("Bodies: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Voyager 1, Voyager 2")
body_in = input("Body: ").strip()
body_id = bodies.get(body_in.lower(), body_in)
body_name = names.get(body_id, f"Body {body_id}")

date_str = input("Start UTC (YYYY-MM-DD) [now]: ").strip()
t0 = Time.now() if not date_str else Time(date_str)

print("\nCenters: (1)Earth (2)Sun (3)Moon (4)Mars (5)Jupiter (6)Saturn (7)Uranus (8)Neptune (9)Pluto (10)SSB")
c_choice = input("Center [1]: ").strip() or "1"
center_id = centers.get(c_choice, "399")
center_name = center_names.get(center_id, center_id)

days = int(input("Days [30]: ") or "30")

# --- constants ---
AU_KM = 149597870.7
SEC_DAY = 86400
KM_MI = 0.621371
KMS_MPH = 2236.93629

records = []; dates_iso = []; dists = []; speeds = []

print(f"\nQuerying {body_name} from {center_name}...")
for i in range(days):
    t = t0 + i * u.day # no warnings
    try:
        v = Horizons(id=body_id, location=center_id, epochs=t.jd).vectors()
        x,y,z = v['x'][0], v['y'][0], v['z'][0]
        vx,vy,vz = v['vx'][0], v['vy'][0], v['vz'][0]

        dau = (x**2+y**2+z**2)**0.5
        dmkm = dau * AU_KM / 1e6
        dmi = dmkm * 1e6 * KM_MI
        vaud = (vx**2+vy**2+vz**2)**0.5
        vkms = vaud * AU_KM / SEC_DAY
        vmph = vkms * KMS_MPH

        dates_iso.append(t.isot); dists.append(dmkm); speeds.append(vkms)
        records.append({
            "body": body_name,
            "body_id": body_id,
            "center": center_name,
            "center_id": center_id,
            "date_utc": t.iso,
            "days_since_start": i,
            "distance_au": round(dau, 6),
            "distance_mkm": round(dmkm, 6),
            "distance_miles": round(dmi, 0),
            "speed_kms": round(vkms, 6),
            "speed_mph": round(vmph, 2)
        })
    except Exception as e:
        pass

# exact
t_close, d_close = exact_extreme(dates_iso, dists, "min")
t_far, d_far = exact_extreme(dates_iso, dists, "max")
print(f"\nClosest: {t_close:%Y-%m-%d %H:%M} — {d_close:.4f} Mkm")
print(f"Farthest: {t_far:%Y-%m-%d %H:%M} — {d_far:.4f} Mkm")

# save
df = pd.DataFrame(records)
csv = f"horizons_{body_name.lower().replace(' ','_')}_{center_id.replace('@','')}_{days}d_FULL.csv"
df.to_csv(csv, index=False)
print(f"✓ Saved {csv} ({len(df.columns)} columns)")

# plots
xdates = [datetime.fromisoformat(d) for d in dates_iso]
plt.figure(figsize=(12,6)); plt.plot(xdates, speeds, lw=2)
plt.axvline(t_close, c='red', ls='--', label=f"Closest {t_close:%m-%d %H:%M}")
plt.axvline(t_far, c='orange', ls='--', label=f"Farthest {t_far:%m-%d %H:%M}")
plt.legend(); plt.title(f"{body_name} Speed from {center_name}")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(csv.replace('.csv','_speed.png'), dpi=150); plt.show()

plt.figure(figsize=(12,6)); plt.plot(xdates, dists, c='tab:orange', lw=2)
plt.axvline(t_close, c='red', ls='--'); plt.axvline(t_far, c='orange', ls='--')
plt.title(f"{body_name} Distance from {center_name}")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(csv.replace('.csv','_dist.png'), dpi=150); plt.show()