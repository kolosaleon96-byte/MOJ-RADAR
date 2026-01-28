import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    
    # 1. TVOJA MASIVNA BAZA (Vpisana tako, da je robot NE MORE spregledati)
    vsi = [
        # --- PREKMURJE DETALJNO ---
        {"regija": "Prekmurje", "kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Facebook", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Facebook", "opis": "STACIONARNI RADAR", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Beltinci center", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook", "opis": "Kontrola prometa", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Facebook", "opis": "Radar v naselju", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Ljutomer center", "lat": 46.5181, "lon": 16.1975, "vir": "Facebook", "opis": "Možna kontrola", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Radenci", "lat": 46.6433, "lon": 16.0422, "vir": "Facebook", "opis": "Merjenje hitrosti", "omejitev": "50 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Lendava obvoznica", "lat": 46.5622, "lon": 16.4511, "vir": "Facebook", "opis": "Radar / Kamere", "omejitev": "70 km/h", "cas": zdaj},
        {"regija": "Prekmurje", "kraj": "Črenšovci", "lat": 46.5711, "lon": 16.2888, "vir": "Facebook", "opis": "Kontrola", "omejitev": "50 km/h", "cas": zdaj},
        
        # --- CELA SLOVENIJA & AVTOCESTE ---
        {"regija": "AC", "kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722, "vir": "DARS", "opis": "Nadzorna točka", "omejitev": "130 km/h", "cas": zdaj},
        {"regija": "AC", "kraj": "AC - Golovec", "lat": 46.0382, "lon": 14.5422, "vir": "DARS", "opis": "Sekcijsko merjenje", "omejitev": "100 km/h", "cas": zdaj},
        {"regija": "AC", "kraj": "AC - Črni Kal", "lat": 45.5533, "lon": 13.8811, "vir": "DARS", "opis": "Kamera / Nadzor", "omejitev": "100 km/h", "cas": zdaj},
        {"regija": "AC", "kraj": "AC - Lukovica", "lat": 46.1681, "lon": 14.6851, "vir": "DARS", "opis": "Nadzor prometa", "omejitev": "130 km/h", "cas": zdaj},
        {"regija": "Ljubljana", "kraj": "Celovška cesta", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot", "opis": "Stacionarni radar", "omejitev": "60 km/h", "cas": zdaj},
        {"regija": "Maribor", "kraj": "Ptujska cesta", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot", "opis": "Radar na križišču", "omejitev": "70 km/h", "cas": zdaj},
        {"regija": "Celje", "kraj": "Mariborska", "lat": 46.2461, "lon": 15.2711, "vir": "Radarbot", "opis": "Radar", "omejitev": "50 km/h", "cas": zdaj}
    ]

    # 2. DODAJANJE WAZE PODATKOV (Z zaščito pred napako)
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if wr.status_code == 200:
            for a in wr.json().get('alerts', []):
                vsi.append({
                    "regija": "Waze Live", "kraj": f"WAZE: {a.get('street', 'Cesta')}",
                    "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                    "vir": "Waze", "opis": a.get('subtype', 'Radar'), "omejitev": "Preveri", "cas": zdaj
                })
    except:
        print("Waze trenutno ni dostopen, uporabljam samo fiksno bazo.")

    # 3. KONČNI ZAPIS
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"USPEH! Sistem osvežen: {len(vsi)} točk naloženih.")

if __name__ == "__main__":
    procesiraj()
