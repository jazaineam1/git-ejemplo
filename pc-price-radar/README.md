# PC Price Radar — buscador y comparador de computadores

**Fecha: 25-oct-2026. Estado: prototipo funcional publicado como código en GitHub; no es aún un agregador universal de precios.**

## Qué hay implementado

* Catálogo de **342 dominios únicos**, 29 países o regiones y 26 fuentes clasificadas para Colombia; ver [catalog.json](./catalog.json).
* Panel móvil con filtros de CPU, RAM, SSD, GPU, VRAM, pantalla, batería deseada, precio y condición; orientado a Ollama, agentes y ciencia de datos.
* Botones de búsqueda en cada comercio (Google con el operador site:dominio) y Google Shopping. El sitio del vendedor no aplica automáticamente esos filtros internos: son términos de búsqueda.
* Carga manual e importación/exportación de ofertas con URL, fecha, vendedor, variante, descuentos, cupones, envío, impuestos, TRM y características.
* Comparación en COP con clasificación de costo parcial cuando no se conocen envío o tributos. Se conservan los registros en el navegador.
* Conector opcional SerpApi Google Shopping Colombia, que entrega fichas JSON con origen y fecha. No usa scraping directo a comercios.
* Verificación HTTPS HEAD por dominio con Python, programada por GitHub Actions cuando la función esté habilitada. Es solamente un chequeo técnico de respuesta HTTP.

**Advertencia central:** 342 dominios catalogados NO significan 342 tiendas con ventas, filtros, inventario, entrega a Colombia y precios comprobados. Los dominios están pendientes de validación comercial; una respuesta HTTP 200 no demuestra confianza, precio ni disponibilidad. La app inicia con [offers.json](./offers.json) vacío para no inventar precios.

## Abrir la aplicación

- Código fuente: https://github.com/jazaineam1/git-ejemplo/tree/main/pc-price-radar
- Archivo: [index.html](./index.html)
- Para ejecutar con Python 3.11 o superior desde esta carpeta: python -m http.server 8000
- Abrir http://localhost:8000/ (no usar file://: el navegador necesita poder cargar JSON).
- Para habilitar un enlace público: GitHub > Settings > Pages > Deploy from a branch > main > / (root). Si Pages está habilitado y ha publicado correctamente, la URL esperada es https://jazaineam1.github.io/git-ejemplo/pc-price-radar/ . **Ese enlace aún no está comprobado como publicado.**

## Activar las búsquedas de precios automáticas

1. Obtener acceso autorizado a SerpApi y revisar su plan y tarifas.
2. Guardar una clave SERPAPI_KEY en GitHub > Settings > Secrets and variables > Actions, nunca en HTML o JavaScript público.
3. Abrir Actions > PC Price Radar - validar y actualizar > Run workflow; se admite una lista de consultas separadas por punto y coma.
4. El workflow ejecuta primero las pruebas dos veces; luego comprueba los dominios y usa el proveedor solo si existe la clave. Máximo cuatro consultas por ejecución por defecto.
5. El job está configurado para 05:00 y 17:00 UTC, sujeto a habilitación y límites de GitHub Actions.
6. Si falla el agregador, conserva el JSON anterior; la existencia de una oferta en Google Shopping tampoco garantiza stock, envío ni precio final.

Para probar sin credenciales, desde la carpeta pc-price-radar:

    python -m unittest discover -s tests -v
    python scripts/verify_sources.py --limit 200 --workers 8

Para revisar resultados de la verificación HTTP: [sources-status.json](./sources-status.json), que se crea al ejecutar el script. **Nunca describir este conteo como número de tiendas verificadas para comprar.**

## Decisiones de ingeniería

- Comparar exactamente la misma variante; verificar GPU y TGP, VRAM, CPU, panel, RAM/SSD, duración real de batería, garantía y teclado.
- Precio estimado en COP = (precio de lista × (1 − descuento/100) − cupón + flete + impuestos) × tasa de cambio. Cuando faltan componentes, el total se rotula PARCIAL.
- Para ejecutar modelos locales, CUDA y VRAM en GPU NVIDIA dedicada suelen pesar más que NPU o Intel Arc cuando las herramientas usadas requieren CUDA, sin que ello haga a Intel/AMD inútiles para otros usos.
- No atribuir compatibilidad de Ollama, autonomía o rendimiento a una ficha que no lo indique.
- Confirmar fecha y restricciones de promociones; los porcentajes anunciados no equivalen a ahorro real.
- Los importes colombianos del agregador pueden ser ambiguos. El colector usa filtro de plausibilidad y los marca como inferidos, NO verificados.

## Fuentes técnicas consultadas

* Amazon Creators API: https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction
* eBay Browse API: https://developer.ebay.com/api-docs/buy/api-browse.html
* Mercado Libre API: https://developers.mercadolibre.com.co/es_ar/api-docs-es/items-y-busquedas
* SerpApi Google Shopping: https://serpapi.com/google-shopping-api
* GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

Se observaron páginas reales para portátiles en https://www.alkosto.com/computadores-tablet/computadores-portatiles/c/BI_104_ALKOS , https://listado.mercadolibre.com.co/computacion/portatiles-accesorios/portatiles/ , https://www.pcware.com.co/portatiles/geforce-rtx-4060 , https://www.professionalwireless.com.co/computador-portatil/portatil-gamer-msi-katana-17-core-i9-13th-rtx-4060-32gb-1tb/ y https://lowpi.com/colombia/laptops-rtx-4060 . Eso no constituye auditoría de precios, legitimidad o inventario.

## Por completar para un comparador comercial competitivo

Feeds/APIs contractuales por vendedor, más de 200 comercios con precio comprobado, búsqueda y normalización de SKU/GTIN, deduplicación, índice histórico, verificación de cupones en checkout, impuestos por destino, alertas, pruebas E2E móviles y registro de cambios. No se presentan como implementados. Los datos manuales permanecen en el navegador salvo exportación expresa.
