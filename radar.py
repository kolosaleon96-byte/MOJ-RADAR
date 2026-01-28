import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. KONFIGURACIJA VIROV ---
FB_SKUPINE = {
    "1": "Pomurje", "2": "Goričko", "3": "Prlekija", "4": "Štajerska",
    "5": "Kolpa-Ljubljana", "6": "Ptuj in okolica", "7": "Ljubljana",
    "8": "Avtoceste", "9": "Maribor", "10": "Majšperk",
    "11": "Ptuj Radarji", "12": "Ribnica-Kočevje", "13": "Kranj", "14": "Postojna"
}

# Waze povezava za celo Slovenijo
WAZE_URL = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"

# --- 2. GPS BAZA (Mesta, izvozi, kamere) ---
LOKACIJE_GPS = {
    "Ljubljan": (46.0569, 14.5058), "Maribor": (46.5547, 15.6459), "Celj": (46.2397, 15.2677),
    "Kranj": (46.2428, 14.3555), "Koper": (45.5488, 13.7301), "Novo mesto": (45.8011, 15.1722),
    "Velenje": (46.3591, 15.1101), "Ptuj": (46.4200, 15.8700), "Murska Sobota": (46.6622, 16.1661),
    "Postojn": (45.7751, 14.2122), "Krško": (45.9591, 15.4911), "Brežice": (45.9031, 15.5951),
    "Lendava": (46.5622, 16.4511), "Vaneča": (46.7214, 16.1633), "Slov. Bistrica": (46.3921, 15.5811),
    "Jesenice": (46.4311, 14.0522), "Nova Gorica": (45.9551, 13.6451), "Domžale": (46.1381, 14.5941),
    "Trojane": (46.1878, 14.8825), "Razcep Kozarje": (46.0425, 14.4489), "Predor Golovec": (46.0382, 14.5422)
}

# --- 3. RADARBOT GOLD (Stalni radarji) ---
STACIONARNI_BAZA = [
    {"kraj": "AC Golovec (Predor)", "lat": 46.0382, "lon": 14.5422},
    {"kraj": "LJ - Celovška", "lat": 46.0792, "lon": 14.4841},
    {"kraj": "LJ - Dunajska", "lat": 46.0841, "lon": 14.5094},
    {"kraj": "MB - Ptujska cesta", "lat": 46.5385, "lon": 15.6662},
    {"kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711},
    {"kraj": "KP - Šmarska cesta", "lat": 45.5401, "lon": 13.7315},
    {"kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622}
]

def dobi_koord(tekst):
    for kraj, koord in LOKACIJE_GPS.items():
        if kraj.lower() in tekst.lower(): return koord
    return None

def skeniraj_waze():
    najdbe = []
    try:
        r = requests.get(WAZE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        podatki = r.json()
        for a in podatki.get('alerts', []):
            if a.get('type') in ['POLICE', 'JAM']:
                najdbe.append({
                    "regija": "Waze", "kraj": f"WAZE: {a.get('subtype', 'Dogodek')}",
                    "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), "vir": "Waze"
                })
    except: pass
    return najdbe

def skeniraj_splet(url, kljucne, vir_ime, barva):
    najdbe = []
    try:
        r = requests.get(url, timeout=10)
        juha = BeautifulSoup(r.text, 'html.parser')
        for dog in juha.find_all(['div', 'p', 'li']):
            tekst = dog.get_text()
            if any(k in tekst.lower() for k in kljucne):
                koord = dobi_koord(tekst)
                if koord:
                    najdbe.append({"regija": vir_ime, "kraj": tekst.strip()[:60], "lat": koord[0], "lon": koord[1], "vir": barva})
    except: pass
    return najdbe

def procesiraj():
    vsi = []
    # 1. Radarbot
    for r in STACIONARNI_BAZA:
        vsi.append({"regija": "Radarbot", "kraj": r["kraj"], "cas": "24/7", "lat": r["lat"], "lon": r["lon"], "vir": "Radarbot"})
    
    # 2. Waze, AMZS, DARS
    vsi.extend(skeniraj_waze())
    vsi.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["radar", "merjenje"], "AMZS", "AMZS"))
    vsi.extend(skeniraj_splet("https://www.promet.si/sl/dogodki", ["zastoj", "nesreča", "zapora"], "DARS", "DARS"))
    vsi.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["kamera", "pretočnost"], "Kamere", "Kamere"))

    # 3. Facebook
    for id_s, ime in FB_SKUPINE.items():
        koord = dobi_koord(f"Radar {ime}")
        if koord and not any(abs(koord[0]-x['lat']) < 0.003 for x in vsi):
            vsi.append({"regija": ime, "kraj": f"FB: {ime}", "cas": datetime.now().strftime("%H:%M"), "lat": koord[0], "lon": koord[1], "vir": "Facebook"})

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    print(f"Sistem posodobljen: {len(vsi)} točk.")

if __name__ == "__main__":
    procesiraj()
