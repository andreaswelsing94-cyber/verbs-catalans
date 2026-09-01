# Verbs Catalans

PWA estática, gratuita y sin registro para aprender y practicar conjugaciones catalanas. Está diseñada para móviles Android, funciona sin conexión después de la primera visita y puede publicarse directamente en una subruta de GitHub Pages.

## Estado real de los datos

- **100 verbos** (53 clasificados como regulares y 47 como irregulares).
- **6.306 celdas lingüísticas** y **8.156 formas o variantes almacenadas**. El segundo recuento incluye variantes normativas y construcciones completas compuestas/perifrásticas.
- 15 tiempos practicables: presente, imperfecto, pasado perifrástico, pasado simple, perfecto, pluscuamperfecto, futuro y futuro perfecto de indicativo; condicional simple y compuesto; presente, imperfecto, perfecto y pluscuamperfecto de subjuntivo; e imperativo afirmativo.
- Formas no personales disponibles según el corpus: infinitivo, gerundio, participio y construcciones perfectas.

El selector de 250/500/1.000 se muestra para que la interfaz y la configuración permanezcan preparadas para futuras ampliaciones, pero nunca finge que existen más datos: la lista informa siempre del número real disponible.

## Fuente lingüística y licencia

Las formas simples y sus variantes proceden de **Apertium Catalan 2.12.0**, paquete morfológico mantenido por el proyecto Apertium: <https://github.com/apertium/apertium-cat>. El repositorio declara **GNU GPL v2 o posterior** en su archivo `COPYING`; por compatibilidad, este proyecto completo se distribuye bajo **GPL-2.0-or-later** y conserva la licencia en `LICENSE`. Autores y contribuciones de la fuente pueden consultarse en el archivo `AUTHORS` del repositorio original.

El script `scripts/generate_data.py` extrae las formas desde `apertium-cat.cat.metadix`; no conjuga por reglas inventadas. Las construcciones compuestas se ensamblan de forma reproducible con las formas de `haver` y el participio extraídos de la misma fuente; el pasado perifrástico usa las formas de `anar` y el infinitivo del mismo corpus. Los textos gramaticales y ejemplos breves son originales de este proyecto, revisados contra la descripción normativa de la conjugación del Institut d’Estudis Catalans: <https://giec.iec.cat/conjugacio/introduccio>. No se han copiado tablas del IEC.

La posición de frecuencia es **orientativa y pedagógica**, no el resultado de un corpus estadístico redistribuido. La lista de 100 lemas comunes se mantiene explícitamente en el generador; Apertium aporta y verifica la morfología. No se incluyen traducciones al español de los lemas porque no se localizó una fuente bilingüe con el mismo nivel de trazabilidad y una licencia integrada en este proceso.

## Funciones

- Navegación SPA entre Pràctica, Verbs, Gramàtica y Configuració, sin recargas.
- Sesiones generales, por verbo, por tiempo, favoritos, irregulares o errores.
- Corrección que ignora mayúsculas y espacios sobrantes, pero exige los acentos y la forma completa.
- Repetición sin duplicar combinaciones hasta agotar el paquete; ponderación opcional de errores.
- Resumen de sesión, lista de errores y enlaces a la tabla y tiempo exactos.
- Diccionario con búsqueda sin acentos, filtros, favoritos, fichas y navegación anterior/siguiente.
- Gramática breve en catalán y accesos directos a la práctica de cada tiempo.
- Configuración completa y progreso local versionado, con migración de la versión 1 a la 2.
- Diseño mobile-first accesible, teclado, foco visible, contraste y modo claro/oscuro del sistema.
- Manifest, iconos 192/512, service worker con actualización de caché y fallback offline.

## Estructura

```text
index.html                 interfaz principal
css/app.css                diseño adaptable
js/app.js                  vistas y navegación
js/engine.js               práctica, filtros y estadísticas
js/storage.js              persistencia y migraciones
js/grammar.js              guía y ejemplos
data/verbs.json            única base lingüística usada por práctica y diccionario
scripts/generate_data.py   extracción y validación desde Apertium
scripts/generate_icons.js  iconos PNG reproducibles
tests/                     pruebas automáticas
sw.js / manifest.webmanifest / icons/  PWA
```

`work/apertium-cat` es una copia de trabajo de la fuente y no hace falta publicarla. Los archivos que sí necesita la web están fuera de `work/`.

## Probar en el ordenador

