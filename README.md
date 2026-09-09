# DML Médica — Portal de redes sociales (QR)

Página tipo "link en bio" para DML Médica. Se comparte con un **código QR**: quien lo escanea
llega a una sola pantalla con botones a todas las redes de la empresa.

**URL pública:** https://redes.dml-medica.com/

> Mientras el subdominio termina de configurarse, la página también responde en
> https://mrcontentoficial-cloud.github.io/dml-redes/

## Qué incluye

| Archivo | Para qué sirve |
|---|---|
| `index.html` | El portal. Un solo archivo: fuentes, logo y QR van dentro, no depende de nada externo (147 KB). |
| `qr/qr-dml-redes.png` | QR de 1400 px con el isotipo DML al centro. Para artes, empaques o firmas de correo. |
| `qr/qr-dml-redes.jpg` | El mismo QR en JPG, para compartir por WhatsApp o correo. |
| `qr/qr-dml-redes.svg` | El mismo QR en vector, para imprenta (se puede ampliar sin pixelearse). |
| `qr/cartel-qr.png` | Cartel 1080 × 1350 con la marca DML, listo para imprimir o publicar en redes. |
| `qr/cartel-qr.jpg` | El cartel en JPG, para mandarlo por WhatsApp o subirlo a redes. |

## Enlaces que muestra

1. Instagram — [@dmlmedica](https://www.instagram.com/dmlmedica/)
2. Facebook — [DML Médica](https://www.facebook.com/profile.php?id=61561692536106)
3. TikTok — [@dml_medica](https://www.tiktok.com/@dml_medica)
4. YouTube — [canal oficial](https://www.youtube.com/channel/UCExyg464aHi95KObGlQB74g)
5. Canal de WhatsApp — [novedades](https://whatsapp.com/channel/0029Vaohei9GE56iuFlMqP2W)

Solo redes: la página no lleva enlaces a la tienda. En el pie queda la firma de la empresa
con `dml-medica.com`.

## Cómo cambiar textos o enlaces

Todo lo editable está marcado dentro del HTML con el comentario `✏️ CAMBIA` (búscalo con Ctrl+F).

- **Cambiar un enlace:** busca la red en `index.html` y edita el `href`, el `<b>` (nombre) y el `<i>` (subtítulo).
- **Agregar una red:** copia un bloque `<li> … </li>` completo, pégalo donde quieras que aparezca
  y cambia el `href`, el ícono (la clase `i-…`) y los textos.
- **Quitar una red:** borra su bloque `<li> … </li>`.

Los cambios de texto y de enlaces se hacen directo en `index.html`; no hace falta compilar nada.

## Dominio

El subdominio `redes.dml-medica.com` apunta a GitHub Pages con un **CNAME** en Cloudflare:

```
Tipo    CNAME
Nombre  redes
Destino mrcontentoficial-cloud.github.io
Proxy   DNS only (nube gris)
TTL     Auto
```

El archivo `CNAME` de este repo es el que le dice a GitHub Pages qué dominio atender: si se
borra, el sitio vuelve a responder solo en la dirección `github.io`.

## Cómo regenerar (solo si cambia la URL, el logo o el QR)

La carpeta `_build/` guarda la plantilla y los scripts. GitHub Pages ignora las carpetas que
empiezan con `_`, así que no se publican.

```bash
python _build/build.py   # arma index.html (mete fuentes Neurial, logo y QR)
python _build/qr.py      # regenera el QR en png/jpg/svg y el cartel
```

Si la página cambia de dirección, edita la variable `URL` en `_build/build.py` y corre los dos
comandos: se actualizan el QR de la página, los archivos imprimibles y el cartel. **Ojo:** un QR
ya impreso deja de servir si cambia la URL.

Requisitos: `pip install "fonttools[woff]" segno pillow` y Google Chrome (para el cartel).

## Detalles técnicos

- Marca: gradiente azul → teal → cian y tipografía **Neurial Grotesk**, iguales a los banners de DML.
- Fuentes recortadas a woff2 (14 KB cada una) para que cargue rápido con datos móviles.
- Los QR se verifican con un decodificador (`cv2.QRCodeDetector`): PNG, JPG, SVG, cartel y el que
  muestra la página en pantalla. Se prueban también recomprimidos a calidad 50 (lo que les hace
  WhatsApp) y en miniatura de 400 px.
- Botones "Compartir" (usa el menú nativo del celular) y "Ver QR" (muestra el código en pantalla,
  útil para que un vendedor lo enseñe desde su teléfono).
