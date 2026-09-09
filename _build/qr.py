# -*- coding: utf-8 -*-
"""Genera los materiales imprimibles del QR en dml-redes/qr/:
     qr-dml-redes.png   QR de alta resolucion con el isotipo al centro
     qr-dml-redes.svg   el mismo QR en vector (para imprenta)
     cartel-qr.png      cartel 1080x1350 con la marca DML, listo para imprimir o publicar
   Uso:  python _build/qr.py
"""
import base64, io, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B   # reutiliza URL, fuente() y logo()

from PIL import Image
import segno

QR_DIR = os.path.join(B.BASE, 'qr')
CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
TINTA  = '#012234'


def qr_png(destino, lado=1400):
    """QR con correccion alta ('h') y el isotipo DML al centro."""
    qr = segno.make(B.URL, error='h')
    buf = io.BytesIO()
    qr.save(buf, kind='png', scale=20, border=4, dark=TINTA, light='#FFFFFF')
    im = Image.open(buf).convert('RGBA').resize((lado, lado), Image.LANCZOS)

    # isotipo a color sobre pastilla blanca (~20% del area: seguro con error='h')
    marca = Image.open(os.path.join(B.MARCA, 'logo-dml-color.png')).convert('RGBA')
    izq = marca.crop((0, 0, int(marca.width * 0.42), marca.height))
    izq = izq.crop(izq.split()[3].getbbox())
    m = round(lado * 0.155)
    izq = izq.resize((m, max(1, round(izq.height * m / izq.width))), Image.LANCZOS)

    pad = round(lado * 0.028)
    caja = Image.new('RGBA', (izq.width + pad * 2, izq.height + pad * 2), (255, 255, 255, 255))
    caja.paste(izq, (pad, pad), izq)
    im.alpha_composite(caja, ((lado - caja.width) // 2, (lado - caja.height) // 2))

    im.convert('RGB').save(destino, 'PNG', optimize=True)
    return destino


def qr_svg(destino):
    with open(destino, 'wb') as f:
        segno.make(B.URL, error='h').save(f, kind='svg', scale=10, border=4,
                                          dark=TINTA, light='#FFFFFF')
    return destino


CARTEL = """<!doctype html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Neurial';font-weight:400;src:url(data:font/woff2;base64,{reg}) format('woff2')}}
@font-face{{font-family:'Neurial';font-weight:500;src:url(data:font/woff2;base64,{med}) format('woff2')}}
@font-face{{font-family:'Neurial';font-weight:800;src:url(data:font/woff2;base64,{xb}) format('woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:'Neurial',sans-serif;color:#fff;overflow:hidden;
  background:radial-gradient(120% 70% at 50% -8%,rgba(92,224,229,.32) 0%,rgba(92,224,229,0) 58%),
             linear-gradient(163deg,#012234 0%,#013F5E 24%,#00577F 50%,#0A7396 74%,#03A6A6 100%);
  position:relative;display:flex;flex-direction:column;align-items:center;
  padding:74px 70px 62px;text-align:center}}
.malla{{position:absolute;inset:0;opacity:.09;
  background-image:linear-gradient(rgba(255,255,255,.8) 2px,transparent 2px),
                   linear-gradient(90deg,rgba(255,255,255,.8) 2px,transparent 2px);
  background-size:112px 112px;
  -webkit-mask-image:radial-gradient(72% 58% at 50% 36%,#000 0%,transparent 78%)}}
.vineta{{position:absolute;inset:0;background:radial-gradient(112% 92% at 50% 44%,transparent 46%,rgba(1,26,42,.55) 100%)}}
.orbe{{position:absolute;border-radius:50%;filter:blur(110px)}}
.o1{{width:520px;height:520px;top:-170px;left:-190px;background:rgba(92,224,229,.5)}}
.o2{{width:480px;height:480px;bottom:-180px;right:-170px;background:rgba(3,166,166,.5)}}
.z{{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;width:100%;height:100%}}
.logo{{width:400px;filter:drop-shadow(0 8px 30px rgba(1,26,42,.5))}}
.regla{{width:96px;height:6px;border-radius:6px;margin:38px 0 26px;
  background:linear-gradient(90deg,#5CE0E5,#03A6A6)}}
h1{{font-size:104px;font-weight:800;letter-spacing:-.025em;line-height:.92;text-transform:uppercase}}
h1 em{{font-style:normal;color:#5CE0E5}}
.sub{{margin-top:22px;font-size:30px;font-weight:500;line-height:1.4;color:rgba(255,255,255,.94);max-width:26em}}
.marco{{margin-top:40px;margin-bottom:40px;padding:30px;border-radius:44px;background:#fff;
  box-shadow:0 34px 80px rgba(1,26,42,.5),0 0 0 3px rgba(92,224,229,.55)}}
.marco img{{display:block;width:430px;height:430px}}
.pie{{margin-top:auto;width:100%}}
.redes{{display:flex;justify-content:center;gap:34px;margin-bottom:30px}}
.red{{display:flex;flex-direction:column;align-items:center;gap:11px}}
.red span{{width:80px;height:80px;border-radius:26px;display:grid;place-items:center;
  box-shadow:0 10px 26px rgba(1,26,42,.4),inset 0 2px 0 rgba(255,255,255,.28)}}
.red svg{{width:44px;height:44px;fill:#fff}}
.red b{{font-size:19px;font-weight:500;color:rgba(207,255,255,.9)}}
.ig{{background:radial-gradient(120% 120% at 28% 108%,#FDCB5C,#F58529 22%,#DD2A7B 52%,#8134AF 78%,#515BD4)}}
.fb{{background:linear-gradient(180deg,#3B8CFF,#1877F2)}}
.tk{{background:linear-gradient(150deg,#2A2A33,#0B0B10)}}
.yt{{background:linear-gradient(180deg,#FF3B3B,#E00000)}}
.wa{{background:linear-gradient(180deg,#3FE07C,#20BA5A)}}
.web{{font-size:30px;font-weight:800;letter-spacing:.06em;color:#5CE0E5}}
</style></head><body>
<div class="malla"></div><div class="vineta"></div>
<div class="orbe o1"></div><div class="orbe o2"></div>
<div class="z">
  <img class="logo" src="data:image/png;base64,{logo}" alt="DML Médica">
  <div class="regla"></div>
  <h1>Síguenos<br><em>en redes</em></h1>
  <p class="sub">Escanea el código con la cámara de tu celular</p>
  <div class="marco"><img src="data:image/png;base64,{qr}" alt="QR"></div>
  <div class="pie">
    <div class="redes">
      <div class="red"><span class="ig"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="5.6" fill="none"/><circle cx="12" cy="12" r="4.4" fill="none"/><circle cx="17.4" cy="6.6" r="1.35" fill="#fff" stroke="none"/></svg></span><b>@dmlmedica</b></div>
      <div class="red"><span class="fb"><svg viewBox="0 0 24 24"><path d="M13.6 22v-8.2h2.8l.42-3.2H13.6V8.5c0-.93.26-1.56 1.59-1.56h1.7V4.08A22.7 22.7 0 0 0 14.42 4c-2.46 0-4.14 1.5-4.14 4.26v2.34H7.5v3.2h2.78V22z"/></svg></span><b>DML Médica</b></div>
      <div class="red"><span class="tk"><svg viewBox="0 0 24 24"><path d="M16.9 2h-3.1v13.2a2.6 2.6 0 1 1-2.6-2.6c.24 0 .47.03.69.1v-3.2a5.9 5.9 0 0 0-.69-.04 5.77 5.77 0 1 0 5.77 5.77V9.06A7.2 7.2 0 0 0 21.3 10.4V7.28a4.1 4.1 0 0 1-2.9-1.2A4.35 4.35 0 0 1 16.9 2z"/></svg></span><b>@dml_medica</b></div>
      <div class="red"><span class="yt"><svg viewBox="0 0 24 24"><path fill-rule="evenodd" d="M21.6 7.2a2.5 2.5 0 0 0-1.76-1.77C18.27 5 12 5 12 5s-6.27 0-7.84.43A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.76 1.77C5.73 19 12 19 12 19s6.27 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10.1 15.02 15.3 12l-5.2-3.02z"/></svg></span><b>DML Médica</b></div>
      <div class="red"><span class="wa"><svg viewBox="0 0 24 24"><path d="M12.04 2.4a9.5 9.5 0 0 0-8.2 14.28L2.4 21.6l5.05-1.4A9.5 9.5 0 1 0 12.04 2.4zm0 1.72a7.79 7.79 0 1 1-3.98 14.48l-.28-.17-2.98.82.8-2.9-.19-.3A7.79 7.79 0 0 1 12.04 4.12zm-3.5 3.9c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1s.9 2.43 1.03 2.6c.13.16 1.75 2.78 4.32 3.79 2.13.84 2.57.67 3.03.63.46-.04 1.49-.6 1.7-1.19.21-.58.21-1.08.15-1.19-.06-.1-.23-.16-.48-.29-.25-.12-1.49-.73-1.72-.82-.23-.08-.4-.12-.57.13-.16.25-.65.82-.8.99-.14.16-.29.19-.54.06-.25-.12-1.06-.39-2.02-1.24-.75-.66-1.25-1.48-1.4-1.73-.14-.25-.01-.38.11-.5.11-.11.25-.29.38-.44.12-.15.16-.25.24-.42.08-.16.04-.31-.02-.44-.06-.12-.56-1.36-.77-1.86-.2-.48-.4-.42-.55-.42z"/></svg></span><b>Canal oficial</b></div>
    </div>
    <div class="web">DML-MEDICA.COM</div>
  </div>
</div></body></html>"""


def cartel(qr_path, destino):
    html = CARTEL.format(
        reg=B.fuente('Regular'), med=B.fuente('Medium'), xb=B.fuente('Extrabold'),
        logo=B.logo('logo-dml-blanco.png', 800, blanco=True),
        qr=base64.b64encode(open(qr_path, 'rb').read()).decode())
    tmp = os.path.join(B.BUILD, 'cartel.html')
    open(tmp, 'w', encoding='utf-8').write(html)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--window-size=1080,1350', '--default-background-color=00000000',
                    '--virtual-time-budget=8000', '--screenshot=' + destino,
                    'file:///' + tmp.replace('\\', '/')], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return destino


def a_jpg(origen, destino):
    """Version JPG para compartir (WhatsApp, correo, imprentas que solo aceptan jpg).
       Calidad 95 sin submuestreo: el QR conserva los bordes filosos y sigue escaneando."""
    im = Image.open(origen).convert('RGBA')
    fondo = Image.new('RGB', im.size, (255, 255, 255))
    fondo.paste(im, mask=im.split()[3])
    fondo.save(destino, 'JPEG', quality=95, subsampling=0, optimize=True, dpi=(300, 300))
    return destino


if __name__ == '__main__':
    os.makedirs(QR_DIR, exist_ok=True)
    print('URL:', B.URL)
    png = qr_png(os.path.join(QR_DIR, 'qr-dml-redes.png'))
    svg = qr_svg(os.path.join(QR_DIR, 'qr-dml-redes.svg'))
    car = cartel(png, os.path.join(QR_DIR, 'cartel-qr.png'))
    jpg1 = a_jpg(png, os.path.join(QR_DIR, 'qr-dml-redes.jpg'))
    jpg2 = a_jpg(car, os.path.join(QR_DIR, 'cartel-qr.jpg'))
    for f in (png, svg, car, jpg1, jpg2):
        print('  %-48s %7.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))
