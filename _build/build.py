# -*- coding: utf-8 -*-
"""Arma dml-redes/index.html: mete las fuentes (woff2), el logo y el QR dentro del HTML.
   Uso:  python _build/build.py
   Requiere: pip install "fonttools[woff]" segno pillow
"""
import base64, io, json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(BASE, '_build')

# ── 1. URL pública del portal (si cambia, edítala aquí y vuelve a correr) ──
URL = 'https://dmlmedica.netlify.app/'

FUENTES = 'C:/Users/GEFORCE/AppData/Local/Microsoft/Windows/Fonts'
MARCA   = 'C:/Users/GEFORCE/Desktop/CODEC CLAUDE/dml-design/brand'
UNI     = 'U+0020-00FF,U+2010-2015,U+2018-201D,U+2022,U+2026,U+2192,U+00D7'


def fuente(nombre):
    from fontTools.subset import main as subset
    dst = os.path.join(BUILD, nombre + '.woff2')
    subset([os.path.join(FUENTES, 'NeurialGrotesk-%s.otf' % nombre),
            '--unicodes=' + UNI, '--flavor=woff2',
            '--layout-features=kern,liga', '--output-file=' + dst])
    b = open(dst, 'rb').read()
    os.remove(dst)
    return base64.b64encode(b).decode()


def logo(archivo, ancho=520, blanco=False, solo_simbolo=False):
    from PIL import Image
    im = Image.open(os.path.join(MARCA, archivo)).convert('RGBA')
    if solo_simbolo:                       # recorta el isotipo (favicon cuadrado)
        izq = im.crop((0, 0, int(im.width * 0.42), im.height))
        caja = izq.split()[3].getbbox()
        im = izq.crop(caja)
        lado = max(im.size)
        lienzo = Image.new('RGBA', (lado, lado), (0, 0, 0, 0))
        lienzo.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2))
        im = lienzo
    if blanco:                             # el "logo blanco" trae el isotipo en gris:
        r, g, b, a = im.split()             # lo igualamos a blanco puro
        im = Image.merge('RGBA', (a.point(lambda _: 255),) * 3 + (a,))
    im = im.resize((ancho, max(1, round(im.height * ancho / im.width))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'PNG', optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def qr_svg(url):
    import segno
    buf = io.BytesIO()
    segno.make(url, error='q').save(
        buf, kind='svg', xmldecl=False, svgclass=None, lineclass=None,
        omitsize=True, border=2, dark='#073243', light=None)
    svg = buf.getvalue().decode('utf-8')
    return svg.replace('<svg ', '<svg role="img" aria-label="Código QR del portal de redes de DML Médica" ', 1)


def main():
    plantilla = open(os.path.join(BUILD, 'plantilla.html'), encoding='utf-8').read()
    piezas = {
        '__REG__':   fuente('Regular'),
        '__MED__':   fuente('Medium'),
        '__XB__':    fuente('Extrabold'),
        '__LOGO__':  logo('logo-dml-blanco.png', blanco=True),
        '__LOGOC__': logo('logo-dml-color.png', 180, solo_simbolo=True),
        '__QR__':    qr_svg(URL),
        '__URL__':   URL,
    }
    salida = plantilla
    for k, v in piezas.items():
        salida = salida.replace(k, v)

    faltan = re.findall(r'__[A-Z]+__', salida)
    if faltan:
        sys.exit('Quedaron marcadores sin reemplazar: %s' % set(faltan))

    destino = os.path.join(BASE, 'index.html')
    open(destino, 'w', encoding='utf-8', newline='\n').write(salida)
    print('OK -> %s  (%.1f KB)' % (destino, os.path.getsize(destino) / 1024))


if __name__ == '__main__':
    main()
