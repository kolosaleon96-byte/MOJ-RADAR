import requests
import json
import time

# VIRI PODATKOV
# 1. DARS (Promet.si) javni podatki
DARS_URL = "https://www.promet.si/dc/traffic.events.public.json"

def posodobi_radarje():
    novi_radarji = []

    # --- POBERI DARS PODATKE ---
    try:
        odgovor = requests.get(DARS_URL, timeout=10)
        podatki = odgovor.json()
        for event in podatki.get('contents', []):
            # Iščemo radarje in dela na cesti
            if "radar" in event.get('description', '').lower() or event.get('type') == 'CONSTRUCTION':
                novi_radarji.append({
                    "lat": event.get('y'),
                    "lon": event.get('x'),
                    "tip": "DARS OPOZORILO",
                    "icon": "🚧" if event.get('type') == 'CONSTRUCTION' else "📸",
                    "opis": event.get('description', 'Opozorilo na poti'),
                    "vir": "DARS",
                    "limit": "80"
                })
    except Exception as e:
        print(f"Dars napaka: {e}")

    # --- SIMULACIJA WAZE SKENIRANJA ---
    # Ker Waze zahteva posebne glave (headers), tukaj robot doda tisto, kar vidi na Live Map
    # V tej fazi robot doda nujne fiksne točke, ki jih Waze vedno kaže
    waze_testni = [
        {"lat": 46.051, "lon": 14.505, "tip": "POLICIJA", "icon": "👮", "opis": "Waze: Mobilni radar", "vir": "WAZE", "limit": "50"}
    ]
    novi_radarji.extend(waze_testni)

    # --- OHRANI STACIONARNE (POMURJE) ---
    # Preberemo obstoječe, da jih robot ne povozi
    try:
        with open('radarji.json', 'r', encoding='utf-8') as f:
            stari = json.load(f)
            # Obdržimo samo tiste, ki so "STACIONARNI RADAR" (Zeleni)
            stacionarni = [r for r in stari if r.get('tip') == "STACIONARNI RADAR"]
            novi_radarji.extend(stacionarni)
    except:
        pass

    # SHRANI VSE SKUPAJ
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(novi_radarji, f, indent=2, ensure_ascii=False)
    
    print(f"Robot: Uspešno posodobljeno! Najdenih {len(novi_radarji)} točk.")

if __name__ == "__main__":
    posodobi_radarje()
