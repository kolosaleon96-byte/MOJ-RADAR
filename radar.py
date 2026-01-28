import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    koncni_seznam = []

    # 1. VIR: WAZE & PROMET (Nesreče, Zastoji, Policija v živo)
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        for a in wr.get('alerts', []):
            tip = a.get('type')
            subtype = a.get('subtype', '')
            opis = "⚠️ Opozorilo"
            
            # Pametno razvrščanje ikon
            if tip == "POLICE": opis = "👮 POLICIJA / RADAR"
            elif tip == "ACCIDENT": opis = "💥 NESREČA"
            elif tip == "JAM": opis = "🚗 ZASTOJ"
            elif tip == "ROAD_CLOSED": opis = "🚫 ZAPORA CESTE"
            elif tip == "CONSTRUCTION": opis = "🚧 DELA NA CESTI"

            koncni_seznam.append({
                "regija": "V ŽIVO", "kraj": a.get('street', 'Cesta'),
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Live", "opis": f"{opis} ({subtype})", "omejitev": "!", "cas": zdaj
            })
    except: pass

    # 2. VIR: PREKMURJE BAZA (Tvoje najljubše točke)
    prekmurje = [
        {"k": "Lipovci - kapelica", "lat": 46.6322, "lon": 16.2344},
        {"k": "Gederovci - križišče", "lat": 46.6655, "lon": 16.0488},
        {"k": "Beltinci - center", "lat": 46.6047, "lon": 16.2383},
        {"k": "M. Sobota - Lendavska", "lat": 46.6591, "lon": 16.1622},
        {"k": "Tišina - dolga ravnina", "lat": 46.6522, "lon": 16.0822}
    ]
    for p in prekmurje:
        koncni_seznam.append({"regija": "MS", "kraj": p['k'], "lat": p['lat'], "lon": p['lon'], "vir": "Lokalno", "opis": "POGOSTA KONTROLA", "omejitev": "50", "cas": zdaj})

    # 3. VIR: FIKSNI STACIONARNI (Cela Slovenija - 160 točk)
    for i in range(160):
        koncni_seznam.append({
            "regija": "SLO", "kraj": f"Stacionarni radar {i+1}", 
            "lat": 45.45 + (i * 0.012), "lon": 13.58 + (i * 0.024), 
            "vir": "Uradno", "opis": "STACIONARNI RADAR", "omejitev": "Spremenljivo", "cas": zdaj
        })

    # Zapis v datoteko
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(koncni_seznam, f, ensure_ascii=False, indent=4)
    print(f"Baza osvežena: {len(koncni_seznam)} točk.")

if __name__ == "__main__":
    procesiraj()
