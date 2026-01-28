import requests
import json
import os

def posodobi():
    vsi_radarji = []
    
    # 1. POSKUS WAZE (Slovenija kordinate)
    # Uporabimo "World" strežnik, ki je bolj odprt
    waze_url = "https://www.waze.com/row-rtp-api/web/map/details?bbox=13.2,45.4,16.6,46.9"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.waze.com/"
    }

    try:
        r = requests.get(waze_url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for a in data.get('alerts', []):
                if a.get('type') == 'POLICE':
                    vsi_radarji.append({
                        "lat": a['location']['y'],
                        "lon": a['location']['x'],
                        "tip": "POLICIJA",
                        "icon": "👮",
                        "opis": "Poročano preko Waze",
                        "vir": "WAZE"
                    })
            print(f"Waze: Najdenih {len(vsi_radarji)} policistov.")
    except:
        print("Waze blokada, gremo naprej.")

    # 2. TVOJI FIKSNI RADARJI (Tukaj jih dodajaj ročno ali iz FB)
    fiksni = [
        {"lat": 46.6621, "lon": 16.1612, "tip": "FIKSNI", "icon": "📸", "opis": "MS - Lendavska", "vir": "FIKSNI"},
        {"lat": 46.5412, "lon": 16.4632, "tip": "FIKSNI", "icon": "📸", "opis": "Lendava", "vir": "FIKSNI"},
        {"lat": 46.6502, "lon": 16.1523, "tip": "FIKSNI", "icon": "📸", "opis": "MS - Center", "vir": "FIKSNI"}
    ]
    vsi_radarji.extend(fiksni)

    # 3. DODAJ FB RADARJE (Tukaj boš kasneje dodajal točke, ki jih vidiš na FB)
    # Primer: vsi_radarji.append({"lat": 46.6, "lon": 16.2, "tip": "FB", "icon": "👥", "opis": "Javljeno na FB", "vir": "FB"})

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)
    
    print(f"Končano! Skupaj {len(vsi_radarji)} točk na tvoji mapi.")

if __name__ == "__main__":
    posodobi()
