# Web Scraper con Selenium

Este proyecto es un script de Python que utiliza Selenium para realizar web scraping en páginas web específicas. Está diseñado para automatizar la recopilación de datos y su almacenamiento en archivos CSV para un análisis posterior.

## Descripción

El `scraper.py` es capaz de iniciar sesión en un sitio web, navegar por los elementos de la página, extraer información relevante y guardar esos datos en un archivo CSV. Además, registra el índice del último producto procesado para permitir un scraping eficiente por lotes.

## Instalación

Asegúrate de tener Python 3.x instalado en tu sistema y sigue estos pasos para instalar las dependencias necesarias:

### Dependencias

Instala las siguientes dependencias utilizando `pip`:

```bash
pip install selenium pandas
```

Además, necesitarás descargar el WebDriver para Chrome que coincida con tu versión actual de Google Chrome.

### Configuración

Antes de ejecutar el script, asegúrate de configurar las siguientes variables dentro del script:

- Credenciales de usuario para el inicio de sesión (usuario y contraseña).
- Parámetros de búsqueda o navegación específicos del sitio.

## Uso

Para ejecutar el script, abre una terminal y corre el siguiente comando:

```bash
python scraper.py
```

El script iniciará una sesión de Chrome, realizará el proceso de scraping y guardará los resultados en `archivo-updated.csv`. También se guardará el índice del último producto procesado en `ultimo_producto.txt` para futuras ejecuciones.

## Contribución

Si deseas contribuir al proyecto, sigue estos pasos:

Proximamente 

## Manejo de Errores

El script utiliza logging para registrar eventos y errores. Si ocurre un error durante la ejecución, revisa el archivo de log para obtener detalles y posibles soluciones.
