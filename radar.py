import os
import json
import time
import requests
from datetime import datetime
from pyotp import TOTP

# 1. SEZNAM VSEH 14 SKUPIN
SKUPINE = {
    "1": {"ime": "Pomurje", "url": "https://www.facebook.com/share/g/1A66ngSA7S/"},
    "2": {"ime": "Goričko", "url": "https://www.facebook.com/share/g/1AURw43PaO/"},
    "3": {"ime": "Prlekija", "url": "https://www.facebook.com/share/g/1AG6ngSA7S/"},
    "4": {"ime": "Štajerska", "url": "https://www.facebook.com/share/g/14VAAgZQTSM/"},
    "5": {"ime": "Kolpa-Ljubljana", "url": "https://www.facebook.com/share/g/1FzLgWdD56/"},
    "6": {"ime": "Ptuj in okolica", "url": "https://www.facebook.com/share/g/1AX5CApbYY/"},
    "7": {"ime": "Ljubljana", "url": "https://www.facebook.com/share/g/1AcsLDZkMf/"},
    "8": {"ime": "Avtoceste", "url": "https://www.facebook.com/share/g/1GEuSgMzFp/"},
    "9": {"ime": "Maribor", "url": "https://www.facebook.com/share/g/14RhQ9s9VGt/"},
    "10": {"ime": "Majšperk", "url": "https://www.facebook.com/share/g/1AULetVbhF/"},
    "11": {"ime": "Ptuj Radarji", "url": "https://www.facebook.com/share/g/17kbN7tFwc/"},
    "12": {"ime": "Ribnica-Kočevje", "url": "https://www.facebook.com/share/g/14TpDav7nez/"},
    "13": {"ime": "Kranj", "url": "https://www.facebook.com/share/g/1HzHQCBFnc/"},
    "14": {"ime": "Postojna", "url": "https://www.facebook.com/share/g/1BzhQCBFnc/"}
}

# 2. POMOŽNA FUNKCIJA ZA GPS
def dobi_koordinate(tekst):
    lokacije = {
        "Vaneča": (46.7214, 16.1633),
        "Ljubljan": (46.0569, 14.5058),
        "Postojn": (45.7751, 14.2122),
        "Maribor": (46.5547, 15.6459),
        "Kranj": (46.2428, 14.3555),
        "Murska": (46.6622, 16.1661)
    }
    for kraj, koord in lokacije.items():
        if kraj.lower() in tekst.lower():
            return koord
    return None

def procesiraj_vse_skupine():
    vsi_radarji = []
    print(f"--- ZAGON ROBOTA: {datetime.now().strftime('%d.%m. ob %H:%M')} ---")

    # Tukaj bova zdaj simulirala najdbe, da se piki takoj narišeta
    # V pravi verziji robot tukaj uporabi tvoje geslo in 2FA za FB
    najdene_objave = [
        {"id": "1", "tekst": "Policijska kontrola Vaneča pri pokopališču"},
        {"id": "7", "tekst": "Radar na Dunajski cesti v Ljubljani"}
    ]

    for objava in najdene_objave:
        koord = dobi_koordinate(objava["tekst"])
        if koord:
            vsi_radarji.append({
                "regija": SKUPINE[objava["id"]]["ime"],
                "kraj": objava["tekst"],
                "cas": datetime.now().strftime("%H:%M"),
                "lat": koord[0],
                "lon": koord[1]
            })
            print(f"[!] NAJDENO: {objava['tekst']} v skupini {SKUPINE[objava['id']]['ime']}")

    # KLJUČNI DEL: Shranjevanje, da zemljevid ne bo več prazen!
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, ensure_ascii=False, indent=4)
    
    print(f"--- KONČANO: V datoteko shranjenih {len(vsi_radarji)} radarjev ---")

if __name__ == "__main__":
    procesiraj_vse_skupine()
