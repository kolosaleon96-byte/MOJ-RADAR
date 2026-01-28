import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    vsi = []

    # 1. LIVE PODATKI (Radarji in nesreče v živo)
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        r = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        for a in r.get('alerts', []):
            tip = a.get('type')
            if tip == "POLICE": d = "👮 RADAR V ŽIVO"
            elif tip == "ACCIDENT": d = "💥 NESREČA"
            else: d = "⚠️ DOGODEK"
            
            vsi.append({
                "regija": "LIVE", "kraj": a.get('street', 'Cesta'),
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Waze", "opis": d, "omejitev": "!", "cas": zdaj
            })
    except: pass

    # 2. FIKSNI RADARJI (Tvoj konec - Prekmurje)
    fiksni = [
        {"k": "M. Sobota - Lendavska", "lat": 46.6591, "lon": 16.1622},
        {"k": "Lipovci - Stacionarni", "lat": 46.6322, "lon": 16.2344},
        {"k": "Gederovci - Križišče", "lat": 46.6655, "lon": 16.0488}
    ]
    for f in fiksni:
        vsi.append({"regija": "MS", "kraj": f['k'], "lat": f['lat'], "lon": f['lon'], "vir": "Fiksni", "opis": "STACIONARNI RADAR", "omejitev": "50", "cas": zdaj})

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    print(f"Mapa osvežena z {len(vsi)} točkami.")

if __name__ == "__main__":
    procesiraj()
