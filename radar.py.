import os
import pyotp

# Robot vzame podatke iz tvojega GitHub sefa
email = os.environ.get('FB_EMAIL')
password = os.environ.get('FB_PASS')
key_2fa = os.environ.get('FB_2FA_KEY')

def generiraj_kodo():
# To ustvari 6-mestno kodo za Facebook prijavo
if not key_2fa:
return "Ključ ni najden!"
totp = pyotp.TOTP(key_2fa.replace(" ", ""))
return totp.now()

print(f"Robot pripravljen za: {email}")
print(f"Trenutna koda za Facebook vstop: {generiraj_kodo()}")
