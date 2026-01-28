import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    
    # --- MASIVNA SLOVENSKA BAZA (Radarji, Kamere, DARS, AMZS) ---
    vsi = [
        # PREKMURJE - Detajlno
        {"regija": "Prekmurje", "kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Radar", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Radar", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Radar", "opis": "Radar v naselju", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "Lendava - Kamere", "lat": 46.5622, "lon": 16.4511, "vir": "DARS", "opis": "DARS Nadzorna kamera", "omejitev": "130"},
        {"regija": "Prekmurje", "kraj": "Beltinci center", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook", "opis": "Kontrola (FB)", "omejitev": "50"},
        
        # AVTOCESTE - VSE KAMERE IN NADZOR (DARS)
        {"regija": "AC", "kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722, "vir": "DARS", "opis": "DARS Nadzor (Kamera/Radar)", "omejitev": "130"},
        {"regija": "AC", "kraj": "AC - Lom", "lat": 45.8922, "lon": 14.3511, "vir": "DARS", "opis": "DARS Nadzor / Tehtanje", "omejitev": "130"},
        {"regija": "AC", "kraj": "AC - Golovec", "lat": 46.0382, "lon": 14.5422, "vir": "DARS", "opis": "SEKCIJSKO MERJENJE", "omejitev": "100"},
        {"regija": "AC", "kraj": "AC - Viadukt Črni Kal", "lat": 45.5533, "lon": 13.8811, "vir": "DARS", "opis": "Radar / Močan veter", "omejitev": "100"},
        {"regija": "AC", "kraj": "AC - Lukovica", "lat": 46.1681, "lon": 14.6851, "vir": "DARS", "opis": "DARS kamera - nadzor", "omejitev": "130"},
        {"regija": "AC", "kraj": "AC - Peračica", "lat": 46.3355, "lon": 14.2388, "vir": "DARS", "opis": "DARS kamera / radar", "omejitev": "130"},
        
        # ŠTAJERSKA IN OSTALO
        {"regija": "Maribor", "kraj": "MB - Ptujska", "lat": 46.5385, "lon": 15.6662, "vir": "Radar", "opis": "STACIONARNI RADAR", "omejitev": "70"},
        {"regija": "Maribor", "kraj": "MB - Tržaška", "lat": 46.5355, "lon": 15.6511, "vir": "Radar", "opis": "STACIONARNI RADAR", "omejitev": "70"},
        {"regija": "Celje", "kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711, "vir": "Radar", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        
        # AMZS - Ključna obvestila
        {"regija": "Ljubljana", "kraj": "AMZS Center", "lat": 46.0688, "lon": 14.5122, "vir": "AMZS", "opis": "AMZS: Stanje na cestah", "omejitev": "50"}
    ]

    # --- WAZE INTEGRACIJA (Če dela, doda še več, če ne, baza ostane polna) ---
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        for a in wr.get('alerts', []):
            vsi.append({
                "regija": "Slovenija", "kraj": a.get('street', 'Cesta'),
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Waze Live", "opis": f"WAZE: {a.get('type')}", "omejitev": "Preveri", "cas": zdaj
            })
    except:
        print("Waze trenutno ne odgovarja, uporabljam bogato fiksno bazo.")

    for r in vsi: r["cas"] = zdaj

    # ZAPIS
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"Sistem osvežen: {len(vsi)} točk (Kamere DARS in Radarji vključeni).")

if __name__ == "__main__":
    procesiraj()
