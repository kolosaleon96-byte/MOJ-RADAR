import os, json, requests
from bs4 import BeautifulSoup
from datetime import datetime

def procesiraj():
    vsi = [
        # --- POMURJE (PODROBNO) ---
        {"regija": "Pomurje", "kraj": "MS-Lendavska (Radar)", "lat": 46.6591, "lon": 16.1622, "vir": "Radarbot"},
        {"regija": "Pomurje", "kraj": "MS-Noršinska (Radar)", "lat": 46.6655, "lon": 16.1811, "vir": "Radarbot"},
        {"regija": "Pomurje", "kraj": "MS-Panonska (Radar)", "lat": 46.6555, "lon": 16.1711, "vir": "Radarbot"},
        {"regija": "Pomurje", "kraj": "Gederovci (Kamera)", "lat": 46.6655, "lon": 16.0488, "vir": "Kamere"},
        {"regija": "Pomurje", "kraj": "Petanjci (Radar)", "lat": 46.6455, "lon": 16.0588, "vir": "Radarbot"},
        {"regija": "Pomurje", "kraj": "Vaneča (Radar)", "lat": 46.7214, "lon": 16.1633, "vir": "Radarbot"},
        {"regija": "Pomurje", "kraj": "Beltinci", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook"},
        {"regija": "Pomurje", "kraj": "Ljutomer", "lat": 46.5181, "lon": 16.1975, "vir": "Facebook"},
        {"regija": "Pomurje", "kraj": "Radenci", "lat": 46.6433, "lon": 16.0422, "vir": "DARS"},
        {"regija": "Pomurje", "kraj": "Lendava AC", "lat": 46.5511, "lon": 16.4411, "vir": "Kamere"},
        {"regija": "Pomurje", "kraj": "G. Radgona", "lat": 46.6775, "lon": 15.9922, "vir": "Facebook"},
        {"regija": "Pomurje", "kraj": "Puconci", "lat": 46.7055, "lon": 16.1522, "vir": "Facebook"},
        {"regija": "Pomurje", "kraj": "Turnišče", "lat": 46.6311, "lon": 16.3211, "vir": "Facebook"},
        
        # --- SLOVENIJA OSTALO ---
        {"regija": "LJ", "kraj": "LJ-Celovška", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot"},
        {"regija": "MB", "kraj": "MB-Ptujska", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot"},
        {"regija": "AC", "kraj": "Tepanje", "lat": 46.3455, "lon": 15.4722, "vir": "Kamere"},
        {"regija": "Obala", "kraj": "Črni Kal", "lat": 45.5533, "lon": 13.8811, "vir": "Kamere"}
    ]

    # --- WAZE INTEGRACIJA ---
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        for a in wr.json().get('alerts', []):
            vsi.append({
                "regija": "Waze Live", "kraj": f"WAZE: {a.get('subtype', 'Kontrola')}",
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Waze", "cas": datetime.now().strftime("%H:%M")
            })
    except: pass

    # --- AMZS & DARS SKENIRANJE ---
    for url, vir_ime in [("https://www.amzs.si/na-poti/stanje-na-cestah", "AMZS"), ("https://www.promet.si/sl/dogodki", "DARS")]:
        try:
            r = requests.get(url, timeout=10)
            if "radar" in r.text.lower() or "merjenje" in r.text.lower():
                vsi.append({"regija": vir_ime, "kraj": f"{vir_ime}: Aktivno merjenje!", "lat": 46.05, "lon": 14.5, "vir": vir_ime})
        except: pass

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    print(f"Sistem osvežen: {len(vsi)} točk.")

if __name__ == "__main__":
    procesiraj()