Requiere Python 3 para servir archivos estáticos y Node.js 20 o posterior solo para las pruebas.

```bash
python3 -m http.server 8080
```

Abre <http://localhost:8080/>. No abras `index.html` mediante `file://`: los módulos, el manifiesto y el service worker necesitan HTTP.

Para simular exactamente una subruta de GitHub Pages desde la carpeta superior:

```bash
cd ..
python3 -m http.server 8080
```

Abre `http://localhost:8080/referenced-chatgpt-conversation-this-is-an/`. Todas las rutas son relativas y conservan la subruta.

## Pruebas y regeneración

```bash
npm test
python3 scripts/generate_data.py --check
node scripts/generate_icons.js
```

Para regenerar los datos desde la fuente exacta:

```bash
git clone --depth 1 https://github.com/apertium/apertium-cat.git work/apertium-cat
python3 scripts/generate_data.py
```

Las validaciones detectan identificadores o infinitivos duplicados, formas vacías, personas no válidas del imperativo, recuentos incorrectos y datos generados desactualizados. Las pruebas cubren comparación, acentos, espacios, variantes, búsqueda, filtros, personas/tiempos, no repetición, estadísticas, errores, persistencia y migración.

## Publicar gratis en GitHub Pages

1. Crea una cuenta en <https://github.com/signup>.
2. En GitHub, pulsa **New repository**, llámalo `verbs-catalans`, elige **Public** y créalo vacío.
3. Desde esta carpeta ejecuta, sustituyendo `TU_USUARIO`:

   ```bash
   git init
   git add index.html css js data icons tests scripts manifest.webmanifest sw.js package.json README.md LICENSE
   git commit -m "Publica Verbs Catalans"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/verbs-catalans.git
   git push -u origin main
   ```

4. En el repositorio abre **Settings → Pages**.
5. En **Build and deployment**, selecciona **Deploy from a branch**, rama `main`, carpeta `/(root)`, y guarda.
6. Tras unos minutos, abre `https://TU_USUARIO.github.io/verbs-catalans/`.

No subas `work/`: no es necesaria para ejecutar la aplicación y contiene el repositorio fuente completo.

## Instalar en Android y funcionamiento sin conexión

Abre la dirección de GitHub Pages en Chrome para Android, espera la primera carga y usa **⋮ → Añadir a pantalla de inicio → Instalar**. La aplicación se abre sin la interfaz del navegador. El service worker guarda la interfaz, los iconos y toda la base lingüística. Después de esa primera carga puede funcionar sin red. Al volver a abrirla con conexión, la versión `verbs-catalans-v1` reemplaza cachés anteriores cuando cambia el identificador de caché en `sw.js`.

El progreso se guarda exclusivamente en `localStorage` del navegador, bajo la clave `verbs-catalans-progress`. No sale del dispositivo. Borrar los datos del sitio o desinstalar y limpiar Chrome puede eliminarlo.

## Limitaciones y ampliación hasta 1.000

- La aplicación incluye 100 verbos, no 1.000. Alcanzar 250/500/1.000 exige elegir y documentar una lista de frecuencia catalana legalmente redistribuible y revisar la clasificación regular/irregular de cada nuevo paradigma.
- Apertium es una fuente morfológica abierta y amplia, pero no sustituye una revisión editorial individual del IEC. Antes de una publicación educativa de alta responsabilidad conviene revisar las 100 fichas con un lingüista y registrar la versión/commit exactos del corpus.
- Algunas variantes territoriales presentes en Apertium pueden aparecer como respuestas aceptadas. La interfaz no etiqueta aún cada variedad.
- La PWA no incorpora sonido, sincronización entre dispositivos, exportación de progreso ni traducciones de lemas.
- La prueba automática verifica la estructura y formas esenciales, pero la instalación real depende de HTTPS (GitHub Pages lo ofrece) y debe confirmarse en Chrome/Android.

Proceso recomendado de ampliación: fijar un commit de Apertium; sustituir `VERBS` por una lista de lemas con fuente y licencia citadas; ejecutar el generador; resolver los lemas ausentes; revisar irregularidad y variantes; ejecutar `npm test` y `--check`; hacer una revisión lingüística por muestreo reforzado para irregulares; y actualizar los recuentos de este README sin prometer niveles aún no incorporados.

## Licencia

GNU General Public License, versión 2 únicamente. Véase `LICENSE`.
