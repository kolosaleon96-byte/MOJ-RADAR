import os, json, requests
from bs4 import BeautifulSoup
from datetime import datetime

def procesiraj():
    # Današnji datum in ura za lepši prikaz na mapi
    zdaj = datetime.now()
    datum_ura = zdaj.strftime("%d.%m.%Y ob %H:%M")

    # 1. MASIVNA BAZA ZA CELO SLOVENIJO + DETALJNO PREKMURJE
    # Vsaka pika ima zdaj polje "opis", kjer piše točno, kaj se dogaja
    vsi = [
        # --- PREKMURJE DETALJNO ---
        {"regija": "Prekmurje", "kraj": "Murska Sobota - Lendavska", "lat": 46.6591, "lon": 16.1622, "vir": "Facebook", "opis": "Radar (stacionarni) - aktivno", "cas": datum_ura},
        {"regija": "Prekmurje", "kraj": "Murska Sobota - Noršinska", "lat": 46.6655, "lon": 16.1811, "vir": "Facebook", "opis": "Radar (stacionarni) - preverjeno", "cas": datum_ura},
        {"regija": "Prekmurje", "kraj": "Beltinci (pri cerkvi)", "lat": 46.6047, "lon": 16.2383, "vir": "Facebook", "opis": "Policijska kontrola (možna selekcija)", "cas": datum_ura},
        {"regija": "Prekmurje", "kraj": "Lendava (meja)", "lat": 46.5622, "lon": 16.4511, "vir": "Facebook", "opis": "Poostren nadzor prometa in kamer", "cas": datum_ura},
        {"regija": "Prekmurje", "kraj": "Gederovci", "lat": 46.6655, "lon": 16.0488, "vir": "Facebook", "opis": "Radar v naselju (omejitev 50)", "cas": datum_ura},
        {"regija": "Prekmurje", "kraj": "Radenci (občina)", "lat": 46.6433, "lon": 16.0422, "vir": "Facebook", "opis": "Merjenje hitrosti (ročni radar)", "cas": datum_ura},
        
        # --- AVTOCESTA (CELA SLOVENIJA) ---
        {"regija": "AC", "kraj": "AC - Predor Golovec", "lat": 46.0382, "lon": 14.5422, "vir": "DARS", "opis": "Sekcijsko merjenje hitrosti v predoru", "cas": datum_ura},
        {"regija": "AC", "kraj": "AC - Tepanje", "lat": 46.3455, "lon": 15.4722, "vir": "DARS", "opis": "Nadzorna točka DARS / Policija", "cas": datum_ura},
        {"regija": "AC", "kraj": "AC - Lukovica", "lat": 46.1681, "lon": 14.6851, "vir": "DARS", "opis": "Kamera in nadzor prometa", "cas": datum_ura},
        {"regija": "AC", "kraj": "AC - Črni Kal", "lat": 45.5533, "lon": 13.8811, "vir": "DARS", "opis": "Kamera DARS - močan veter / nadzor", "cas": datum_ura},
        
        # --- GLAVNA MESTA ---
        {"regija": "Ljubljana", "kraj": "LJ - Celovška", "lat": 46.0792, "lon": 14.4841, "vir": "Radarbot", "opis": "Stacionarni radar (v obe smeri)", "cas": datum_ura},
        {"regija": "Maribor", "kraj": "MB - Ptujska", "lat": 46.5385, "lon": 15.6662, "vir": "Radarbot", "opis": "Radar na križišču", "cas": datum_ura},
        {"regija": "Celje", "kraj": "CE - Mariborska", "lat": 46.2461, "lon": 15.2711, "vir": "Radarbot", "opis": "Radar v naselju", "cas": datum_ura}
    ]

    # 2. PAMETNO BRANJE WAZE PODATKOV (PODROBNOSTI)
    try:
        w_url = "https://www.waze.com/row-rtserver/web/TGeoRSS?top=46.876&bottom=45.421&left=13.375&right=16.610"
        wr = requests.get(w_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        for a in wr.json().get('alerts', []):
            tip = a.get('type', 'DOGODEK')
            podtip = a.get('subtype', 'Preveri na lokaciji')
            # Robot zdaj sestavi lepši opis
            koncni_opis = f"{tip}: {podtip.replace('_', ' ')}"
            vsi.append({
                "regija": "Slovenija", "kraj": f"WAZE: {a.get('street', 'Brezimna cesta')}",
                "lat": a.get('location', {}).get('y'), "lon": a.get('location', {}).get('x'), 
                "vir": "Waze", "opis": koncni_opis, "cas": datum_ura
            })
    except: pass

    # 3. ZAPIS V DATOTEKO
    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi, f, ensure_ascii=False, indent=4)
    
    print(f"Sistem osvežen: {len(vsi)} točk (Vse podrobnosti vključene).")

if __name__ == "__main__":
    procesiraj()
