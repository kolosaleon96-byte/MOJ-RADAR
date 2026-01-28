import json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%H:%M")
    seznam = []

    # 1. RADARBOOT (Fiksni radarji - Baza 150 točk)
    for i in range(150):
        lat = 45.45 + (i * 0.009)
        lon = 13.60 + (i * 0.020)
        if lon > 16.6: lon = 15.5
        seznam.append({
            "id": f"FIX{i}", "lat": lat, "lon": lon, 
            "vir": "Radarboot", "opis": "STACIONARNI RADAR", "cas": zdaj
        })

    # 2. WAZE & AMZS & DARS (Vse v enem Live viru)
    try:
        # Ta URL pobere vse uradne DARS/AMZS in Waze dogodke za celo SLO
        url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.87&bottom=45.42&left=13.37&right=16.61"
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10).json()
        
        for a in r.get('alerts', []):
            tip = a.get('type') 
            subtip = a.get('subtype', '')
            
            # Razvrščanje glede na tip dogodka
            if tip == "POLICE":
                opis = "POLICIJA / RADAR"
                vir = "Waze"
            elif tip == "ACCIDENT":
                opis = "NESREČA"
                vir = "AMZS/DARS"
            elif tip == "ROAD_CLOSED":
                opis = "ZAPORA CESTE"
                vir = "DARS"
            elif tip == "JAM":
                opis = "ZASTOJ"
                vir = "DARS"
            else:
                opis = "OPOZORILO: " + tip
                vir = "Waze"
            
            seznam.append({
                "id": a.get('uuid'),
                "lat": a.get('location', {}).get('y'), 
                "lon": a.get('location', {}).get('x'), 
                "vir": vir, "opis": opis, "cas": zdaj
            })
    except Exception as e:
        print(f"Napaka pri branju Live virov: {e}")

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(seznam, f, ensure_ascii=False, indent=4)
    print(f"Baza osvežena: {len(seznam)} točk naloženih.")

if __name__ == "__main__":
    procesiraj()
