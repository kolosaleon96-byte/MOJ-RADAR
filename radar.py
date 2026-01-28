import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 1. GPS BAZA (Tukaj robot ve, kje so kraji)
def dobi_koordinate(tekst):
    lokacije = {
        "Vaneča": (46.7214, 16.1633),
        "Ljubljan": (46.0569, 14.5058),
        "Celj": (46.2397, 15.2677),
        "Maribor": (46.5547, 15.6459),
        "Kranj": (46.2428, 14.3555),
        "Postojn": (45.7751, 14.2122)
    }
    for kraj, koord in lokacije.items():
        if kraj.lower() in tekst.lower():
            return koord
    return None

# 2. AMZS SKENER
def preveri_amzs():
    print("Preverjam AMZS...")
    amzs_najdbe = []
    try:
        url = "https://www.amzs.si/na-poti/stanje-na-cestah"
        odziv = requests.get(url, timeout=10)
        juha = BeautifulSoup(odziv.text, 'html.parser')
        
        # AMZS objavlja radarje v posebnih blokih besedila
        vsa_besedila = juha.get_text()
        
        # Testno iskanje besed v AMZS poročilu
        if "radar" in vsa_besedila.lower() or "merjenje" in vsa_besedila.lower():
            # Tukaj robot išče kraje iz najine GPS baze znotraj AMZS poročila
            for kraj in ["Celj", "Ljubljan", "Maribor", "Postojn"]:
                if kraj.lower() in vsa_besedila.lower():
                    koord = dobi_koordinate(kraj)
                    amzs_najdbe.append({
                        "regija": "AMZS Uradno",
                        "kraj": f"Radar: {kraj} (AMZS)",
                        "cas": datetime.now().strftime("%H:%M"),
                        "lat": koord[0],
                        "lon": koord[1],
                        "vir": "AMZS"
                    })
    except:
        print("AMZS stran trenutno ni dosegljiva.")
    return amzs_najdbe

def procesiraj():
    # Najprej Facebook (Tvoji testni točki, ki ju že vidiš)
    vsi_radarji = [
        {"regija": "Pomurje", "kraj": "Policijska kontrola Vaneča", "cas": "06:58", "lat": 46.7214, "lon": 16.1633, "vir": "Facebook"},
        {"regija": "Ljubljana", "kraj": "Radar Dunajska", "cas": "06:58", "lat": 46.0569, "lon": 14.5058, "vir": "Facebook"}
    ]
    
    # Dodamo še AMZS najdbe
    vsi_radarji.extend(preveri_amzs())
    
    # Shranimo vse skupaj
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, ensure_ascii=False, indent=4)
    print(f"Končano! Skupno število točk: {len(vsi_radarji)}")

if __name__ == "__main__":
    procesiraj()
