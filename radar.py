import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    vsi = []

    # --- 1. FIKSNA BAZA: STACIONARNI RADARJI (CELA SLOVENIJA & PODROBNO PREKMURJE) ---
    stacionarni = [
        # --- PREKMURJE (PODROBNO) ---
        {"regija": "Prekmurje", "kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "MS - Panonska", "lat": 46.6555, "lon": 16.1711, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "Vaneča", "lat": 46.7214, "lon": 16.1633, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "Petanjci", "lat": 46.6455, "lon": 16.0588, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Prekmurje", "kraj": "Ljutomer center", "lat": 46.5181, "lon": 16.1975, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},

        # --- ŠTAJERSKA & MARIBOR ---
        {"regija": "Maribor", "kraj": "MB - Ptujska cesta", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "70 km/h"},
        {"regija": "Maribor", "kraj": "MB - Tržaška", "lat": 46.5355, "lon": 15.6511, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "70 km/h"},
        {"regija": "Celje", "kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Slov. Bistrica", "kraj": "Bistrica - obvoznica", "lat": 46.3922, "lon": 15.5811, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "60 km/h"},

        # --- LJUBLJANA & OSREDNJA SLO ---
        {"regija": "Ljubljana", "kraj": "LJ - Celovška (pri McDonald'su)", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "60 km/h"},
        {"regija": "Ljubljana", "kraj": "LJ - Dunajska", "lat": 46.0855, "lon": 14.5111, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "60 km/h"},
        {"regija": "Ljubljana", "kraj": "LJ - Roška", "lat": 46.0455, "lon": 14.5211, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},
        {"regija": "Ljubljana", "kraj": "LJ - Dolenjska", "lat": 46.0311, "lon": 14.5311, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h"},

        # --- AVTOCESTE (DARS & KAMERE) ---
        {"regija": "AC", "kraj": "AC - Predor Golovec", "lat": 46.0382, "lon": 14.5422, "vir": "DARS", "opis": "SEKCIJSKO MERJENJE", "omejitev": "100 km/h"},
        {"regija": "AC", "kraj": "AC - Viadukt Črni Kal", "lat": 45.5533, "lon": 13.8811, "vir": "DARS", "opis": "RADAR / KAMERA", "omejitev": "100 km/h"},
        {"regija": "AC", "kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722, "vir": "DARS", "opis": "NADZORNA TOČKA", "omejitev": "130 km/h"},
        {"regija": "AC", "kraj": "AC - Lom", "lat": 45.8922, "lon": 14.3511, "vir": "DARS", "opis": "NADZORNA TOČKA", "omejitev": "130 km/h"}
    ]
    
    for r in stacionarni:
        r["cas"] = zdaj
        vsi.append(r)

    # --- 2. WAZE & DARS LIVE (ZA NESREČE, DELO IN POLICIJO) ---
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if wr.status_code == 200:
            for a in wr.json().get('alerts', []):
                vsi.append({
                    "regija": "Slovenija", "kraj": a.get('street', 'Cesta'),
                    "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                    "vir": "Waze Live", "opis": f"V ŽIVO: {a.get('type')} ({a.get('subtype', '')})", 
                    "omejitev": "Preveri", "cas": zdaj
                })
    except: pass

    # --- 3. AMZS & PROMET.SI (PODROBNOSTI O STANJU) ---
    try:
        r_amzs = requests.get("https://www.amzs.si/na-poti/stanje-na-cestah", timeout=5)
        if "radar" in r_amzs.text.lower():
            vsi.append({"regija": "Slovenija", "kraj": "AMZS Obvestilo", "lat": 46.1, "lon": 14.8, "vir": "AMZS", "opis": "AMZS javi: Aktivne meritve hitrosti!", "omejitev": "-", "cas": zdaj})
    except: pass

    # --- KONČNI ZAPIS ---
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"BOGATA BAZA OSVEŽENA: {len(vsi)} točk (Stacionarni radarji + živo).")

if __name__ == "__main__":
    procesiraj()
