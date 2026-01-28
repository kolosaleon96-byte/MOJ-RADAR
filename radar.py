import pyotp
import os
import time
import random
import requests
from geopy.geocoders import Nominatim

# 1. Seznam tvojih 14 skupin s pripadajočimi regijami
SKUPINE = {
    "1": {"ime": "Pomurje", "url": "https://www.facebook.com/share/g/1Di1VxZsWT/"},
    "2": {"ime": "Goričko", "url": "https://www.facebook.com/share/g/1HF9irCSKM/"},
    "3": {"ime": "Prlekija", "url": "https://www.facebook.com/share/g/1AoFw43FAo/"},
    "4": {"ime": "Štajerska", "url": "https://www.facebook.com/share/g/1AG6ngSA7S/"},
    "5": {"ime": "Kolpa-Ljubljana", "url": "https://www.facebook.com/share/g/14VAAgZQTSM/"},
    "6": {"ime": "Ptuj in okolica", "url": "https://www.facebook.com/share/g/1FzLgWDd56/"},
    "7": {"ime": "Ljubljana", "url": "https://www.facebook.com/share/g/1AX5CApbYY/"},
    "8": {"ime": "Avtoceste", "url": "https://www.facebook.com/share/g/1AcsLDZkMf/"},
    "9": {"ime": "Maribor", "url": "https://www.facebook.com/share/g/1GEuSgMZFp/"},
    "10": {"ime": "Majšperk", "url": "https://www.facebook.com/share/g/14RhQ9s9VGt/"},
    "11": {"ime": "Ptuj Radarji", "url": "https://www.facebook.com/share/g/1AULetVBhF/"},
    "12": {"ime": "Ribnica-Kočevje", "url": "https://www.facebook.com/share/g/17kbN7tFwc/"},
    "13": {"ime": "Kranj", "url": "https://www.facebook.com/share/g/14TpDav7nez/"},
    "14": {"ime": "Postojna", "url": "https://www.facebook.com/share/g/1BzHQcBFnc/"}
}

geolocator = Nominatim(user_agent="radar_slovenija_bot")

def najdi_gps_koordinate(besedilo):
    """Robot samodejno poišče kraj v Sloveniji in vrne GPS."""
    for beseda in besedilo.split():
        # Iščemo besede z veliko začetnico (npr. Vaneča, Maribor)
        if beseda[0].isupper() and len(beseda) > 3:
            try:
                lokacija = geolocator.geocode(beseda + ", Slovenia")
                if lokacija:
                    return beseda, lokacija.latitude, lokacija.longitude
            except:
                continue
    return None, None, None

def procesiraj_radarje():
    # Pridobivanje podatkov iz GitHub Secrets
    email = os.getenv('FB_EMAIL')
    geslo = os.getenv('FB_PASS')
    key_2fa = os.getenv('FB_2FA_KEY')

    if not key_2fa:
        print("NAPAKA: FB_2FA_KEY manjka v Secrets!")
        return

    # Generiranje 2FA kode
    totp = pyotp.TOTP(key_2fa.replace(" ", ""))
    print(f"--- ZAGON ROBOTA ---")
    print(f"Uporabnik: {email}")
    print(f"Trenutna 2FA koda za vstop: {totp.now()}")
    print("--------------------")

    # Robot gre skozi vseh 14 skupin
    for id_sk, podatki in SKUPINE.items():
        print(f"Preverjam regijo: {podatki['ime']}...")
        
        # Tukaj robot dejansko 'prebere' zadnjo objavo (simulacija za test)
        # V pravi verziji tukaj requests pobere tekst iz FB
        testna_objave = {
            "1": "Policijska kontrola Vaneča pri pokopališču",
            "7": "Radar na Dunajski cesti v Ljubljani",
            "14": "Kontrola prometa Postojna"
        }
        
        tekst = testna_objave.get(id_sk, "")
        if tekst:
            kraj, lat, lon = najdi_gps_koordinate(tekst)
            if kraj:
                print(f" [!] NAJDENO: {kraj} | GPS: {lat}, {lon}")
                print(f" [!] Objava: {tekst}")
        
        # Premor, da nas FB ne zazna kot napad
        time.sleep(random.randint(2, 4))

    print("--- PREGLED ZAKLJUČEN ---")

if __name__ == "__main__":
    procesiraj_radarje()
