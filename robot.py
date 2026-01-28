import json
import os

def posodobi():
    # Osnovni fiksni radarji
    vsi_radarji = [
        {"lat": 46.6621, "lon": 16.1612, "tip": "FIKSNI", "icon": "📸", "opis": "MS Center", "vir": "FIKSNI"},
        {"lat": 46.5412, "lon": 16.4632, "tip": "FIKSNI", "icon": "📸", "opis": "Lendava", "vir": "FIKSNI"}
    ]

    # Dodaj še Radarbot Gold, če obstaja datoteka
    if os.path.exists('radarbot_gold.json'):
        try:
            with open('radarbot_gold.json', 'r', encoding='utf-8') as f:
                vsi_radarji.extend(json.load(f))
        except: pass

    with open('radarji.json', 'w', encoding='utf-8') as f:
        json.dump(vsi_radarji, f, indent=2, ensure_ascii=False)
    print(f"Robot osvežil bazo. Skupaj točk: {len(vsi_radarji)}")

if __name__ == "__main__":
    posodobi()
