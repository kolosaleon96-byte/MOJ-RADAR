import requests
import json
import os
import urllib3

# Izklopimo opozorila za varnostne certifikate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WAZE_URL = "https://www.waze.com/rtp-api/web/map/details?bbox=13.0,45.3,16.7,47.0"
PROMET_URL = "https://www.promet.si/dc/traffic.events.public.json"

def posodobi():
    vsi_radarji = []
    
    # Ustvarimo sejo, ki si zapomni piškotke (kot pravi brskalnik)
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'sl-SI,sl;q=0.9,en-GB;q=0.8,en;q=0.7',
        'Referer': 'https://www.promet.si/'
    })

    # --- 1. WAZE ---
    try:
        w_res = session.get(WAZE_URL, timeout=20, verify=False)
        if w_res.status_code == 200:
            alerts = w_res.json().get('alerts', [])
            w_count = 0
            for a in alerts:
                if a.get('type') in ['POLICE', 'ROAD_HAZARD']:
                    vsi_radarji.append({
                        "lat": a['location']['y'], "lon": a['location']['x'],
                        "tip": "WAZE: " + a.get('subtype', 'POLICIJA'),
                        "icon": "👮", "opis": a.get('reportDescription', 'Mobilni radar'),
                        "vir": "WAZE"
                    })
                    w_count += 1
            print(f"Waze: najdenih {w_count} točk")
    except Exception as e:
        print(f"Waze napaka: {e}")

    # --- 2. DARS / AMZS ---
    try:
        d_res = session.get(PROMET_URL, timeout=20, verify=False)
        if d_res.status_code == 200:
            events = d_res.json().get('contents', [])
            d_count = 0
            for e in events:
                desc = e.get('description', '').lower()
                if any(x in desc for x in ["radar", "meritev", "kontrola"]):
                    vsi_radarji.append({
                        "lat": e['y'], "lon": e['x'],
                        "tip": "DARS RADAR", "icon": "📸",
                        "opis": e.get('description'), "vir": "DARS"
                    })
                    d_count += 1
            print(f"Dars: najdenih {d_count} točk")
        else:
            print(f"Dars še vedno blokira (Koda: {d_res.status_code})")
    except Exception as e:
        print(f"Dars napaka: {e}")

    # --- 3. RADARBOT GOLD & FIKSNI ---
    # Dodamo tvoja dva fiksna radarja, da bosta vedno tam
    vsi_radarji.append({"lat": 46.6621, "lon": 16.1612, "tip": "FIKSNI", "icon": "📸", "opis": "MS Center", "vir": "FIKSNI"})
    vsi_radarji.append({"lat": 46.5412, "lon": 16.4632, "tip": "FIKSNI", "icon": "📸", "opis": "Lendava", "vir": "FIKSNI"})

    # Če imaš datoteko radarbot_gold.json, jo dodamo
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                vsi_radarji.extend(json.load(f))
        except: pass

    # SHRANJEVANJE
    print(f"Skupaj v bazi: {len(vsi_radarji)}")
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    posodobi()
