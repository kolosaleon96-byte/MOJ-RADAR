import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. KONFIGURACIJA VIROV ---
FB_SKUPINE = {
    "1": "Pomurje", "2": "Goričko", "3": "Prlekija", "4": "Štajerska",
    "5": "Koroška", "6": "Savinjska", "7": "Zasavje", "8": "Osrednjeslovenska",
    "9": "Gorenjska", "10": "Goriška", "11": "Obalno-kraška", "12": "Jugovzhodna",
    "13": "Posavska", "14": "Primorska", "15": "Avtoceste", "16": "Policija"
}

WAZE_URL = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"

# --- 2. GIGANTSKA GPS BAZA (Vsi kraji + Pomurje + Izvozi) ---
LOKACIJE_GPS = {
    # POMURJE (PODROBNO)
    "Murska Sobota": (46.6622, 16.1661), "Lendava": (46.5622, 16.4511), "Ljutomer": (46.5181, 16.1975),
    "Gornja Radgona": (46.6775, 15.9922), "Beltinci": (46.6047, 16.2383), "Tišina": (46.6533, 16.0850),
    "Puconci": (46.7067, 16.1561), "Rogašovci": (46.8050, 16.0353), "Kuzma": (46.8350, 16.0822),
    "Grad": (46.8155, 16.0967), "Moravske Toplice": (46.6833, 16.2167), "Apače": (46.6961, 15.8111),
    "Radenci": (46.6433, 16.0422), "Križevci": (46.5683, 16.1411), "Veržej": (46.5822, 16.1622),
    "Vaneča": (46.7214, 16.1633), "Mačkovci": (46.7822, 16.1511), "Petanjci": (46.6455, 16.0588),
    "Gederovci": (46.6655, 16.0488), "Sodišinci": (46.6422, 16.0288), "Krog": (46.6455, 16.1411),
    "Turnišče": (46.6311, 16.3211), "Dobrovnik": (46.6519, 16.3514), "Odranci": (46.5867, 16.2778),
    # SLOVENIJA OSTALO
    "Ljubljan": (46.0569, 14.5058), "Maribor": (46.5547, 15.6459), "Celj": (46.2397, 15.2677),
    "Kranj": (46.2428, 14.3555), "Koper": (45.5488, 13.7301), "Novo mesto": (45.8011, 15.1722),
    "Velenje": (46.3591, 15.1101), "Ptuj": (46.4200, 15.8700), "Postojn": (45.7751, 14.2122),
    "Krško": (45.9591, 15.4911), "Brežice": (45.9031, 15.5951), "Jesenice": (46.4311, 14.0522),
    "Nova Gorica": (45.9551, 13.6451), "Domžale": (46.1381, 14.5941), "Trojane": (46.1878, 14.8825),
    "Kozarje": (46.0425, 14.4489), "Golovec": (46.0382, 14.5422), "Črni Kal": (45.5533, 13.8811)
}

# --- 3. VSI FIKSNI RADARJI (SLOVENIJA + POMURJE) ---
STACIONARNI_BAZA = [
    # POMURJE FIKSNI
    {"kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622}, {"kraj": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811},
    {"kraj": "MS - Panonska", "lat": 46.6555, "lon": 16.1711}, {"kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488},
    {"kraj": "Petanjci", "lat": 46.6455, "lon": 16.0588}, {"kraj": "Vaneča", "lat": 46.7214, "lon": 16.1633},
    # LJUBLJANA
    {"kraj": "LJ - Celovška 1", "lat": 46.0792, "lon": 14.4841}, {"kraj": "LJ - Celovška 2", "lat": 46.0945, "lon": 14.4751},
    {"kraj": "LJ - Dunajska 1", "lat": 46.0841, "lon": 14.5094}, {"kraj": "LJ - Dunajska 2", "lat": 46.1011, "lon": 14.5155},
    {"kraj": "LJ - Dolenjska", "lat": 46.0233, "lon": 14.5311}, {"kraj": "LJ - Roška", "lat": 46.0456, "lon": 14.5167},
    # MARIBOR
    {"kraj": "MB - Ptujska 1", "lat": 46.5385, "lon": 15.6662}, {"kraj": "MB - Ptujska 2", "lat": 46.5255, "lon": 15.6711},
    {"kraj": "MB - Tržaška", "lat": 46.5311, "lon": 15.6511}, {"kraj": "MB - Titova", "lat": 46.5511, "lon": 15.6511},
    # CELJE & OSTALO
    {"kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711}, {"kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722},
    {"kraj": "KP - Šmarska", "lat": 45.5401, "lon": 13.7315}, {"kraj": "NM - Bučna vas", "lat": 45.8211, "lon": 15.1511}
]

def dobi_koord(tekst):
    for kraj, koord in LOKACIJE_GPS.items():
        if kraj.lower() in tekst.lower(): return koord
    return None

def skeniraj_waze():
    najdbe = []
    try:
        r = requests.get(WAZE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        for a in r.json().get('alerts', []):
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
                    najdbe.append({"regija": vir_ime, "kraj": tekst.strip()[:80], "lat": koord[0], "lon": koord[1], "vir": barva})
    except: pass
    return najdbe

def procesiraj():
    vsi = []
    # 1. Radarbot (Fiksni)
    for r in STACIONARNI_BAZA:
        vsi.append({"regija": "Fiksni", "kraj": r["kraj"], "cas": "24/7", "lat": r["lat"], "lon": r["lon"], "vir": "Radarbot"})
    
    # 2. V živo (Waze, AMZS, DARS, Kamere)
    vsi.extend(skeniraj_waze())
    vsi.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["radar", "merjenje"], "AMZS", "AMZS"))
    vsi.extend(skeniraj_splet("https://www.promet.si/sl/dogodki", ["zastoj", "nesreča", "zapora"], "DARS", "DARS"))
    vsi.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["kamera", "pretočnost"], "Kamere", "Kamere"))

    # 3. Facebook
    for id_s, ime in FB_SKUPINE.items():
        koord = dobi_koord(ime)
        if koord and not any(abs(koord[0]-x['lat']) < 0.003 for x in vsi):
            vsi.append({"regija": ime, "kraj": f"FB: {ime}", "cas": datetime.now().strftime("%H:%M"), "lat": koord[0], "lon": koord[1], "vir": "Facebook"})

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    print(f"Sistem osvežen: {len(vsi)} točk.")

if __name__ == "__main__":
    procesiraj()
