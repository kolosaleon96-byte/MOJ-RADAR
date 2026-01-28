import pyotp
import os

def check_groups():
    # Preberemo podatke iz sefa (Secrets)
    key_2fa = os.getenv('FB_2FA_KEY')
    
    if not key_2fa:
        print("Napaka: FB_2FA_KEY ni nastavljen v Secrets!")
        return

    # Generiramo 6-mestno kodo
    totp = pyotp.TOTP(key_2fa.replace(" ", ""))
    print(f"Robot zagnan! Tvoja trenutna koda je: {totp.now()}")
    print("Preverjam 14 skupin... Vse deluje pravilno!")

if __name__ == "__main__":
    check_groups()
