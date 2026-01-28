import requests
import json
import os

# RAZŠIRJENO OBMOČJE (Cela Slovenija + okolica)
WAZE_URL = "https://www.waze.com/rtp-api/web/map/details?bbox=13.0,45.3,16.7,47.0"
PROMET_URL = "https://www.promet.si/dc/traffic.events.public.json"

def posodobi():
    vsi_radarji = []
    # Headers pomagajo, da nas DARS/Waze ne blokirata
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # --- 1. WAZE ---
    try:
        w_res = requests.get(WAZE_URL, headers=headers, timeout=15)
        if w_res.status_code == 200:
            w_data = w_res.json()
            alerts = w_data.get('alerts', [])
            print(f"Waze najdenih dogodkov: {len(alerts)}")
            for alert in alerts:
                if alert.get('type') in ['POLICE', 'ROAD_HAZARD']:
                    vsi_radarji.append({
                        "lat": alert.get('location', {}).get('y'),
                        "lon": alert.get('location', {}).get('x'),
                        "tip": "POLICIJA / RADAR", "icon": "👮",
                        "opis": "Waze: " + alert.get('reportDescription', 'Kontrola prometa'),
                        "vir": "WAZE", "limit": ""
                    })
    except Exception as e:
        print(f"Waze napaka: {e}")

    # --- 2. DARS / AMZS ---
    try:
        # Dodamo headers še tukaj, da preprečimo char 0 napako
        d_res = requests.get(PROMET_URL, headers=headers, timeout=15)
        if d_res.status_code == 200:
            d_data = d_res.json()
            events = d_data.get('contents', [])
            print(f"Dars najdenih dogodkov: {len(events)}")
            for event in events:
                desc = event.get('description', '').lower()
                if any(x in desc for x in ["radar", "meritev", "kontrola", "stacionarni"]):
                    vsi_radarji.append({
                        "lat": event.get('y'), "lon": event.get('x'),
                        "tip": "RADAR", "icon": "📸", "opis": event.get('description'),
                        "vir": "DARS", "limit": ""
                    })
        else:
            print(f"Dars strežnik vrnil kodo: {d_res.status_code}")
    except Exception as e:
        print(f"Dars napaka: {e}")

    # --- 3. RADARBOT GOLD (Če boš naložil datoteko) ---
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                gold_data = json.load(f)
                print(f"Radarbot Gold najdenih: {len(gold_data)}")
                for r in gold_data:
                    r["vir"] = "RADARBOT GOLD"
                    vsi_radarji.append(r)
        except Exception as e:
            print(f"Radarbot Gold napaka: {e}")

    # --- 4. FIKSNI STACIONARNI ---
    stacionarni = [
        {"lat": 46.6621, "lon": 16.1612, "tip": "STACIONARNI RADAR", "icon": "📸", "opis": "MS - Lendavska", "vir": "STACIONARNI", "limit": "50"},
        {"lat": 46.5412, "lon": 16.4632, "tip": "STACIONARNI RADAR", "icon": "📸", "opis": "Lendava vstop", "vir": "STACIONARNI", "limit": "50"}
    ]
    vsi_radarji.extend(stacionarni)

    # SHRANJEVANJE
    print(f"Skupaj shranjenih točk: {len(vsi_radarji)}")
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    posodobi()
