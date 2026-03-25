# A web based password-is-being-generated.-Password-security-analysis
Web Tabanlı Şifre Oluşturucu ve Güvenlik Analiz Aracı (Gelişmiş Proje)
# **1. Proje Amacı**
Bu proje, kullanıcıların güçlü şifreler oluşturmasını ve mevcut şifrelerinin güvenlik seviyesini analiz etmesini sağlayan web tabanlı bir uygulamadır. Ayrıca brute-force saldırılarına karşı tahmini kırılma süresi hesaplaması yapmaktadır.
# **2. Proje Özellikleri**
\- Rastgele şifre oluşturma\
\- Şifre güvenlik analizi\
\- Kırılma süresi tahmini\
\- Kullanıcı şifresi analizi\
\- Web tabanlı kullanım
# **3. Kullanılan Teknolojiler**
Backend: Python (Flask)\
Frontend: HTML, JavaScript\
Kütüphaneler: flask, flask-cors
# **4. Backend Kodu**
Kodlar kullanıcı tarafından sağlanmıştır (app.py).

```python
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


```


# **5. Frontend Kodu**
Kodlar kullanıcı tarafından sağlanmıştır (index.html).

```html

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Şifre Güvenlik Aracı</title>
</head>
<body>

<h2>🔐 Şifre Oluşturucu</h2>
<button onclick="olustur()">Şifre Oluştur</button>

<p><b>Şifre:</b> <span id="sifre"></span></p>
<p><b>Güç:</b> <span id="guc"></span></p>
<p><b>Kırılma Süresi:</b> <span id="sure"></span></p>

<hr>

<h2>🎯 Şifre Analizi</h2>

<input type="text" id="kullaniciSifre" placeholder="Şifreni gir">
<button onclick="analiz()">Analiz Et</button>

<p><b>Güç:</b> <span id="analizGuc"></span></p>
<p><b>Kırılma Süresi:</b> <span id="analizSure"></span></p>

<script>
function olustur() {
    fetch("http://127.0.0.1:5000/sifre")
    .then(res => res.json())
    .then(data => {
        document.getElementById("sifre").innerText = data.sifre;
        document.getElementById("guc").innerText = data.guc;
        document.getElementById("sure").innerText = data.sure;
    });
}

function analiz() {
    let sifre = document.getElementById("kullaniciSifre").value;

    fetch("http://127.0.0.1:5000/analiz", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ sifre: sifre })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("analizGuc").innerText = data.guc;
        document.getElementById("analizSure").innerText = data.sure;
    });
}
</script>

</body>
</html>

```




