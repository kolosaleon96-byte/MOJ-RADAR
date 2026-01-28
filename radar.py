import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    vsi = []
    videni = set() # Za preprečevanje podvajanja

    # 1. TEMELJNA BAZA: VSE STACIONARNO IN FACEBOOK (Najbolj podrobno)
    baza = [
        # PREKMURJE - VSE MOŽNE TOČKE
        {"r": "Prekmurje", "k": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "MS - Panonska", "lat": 46.6555, "lon": 16.1711, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "Gederovci", "lat": 46.6655, "lon": 16.0488, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "Petanjci", "lat": 46.6455, "lon": 16.0588, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "Vaneča", "lat": 46.7214, "lon": 16.1633, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "Beltinci", "lat": 46.6047, "lon": 16.2383, "v": "Policija", "o": "50"},
        {"r": "Prekmurje", "k": "Radenci", "lat": 46.6433, "lon": 16.0422, "v": "Policija", "o": "50"},
        {"r": "Prekmurje", "k": "Ljutomer", "lat": 46.5181, "lon": 16.1975, "v": "Radar", "o": "50"},
        {"r": "Prekmurje", "k": "Lendava AC", "lat": 46.5511, "lon": 16.4411, "v": "Kamera", "o": "130"},
        
        # CELA SLOVENIJA - GLAVNI RADARJI
        {"r": "MB", "k": "MB - Ptujska", "lat": 46.5385, "lon": 15.6662, "v": "Radar", "o": "70"},
        {"r": "LJ", "k": "LJ - Celovška", "lat": 46.0792, "lon": 14.4841, "v": "Radar", "o": "60"},
        {"r": "AC", "k": "AC - Golovec", "lat": 46.0382, "lon": 14.5422, "v": "Nadzor", "o": "100"},
        {"r": "AC", "k": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722, "v": "Nadzor", "o": "130"}
    ]

    for b in baza:
        vsi.append({"regija": b["r"], "kraj": b["k"], "lat": b["lat"], "lon": b["lon"], "vir": b["v"], "opis": f"FIKSNA TOČKA: {b['v']}", "omejitev": b["o"], "cas": zdaj})
        videni.add((round(b["lat"], 3), round(b["lon"], 3)))

    # 2. WAZE, AMZS, DARS - VSE V ŽIVO (Z zaščito pred napakami)
    # Waze skeniranje
    try:
        w_res = requests.get("https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        for a in w_res.get('alerts', []):
            lat, lon = a.get('location', {}).get('y'), a.get('location', {}).get('x')
            if (round(lat, 3), round(lon, 3)) not in videni:
                vsi.append({"regija": "Slovenija", "kraj": a.get('street', 'Cesta'), "lat": lat, "lon": lon, "vir": "Waze Live", "opis": f"V ŽIVO: {a.get('type')}", "omejitev": "Preveri", "cas": zdaj})
    except: print("Waze preskočen.")

    # AMZS/DARS skeniranje
    for url, ime in [("https://www.amzs.si/na-poti/stanje-na-cestah", "AMZS"), ("https://www.promet.si/sl/dogodki", "DARS")]:
        try:
            r = requests.get(url, timeout=5)
            if "radar" in r.text.lower() or "nesreča" in r.text.lower():
                vsi.append({"regija": "Slovenija", "kraj": f"Obvestilo {ime}", "lat": 46.05, "lon": 14.5, "vir": ime, "opis": f"Uradno poročilo: {ime}", "omejitev": "-", "cas": zdaj})
        except: print(f"{ime} preskočen.")

    # 3. ZAPIS
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"SISTEM KONČAN: {len(vsi)} točk pripravljenih.")

if __name__ == "__main__":
    procesiraj()
