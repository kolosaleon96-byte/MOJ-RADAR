import requests
import json
import os
import time

# Koordinate za celo Slovenijo
WAZE_URL = "https://www.waze.com/rtp-api/web/map/details?bbox=13.0,45.3,16.7,47.0"
PROMET_URL = "https://www.promet.si/dc/traffic.events.public.json"

def posodobi():
    vsi_radarji = []
    
    # Še močnejši Headers, da izgledamo kot pravi Chrome brskalnik
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'sl-SI,sl;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Referer': 'https://www.promet.si/'
    }

    # --- 1. WAZE (Dodano več preverjanja) ---
    try:
        w_res = requests.get(WAZE_URL, headers=headers, timeout=20)
        if w_res.status_code == 200:
            w_data = w_res.json()
            alerts = w_data.get('alerts', [])
            w_count = 0
            for alert in alerts:
                # Iščemo policijo in nevarnosti (vsebuje radarje)
                if alert.get('type') in ['POLICE', 'ROAD_HAZARD']:
                    vsi_radarji.append({
                        "lat": alert.get('location', {}).get('y'),
                        "lon": alert.get('location', {}).get('x'),
                        "tip": "WAZE: " + alert.get('subtype', 'POLICIJA'), 
                        "icon": "👮",
                        "opis": alert.get('reportDescription', 'Mobilna kontrola'),
                        "vir": "WAZE"
                    })
                    w_count += 1
            print(f"Waze najdenih radarjev: {w_count}")
    except Exception as e:
        print(f"Waze napaka: {e}")

    # --- 2. DARS / AMZS (Reševanje kode 403) ---
    try:
        # Počakamo 2 sekundi med klici, da ne izgledamo prehitri
        time.sleep(2)
        d_res = requests.get(PROMET_URL, headers=headers, timeout=20)
        if d_res.status_code == 200:
            d_data = d_res.json()
            events = d_data.get('contents', [])
            d_count = 0
            for event in events:
                desc = event.get('description', '').lower()
                if any(x in desc for x in ["radar", "meritev", "kontrola"]):
                    vsi_radarji.append({
                        "lat": event.get('y'), "lon": event.get('x'),
                        "tip": "DARS RADAR", "icon": "📸", 
                        "opis": event.get('description'),
                        "vir": "DARS"
                    })
                    d_count += 1
            print(f"Dars najdenih radarjev: {d_count}")
        else:
            print(f"Dars še vedno blokira (Koda: {d_res.status_code})")
    except Exception as e:
        print(f"Dars napaka: {e}")

    # --- 3. RADARBOT GOLD (Iz tvoje datoteke) ---
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                gold_data = json.load(f)
                print(f"Radarbot Gold naloženih: {len(gold_data)}")
                for r in gold_data:
                    vsi_radarji.append(r)
        except: pass

    # --- 4. FIKSNI (Tvoji osebni) ---
    vsi_radarji.append({"lat": 46.6621, "lon": 16.1612, "tip": "STACIONARNI", "icon": "📸", "opis": "MS Center", "vir": "FIKSNI"})
    vsi_radarji.append({"lat": 46.5412, "lon": 16.4632, "tip": "STACIONARNI", "icon": "📸", "opis": "Lendava", "vir": "FIKSNI"})

    # SHRANJEVANJE
    print(f"Skupaj v bazi: {len(vsi_radarji)}")
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    posodobi()
