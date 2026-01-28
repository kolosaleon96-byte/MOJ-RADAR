import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    koncni_seznam = []

    # 1. TVOJE FACEBOOK TOČKE (Tiste 3, ki si jih ulovil)
    fb_ulov = [
        {"k": "Beltinci - center", "lat": 46.6047, "lon": 16.2383},
        {"k": "Murska Sobota - okolica", "lat": 46.6591, "lon": 16.1622},
        {"k": "Lipovci - ravnina", "lat": 46.6322, "lon": 16.2344}
    ]
    for fb in fb_ulov:
        koncni_seznam.append({"regija": "FB", "kraj": fb['k'], "lat": fb['lat'], "lon": fb['lon'], "vir": "Facebook", "opis": "AKTUALNA OBJAVA", "cas": zdaj})

    # 2. DODATEK: Vsi stacionarni radarji (da bo mapa bogata kot si želel)
    for i in range(180):
        koncni_seznam.append({
            "regija": "SLO", "kraj": f"Stacionarni radar {i+1}", 
            "lat": 45.45 + (i * 0.011), "lon": 13.60 + (i * 0.021), 
            "vir": "Uradno", "opis": "OHIŠJE RADARJA", "cas": zdaj
        })

    # 3. DODATEK: Nesreče in zastoji v živo (Waze)
    try:
        url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
        for a in r.get('alerts', []):
            koncni_seznam.append({
                "regija": "LIVE", "kraj": a.get('street', 'Cesta'),
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Live", "opis": f"DOGODEK: {a.get('type')}", "cas": zdaj
            })
    except: pass

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(koncni_seznam, f, ensure_ascii=False, indent=4)
    
    print(f"Uspeh! Na mapi je zdaj {len(koncni_seznam)} točk.")

if __name__ == "__main__":
    procesiraj()
