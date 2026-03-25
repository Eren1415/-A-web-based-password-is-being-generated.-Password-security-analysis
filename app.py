from flask import Flask, jsonify, request
import random
import string
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Şifre oluşturma
def sifre_olustur(uzunluk=12):
    karakterler = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(karakterler) for _ in range(uzunluk))

# Güç analizi
def sifre_kontrol(sifre):
    guc = 0

    if any(c.islower() for c in sifre):
        guc += 1
    if any(c.isupper() for c in sifre):
        guc += 1
    if any(c.isdigit() for c in sifre):
        guc += 1
    if any(c in "!@#$%^&*()" for c in sifre):
        guc += 1

    if len(sifre) < 8:
        return "Çok Zayıf"
    elif guc <= 2:
        return "Zayıf"
    elif guc == 3:
        return "Orta"
    else:
        return "Güçlü"

# Kırılma süresi hesaplama
def kirilma_suresi(sifre):
    karakter_seti = 0

    if any(c.islower() for c in sifre):
        karakter_seti += 26
    if any(c.isupper() for c in sifre):
        karakter_seti += 26
    if any(c.isdigit() for c in sifre):
        karakter_seti += 10
    if any(c in "!@#$%^&*()" for c in sifre):
        karakter_seti += 10

    kombinasyon = karakter_seti ** len(sifre)

    # saniyede 1 milyar deneme (brute force)
    saniye = kombinasyon / 1_000_000_000

    return saniyeyi_formatla(saniye)

def saniyeyi_formatla(saniye):
    dakika = saniye / 60
    saat = dakika / 60
    gun = saat / 24
    yil = gun / 365

    if yil > 1:
        return f"{int(yil)} yıl"
    elif gun > 1:
        return f"{int(gun)} gün"
    elif saat > 1:
        return f"{int(saat)} saat"
    elif dakika > 1:
        return f"{int(dakika)} dakika"
    else:
        return f"{int(saniye)} saniye"

# Otomatik şifre
@app.route("/sifre")
def sifre():
    yeni = sifre_olustur()
    return jsonify({
        "sifre": yeni,
        "guc": sifre_kontrol(yeni),
        "sure": kirilma_suresi(yeni)
    })

# Kullanıcı şifresi analiz
@app.route("/analiz", methods=["POST"])
def analiz():
    data = request.json
    sifre = data.get("sifre")

    return jsonify({
        "guc": sifre_kontrol(sifre),
        "sure": kirilma_suresi(sifre)
    })

if __name__ == "__main__":
    app.run(debug=True)
    from flask import send_file

    @app.route("/")
    def home():
      return send_file("index.html")