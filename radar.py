import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. SEZNAM FB SKUPIN ---
FB_SKUPINE = {
    "1": "Pomurje", "2": "Goričko", "3": "Prlekija", "4": "Štajerska",
    "5": "Kolpa-Ljubljana", "6": "Ptuj in okolica", "7": "Ljubljana",
    "8": "Avtoceste", "9": "Maribor", "10": "Majšperk",
    "11": "Ptuj Radarji", "12": "Ribnica-Kočevje", "13": "Kranj", "14": "Postojna"
}

# --- 2. RAZŠIRJENA GPS BAZA (Mesta, Izvozi, Kamere) ---
LOKACIJE_GPS = {
    "Ljubljan": (46.0569, 14.5058), "Maribor": (46.5547, 15.6459), "Celj": (46.2397, 15.2677),
    "Kranj": (46.2428, 14.3555), "Koper": (45.5488, 13.7301), "Novo mesto": (45.8011, 15.1722),
    "Velenje": (46.3591, 15.1101), "Ptuj": (46.4200, 15.8700), "Murska Sobota": (46.6622, 16.1661),
    "Postojn": (45.7751, 14.2122), "Krško": (45.9591, 15.4911), "Brežice": (45.9031, 15.5951),
    "Lendava": (46.5622, 16.4511), "Vaneča": (46.7214, 16.1633), "Slov. Bistrica": (46.3921, 15.5811),
    "Jesenice": (46.4311, 14.0522), "Nova Gorica": (45.9551, 13.6451), "Domžale": (46.1381, 14.5941),
    "Razcep Kozarje": (46.0425, 14.4489), "Predor Golovec": (46.0382, 14.5422),
    "Izvoz Bežigrad": (46.0822, 14.5122), "Viadukt Črni Kal": (45.5533, 13.8811),
    "Predor Karavanke": (46.4811, 14.0122), "Trojane": (46.1878, 14.8825)
}

# --- 3. RADARBOT GOLD (Stalni radarji) ---
STACIONARNI_BAZA = [
    {"kraj": "AC Golovec (Predor)", "lat": 46.0382, "lon": 14.5422},
    {"kraj": "LJ - Celovška", "lat": 46.0792, "lon": 14.4841},
    {"kraj": "LJ - Dunajska", "lat": 46.0841, "lon": 14.5094},
    {"kraj": "MB - Ptujska cesta", "lat": 46.5385, "lon": 15.6662},
    {"kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711},
    {"kraj": "KP - Šmarska cesta", "lat": 45.5401, "lon": 13.7315},
    {"kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622},
    {"kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722},
    {"kraj": "AC - Lukovica", "lat": 46.1681, "lon": 14.6851}
]

def dobi_koord(tekst):
    for kraj, koord in LOKACIJE_GPS.items():
        if kraj.lower() in tekst.lower():
            return koord
    return None

def skeniraj_splet(url, kljucne_besede, vir_ime, barva_v_json):
    najdbe = []
    try:
        r = requests.get(url, timeout=10)
        juha = BeautifulSoup(r.text, 'html.parser')
        for dogodek in juha.find_all(['div', 'p', 'li']):
            tekst = dogodek.get_text()
            if any(b in tekst.lower() for b in kljucne_besede):
                koord = dobi_koord(tekst)
                if koord:
                    najdbe.append({
                        "regija": vir_ime,
                        "kraj": tekst.strip()[:60],
                        "lat": koord[0], "lon": koord[1],
                        "vir": barva_v_json
                    })
    except: pass
    return najdbe

def procesiraj():
    koncni = []
    
    # 1. Dodajanje Radarbot Gold (Oranžna)
    for r in STACIONARNI_BAZA:
        koncni.append({"regija": "Radarbot Gold", "kraj": r["kraj"], "cas": "24/7", "lat": r["lat"], "lon": r["lon"], "vir": "Radarbot"})

    # 2. AMZS Radarji (Rumena)
    koncni.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["radar", "merjenje"], "AMZS Radar", "AMZS"))

    # 3. DARS Zastoji/Nesreče (Rdeča)
    koncni.extend(skeniraj_splet("https://www.promet.si/sl/dogodki", ["zastoj", "nesreča", "zapora", "ovira"], "DARS Promet", "DARS"))

    # 4. AMZS Kamere (Siva)
    koncni.extend(skeniraj_splet("https://www.amzs.si/na-poti/stanje-na-cestah", ["kamera", "pretočnost"], "AMZS Kamere", "Kamere"))

    # 5. Facebook (Modra)
    for id_s, ime in FB_SKUPINE.items():
        koord = dobi_koord(f"Radar {ime}")
        if koord and not any(abs(koord[0]-x['lat']) < 0.003 for x in koncni):
            koncni.append({"regija": ime, "kraj": f"FB Javljanje: {ime}", "cas": datetime.now().strftime("%H:%M"), "lat": koord[0], "lon": koord[1], "vir": "Facebook"})

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(koncni, f, ensure_ascii=False, indent=4)
    print(f"Sistem posodobljen. Najdenih {len(koncni)} točk.")

if __name__ == "__main__":
    procesiraj()
