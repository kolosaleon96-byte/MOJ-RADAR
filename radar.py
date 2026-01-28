import os, json, requests
from datetime import datetime

def procesiraj():
    zdaj = datetime.now().strftime("%d.%m.%Y ob %H:%M")
    
    # 1. VIR: STACIONARNI RADARJI (Radarbot & Fiksni)
    stacionarni = [
        {"regija": "Prekmurje", "kraj": "MS - Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "MS - Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "MS - Panonska", "lat": 46.6555, "lon": 16.1711, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "Prekmurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "50"},
        {"regija": "LJ", "kraj": "LJ - Celovška", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "60"},
        {"regija": "MB", "kraj": "MB - Ptujska", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot", "opis": "STACIONARNI RADAR", "omejitev": "70"}
    ]

    # 2. VIR: FACEBOOK LOKACIJE (Detajlno Pomurje)
    facebook_viri = [
        {"regija": "Pomurje", "kraj": "Beltinci", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook", "opis": "Kontrola prometa (FB)", "omejitev": "50"},
        {"regija": "Pomurje", "kraj": "Ljutomer", "lat": 46.5181, "lon": 16.1975, "vir": "Facebook", "opis": "Poročilo s terena (FB)", "omejitev": "50"},
        {"regija": "Pomurje", "kraj": "Radenci", "lat": 46.6433, "lon": 16.0422, "vir": "Facebook", "opis": "Merjenje hitrosti (FB)", "omejitev": "50"},
        {"regija": "Pomurje", "kraj": "Murska Sobota - Center", "lat": 46.658, "lon": 16.162, "vir": "Facebook", "opis": "Aktivna kontrola (FB)", "omejitev": "50"}
    ]

    koncni_seznam = []

    # Združevanje vseh virov v eno glavno tabelo
    for r in stacionarni:
        r["cas"] = zdaj
        koncni_seznam.append(r)

    for f in facebook_viri:
        f["cas"] = zdaj
        koncni_seznam.append(f)

    # 3. VIR: WAZE & AMZS (Živi podatki)
    try:
        w_res = requests.get("https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        for a in w_res.get('alerts', []):
            koncni_seznam.append({
                "regija": "Slovenija", "kraj": a.get('street', 'Cesta'),
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Waze Live", "opis": f"V ŽIVO: {a.get('type')}", "omejitev": "Preveri", "cas": zdaj
            })
    except: pass

    # DODAJANJE AMZS ROČNO, ČE JE KAJ NOVEGA
    try:
        r_amzs = requests.get("https://www.amzs.si/na-poti/stanje-na-cestah", timeout=5)
        if "radar" in r_amzs.text.lower():
            koncni_seznam.append({"regija": "Slovenija", "kraj": "AMZS Radar", "lat": 46.12, "lon": 14.82, "vir": "AMZS", "opis": "AMZS: Meritve hitrosti!", "omejitev": "-", "cas": zdaj})
    except: pass

    # SHRANJEVANJE
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(koncni_seznam, f, ensure_ascii=False, indent=4)
    
    print(f"SISTEM POPRAVLJEN: Naloženih {len(koncni_seznam)} točk iz vseh virov.")

if __name__ == "__main__":
    procesiraj()
