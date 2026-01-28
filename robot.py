import requests
import json
import os

def posodobi():
    vsi_radarji = []
    
    # POSKUS 1: Svetovni Waze strežnik (včasih manj blokiran)
    WAZE_URL = "https://www.waze.com/row-rtp-api/web/map/details?bbox=13.0,45.3,16.7,47.0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
    }

    try:
        # Dodamo par parametrov, ki jih uporablja prava Waze aplikacija
        params = {
            "cities": "true",
            "intersections": "true",
            "alerts": "true"
        }
        r = requests.get(WAZE_URL, headers=headers, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            alerts = data.get('alerts', [])
            for a in alerts:
                if a.get('type') in ['POLICE', 'ROAD_HAZARD']:
                    vsi_radarji.append({
                        "lat": a['location']['y'], "lon": a['location']['x'],
                        "tip": "WAZE: " + a.get('subtype', 'POLICIJA'),
                        "icon": "👮", "opis": a.get('reportDescription', 'Mobilni radar'),
                        "vir": "WAZE"
                    })
            print(f"Waze uspeh! Najdenih: {len(vsi_radarji)}")
    except Exception as e:
        print(f"Waze blokiran: {e}")

    # FIKSNI (Tvoji osebni)
    vsi_radarji.append({"lat": 46.6621, "lon": 16.1612, "tip": "FIKSNI", "icon": "📸", "opis": "MS Center", "vir": "FIKSNI"})
    vsi_radarji.append({"lat": 46.5412, "lon": 16.4632, "tip": "FIKSNI", "icon": "📸", "opis": "Lendava", "vir": "FIKSNI"})

    # Če imaš datoteko radarbot_gold.json, jo dodamo
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                vsi_radarji.extend(json.load(f))
        except: pass

    # SHRANJEVANJE
    print(f"Končni izplen: {len(vsi_radarji)} točk v bazi.")
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    posodobi()
