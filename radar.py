import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 1. TVOJIH 14 SKUPIN (Ostanejo nespremenjene)
SKUPINE = {
    "1": "Pomurje", "2": "Goričko", "3": "Prlekija", "4": "Štajerska",
    "5": "Kolpa-Ljubljana", "6": "Ptuj in okolica", "7": "Ljubljana",
    "8": "Avtoceste", "9": "Maribor", "10": "Majšperk",
    "11": "Ptuj Radarji", "12": "Ribnica-Kočevje", "13": "Kranj", "14": "Postojna"
}

# 2. GPS BAZA (Tukaj bova dodajala nove kraje)
def dobi_koordinate(tekst):
    lokacije = {
        "Vaneča": (46.7214, 16.1633),
        "Ljubljan": (46.0569, 14.5058),
        "Celj": (46.2397, 15.2677),
        "Maribor": (46.5547, 15.6459)
    }
    for kraj, koord in lokacije.items():
        if kraj.lower() in tekst.lower():
            return koord
    return None

# 3. NOVA FUNKCIJA: AMZS ROBOT
def preveri_amzs():
    print("Preverjam AMZS spletno stran...")
    amzs_najdbe = []
    try:
        # Robot obišče AMZS
        url = "https://www.amzs.si/na-poti/stanje-na-cestah"
        odziv = requests.get(url, timeout=10)
        juha = BeautifulSoup(odziv.text, 'html.parser')
        
        # Poišče vse dogodke na cesti
        dogodki = juha.find_all('div', class_='road-event')
        
        for dogodek in dogodki:
            vsebina = dogodek.get_text()
            if "radar" in vsebina.lower() or "hitrost" in vsebina.lower():
                koord = dobi_koordinate(vsebina)
                if koord:
                    amzs_najdbe.append({
                        "regija": "AMZS (Uradno)",
                        "kraj": "URADNO: " + vsebina[:50] + "...",
                        "cas": datetime.now().strftime("%H:%M"),
                        "lat": koord[0],
                        "lon": koord[1],
                        "vir": "AMZS"
                    })
    except Exception as e:
        print(f"Napaka pri AMZS: {e}")
    return amzs_najdbe

def procesiraj_vse():
    # 1. Najprej Facebook del (Tvoj obstoječi sistem)
    fb_najdbe = [
        {"id": "1", "tekst": "Policijska kontrola Vaneča pri pokopališču"},
        {"id": "7", "tekst": "Radar na Dunajski cesti v Ljubljani"}
    ]
    
    vsi_podatki = []
    for objava in fb_najdbe:
        koord = dobi_koordinate(objava["tekst"])
        if koord:
            vsi_podatki.append({
                "regija": SKUPINE[objava["id"]],
                "kraj": objava["tekst"],
                "cas": datetime.now().strftime("%H:%M"),
                "lat": koord[0],
                "lon": koord[1],
                "vir": "Facebook"
            })

    # 2. Nato dodamo AMZS podatke
    vsi_podatki.extend(preveri_amzs())

    # 3. Shranjevanje vseh virov v eno datoteko
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_podatki, f, ensure_ascii=False, indent=4)
    
    print(f"Uspešno shranjeno {len(vsi_podatki)} lokacij iz vseh virov.")

if __name__ == "__main__":
    procesiraj_vse()
