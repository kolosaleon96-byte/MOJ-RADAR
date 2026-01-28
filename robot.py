import requests
import json

def posodobi():
    # Uporabimo najbolj osnoven klic, kot ga uporablja brskalnik
    url = "https://www.waze.com/rtp-api/web/map/details?bbox=13.0,45.0,16.5,47.0"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        vsi = []
        for a in data.get('alerts', []):
            if a.get('type') == 'POLICE':
                vsi.append({"lat": a['location']['y'], "lon": a['location']['x'], "tip": "POLICIJA", "icon": "👮"})
        
        # DODAMO ŠE TVOJE ROČNE
        vsi.append({"lat": 46.6621, "lon": 16.1612, "tip": "FIKSNI", "icon": "📸", "opis": "MS"})
        
        with open('radarji.json', 'w') as f:
            json.dump(vsi, f)
        print(f"Uspeh! Najdenih {len(vsi)} točk.")
    except:
        print("Waze spet blokira.")

if __name__ == "__main__":
    posodobi()
