import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pyotp
import time

# 1. NASTAVITVE IN SKUPINE
SKUPINE = {
    "1": "Pomurje", "2": "Goričko", "3": "Prlekija", "4": "Štajerska",
    "5": "Kolpa-Ljubljana", "6": "Ptuj in okolica", "7": "Ljubljana",
    "8": "Avtoceste", "9": "Maribor", "10": "Majšperk",
    "11": "Ptuj Radarji", "12": "Ribnica-Kočevje", "13": "Kranj", "14": "Postojna"
}

# 2. GPS BAZA (Tukaj dodajaj nove kraje, ko jih robot najde)
def dobi_koordinate(tekst):
    lokacije = {
        "Vaneča": (46.7214, 16.1633), "Ljubljan": (46.0569, 14.5058),
        "Celj": (46.2397, 15.2677), "Maribor": (46.5547, 15.6459),
        "Postojn": (45.7751, 14.2122), "Kranj": (46.2428, 14.3555),
        "Ptuj": (46.4200, 15.8700), "Murska": (46.6622, 16.1661)
    }
    for kraj, koord in lokacije.items():
        if kraj.lower() in tekst.lower():
            return koord
    return None

# 3. AMZS SKENER
def preveri_amzs():
    amzs_najdbe = []
    try:
        url = "https://www.amzs.si/na-poti/stanje-na-cestah"
        odziv = requests.get(url, timeout=10)
        juha = BeautifulSoup(odziv.text, 'html.parser')
        vsa_besedila = juha.get_text()
        
        if "radar" in vsa_besedila.lower() or "merjenje" in vsa_besedila.lower():
            for kraj in ["Celj", "Ljubljan", "Maribor", "Postojn", "Kranj"]:
                if kraj.lower() in vsa_besedila.lower():
                    koord = dobi_koordinate(kraj)
                    if koord:
                        amzs_najdbe.append({
                            "regija": "AMZS Uradno",
                            "kraj": f"Radar: {kraj} (Uradno potrjeno)",
                            "cas": datetime.now().strftime("%H:%M"),
                            "lat": koord[0], "lon": koord[1], "vir": "AMZS"
                        })
    except:
        pass
    return amzs_najdbe

# 4. GLAVNI PROCES
def procesiraj():
    vsi_radarji = []
    
    # Tukaj robot uporabi tvoje Secrets za prijavo (Simulacija prijave)
    email = os.getenv("FB_EMAIL")
    geslo = os.getenv("FB_PASS")
    skrivnost_2fa = os.getenv("FB_2FA_KEY")
    
    if skrivnost_2fa:
        totp = pyotp.TOTP(skrivnost_2fa.replace(" ", ""))
        print(f"Generirana 2FA koda: {totp.now()}")

    # TESTNI PODATKI (Robot bi tukaj bral FB - za zdaj pustiva te, da vidiva delovanje)
    fb_objave = [
        {"id": "1", "tekst": "Policijska kontrola Vaneča pri pokopališču"},
        {"id": "7", "tekst": "Radar na Dunajski cesti v Ljubljani"}
    ]

    for objava in fb_objave:
        koord = dobi_koordinate(objava["tekst"])
        if koord:
            vsi_radarji.append({
                "regija": SKUPINE.get(objava["id"], "Neznano"),
                "kraj": objava["tekst"],
                "cas": datetime.now().strftime("%H:%M"),
                "lat": koord[0], "lon": koord[1], "vir": "Facebook"
            })

    vsi_radarji.extend(preveri_amzs())

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, ensure_ascii=False, indent=4)
    print(f"Robot končal. Najdenih {len(vsi_radarji)} točk.")

if __name__ == "__main__":
    procesiraj()
