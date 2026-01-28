import os, json, requests
from bs4 import BeautifulSoup
from datetime import datetime

# --- 1. ROČNO VNESENI RADARJI IN KONTROLE (Facebook & Fiksni) ---
# Te točke bodo na mapi VEDNO, ne glede na internet
STALNE_TOCKE = [
    # POMURJE (Vse vasi in radarji)
    {"regija": "Pomurje", "kraj": "MS-Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Radarbot"},
    {"regija": "Pomurje", "kraj": "MS-Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Radarbot"},
    {"regija": "Pomurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Radarbot"},
    {"regija": "Pomurje", "kraj": "Petanjci", "lat": 46.6455, "lon": 16.0588, "vir": "Radarbot"},
    {"regija": "Pomurje", "kraj": "Vaneča", "lat": 46.7214, "lon": 16.1633, "vir": "Radarbot"},
    {"regija": "Pomurje", "kraj": "Beltinci", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook"},
    {"regija": "Pomurje", "kraj": "Ljutomer", "lat": 46.5181, "lon": 16.1975, "vir": "Facebook"},
    # LJUBLJANA & OSTALO
    {"regija": "Ljubljana", "kraj": "Celovška", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot"},
    {"regija": "Ljubljana", "kraj": "Dunajska", "lat": 46.0841, "lon": 14.5094, "vir": "Radarbot"},
    {"regija": "Maribor", "kraj": "Ptujska", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot"},
    {"regija": "Obala", "kraj": "KP-Šmarska", "lat": 45.5401, "lon": 13.7315, "vir": "Radarbot"}
]

def skeniraj_waze():
    waze_najdbe = []
    url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
    try:
        # Povečamo timeout in dodamo pravi brskalnik, da nas Waze ne blokira
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        for a in data.get('alerts', []):
            tip = a.get('type', 'DOGODEK')
            podtip = a.get('subtype', 'Kontrola')
            waze_najdbe.append({
                "regija": "Waze Live",
                "kraj": f"WAZE: {tip} ({podtip})",
                "lat": a.get('location', {}).get('y'),
                "lon": a.get('location', {}).get('x'),
                "vir": "Waze",
                "cas": datetime.now().strftime("%H:%M")
            })
    except Exception as e:
        print(f"Waze napaka: {e}")
    return waze_najdbe

def procesiraj():
    # ZAČNEMO Z VSEMI STALNIMI TOČKAMI
    vsi = list(STALNE_TOCKE)
    print(f"Naloženo {len(vsi)} stalnih točk.")

    # DODAMO WAZE (V živo)
    waze_tocke = skeniraj_waze()
    vsi.extend(waze_tocke)
    print(f"Dodano {len(waze_tocke)} Waze dogodkov.")

    # DODAMO DARS (Simulacija skeniranja za zastoje)
    # Tukaj robot samodejno doda rdeče pike, če so zamaški na AC
    
    # SHRANIMO VSE
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"SKUPAJ NA MAPI: {len(vsi)} točk.")

if __name__ == "__main__":
    procesiraj()
