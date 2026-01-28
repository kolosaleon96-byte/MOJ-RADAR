import requests
import json
import os

# VIRI PODATKOV
PROMET_URL = "https://www.promet.si/dc/traffic.events.public.json"
# Waze zahteva simulacijo brskalnika, zato dodamo 'headers'
WAZE_URL = "https://www.waze.com/rtp-api/web/map/details?bbox=13.3,45.4,16.6,46.9"

def posodobi():
    vsi_radarji = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    # --- 1. WAZE (Policija in mobilni radarji) ---
    try:
        w_res = requests.get(WAZE_URL, headers=headers, timeout=10)
        if w_res.status_code == 200:
            w_data = w_res.json()
            # Waze podatki so v 'alerts'
            for alert in w_data.get('alerts', []):
                if alert.get('type') == 'POLICE':
                    vsi_radarji.append({
                        "lat": alert.get('location', {}).get('y'),
                        "lon": alert.get('location', {}).get('x'),
                        "tip": "POLICIJA / MOBILNI RADAR", "icon": "👮",
                        "opis": "Waze: " + alert.get('reportDescription', 'Kontrola prometa'),
                        "vir": "WAZE", "limit": ""
                    })
    except: print("Waze trenutno ni dosegljiv")

    # --- 2. AMZS / DARS (Uradni radarji in dela) ---
    try:
        d_res = requests.get(PROMET_URL, timeout=10)
        d_data = d_res.json()
        for event in d_data.get('contents', []):
            desc = event.get('description', '').lower()
            if any(x in desc for x in ["radar", "meritev", "kontrola"]):
                vsi_radarji.append({
                    "lat": event.get('y'), "lon": event.get('x'),
                    "tip": "RADAR", "icon": "📸", "opis": event.get('description'),
                    "vir": "DARS", "limit": ""
                })
    except: print("Dars trenutno ni dosegljiv")

    # --- 3. RADARBOT GOLD (Tvoj izvoz) ---
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                gold = json.load(f)
                for r in gold:
                    r["vir"] = "RADARBOT GOLD"
                    vsi_radarji.append(r)
        except: print("Napaka pri Radarbot datoteki")

    # --- 4. FIKSNI STACIONARNI (Zeleni) ---
    stacionarni = [
        {"lat": 46.6621, "lon": 16.1612, "tip": "STACIONARNI RADAR", "icon": "📸", "opis": "MS - Lendavska", "vir": "STACIONARNI", "limit": "50"},
        {"lat": 46.5623, "lon": 16.4521, "tip": "STACIONARNI RADAR", "icon": "📸", "opis": "Lendava vstop", "vir": "STACIONARNI", "limit": "50"}
    ]
    vsi_radarji.extend(stacionarni)

    # SHRANJEVANJE
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    posodobi()
