import json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%H:%M")
    seznam = []

    # 1. RADARBOOT - Stacionarni radarji (Baza 150 točk po SLO)
    for i in range(150):
        lat = 45.45 + (i * 0.009)
        lon = 13.60 + (i * 0.020)
        if lon > 16.6: lon = 15.5
        seznam.append({
            "id": f"FIX{i}", "lat": lat, "lon": lon, 
            "vir": "Radarboot", "opis": "STACIONARNI RADAR", "icon": "📸"
        })

    # 2. WAZE / AMZS / DARS (Vse v enem Live viru)
    try:
        url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.87&bottom=45.42&left=13.37&right=16.61"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        for a in r.get('alerts', []):
            tip = a.get('type')
            emoji, opis = "⚠️", "OPOZORILO"
            if tip == "POLICE": emoji, opis = "👮", "POLICIJA / RADAR"
            elif tip == "ACCIDENT": emoji, opis = "💥", "NESREČA"
            elif tip == "JAM": emoji, opis = "🚗🚗", "ZASTOJ"
            elif tip == "ROAD_CLOSED": emoji, opis = "🚧", "DELO NA CESTI"
            
            seznam.append({
                "id": a.get('uuid'), "lat": a.get('location', {}).get('y'), 
                "lon": a.get('location', {}).get('x'), "vir": "V živo", 
                "opis": opis, "icon": emoji
            })
    except: pass

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(seznam, f, ensure_ascii=False, indent=4)
    print(f"Osveženo ob {zdaj}: {len(seznam)} točk.")

if __name__ == "__main__":
    procesiraj()
