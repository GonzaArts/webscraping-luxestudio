# README

Este script de Python utiliza la biblioteca Selenium WebDriver para automatizar el proceso de búsqueda y extracción de URLs de imágenes de productos en el sitio web `https://www.luxestudio.es`. A continuación, se describen las principales secciones y funciones del script, así como el flujo general del programa.

## Dependencias
- **Selenium**: Para automatizar la interacción con el navegador.
- **Pandas**: Para la manipulación y análisis de datos.
- **Logging**: Para registrar información relevante durante la ejecución del script.

## Configuración Inicial
1. Configuración de **logging**: Se establece la configuración básica del registro para que muestre la hora, el nivel de gravedad y el mensaje.
2. Inicialización del **WebDriver**: Se crea una nueva instancia del navegador Chrome.

## Funciones Principales
1. **login()**:
   - Navega a la página de inicio de sesión.
   - Encuentra los campos de correo electrónico y contraseña, los llena y envía el formulario.
   - Espera hasta que la página de contenido esté cargada para confirmar el inicio de sesión.

2. **check_session_and_relogin()**:
   - Verifica si la sesión se ha cerrado comprobando la URL actual.
   - Si es necesario, inicia sesión nuevamente y navega de vuelta a la página de medios.

3. **get_last_processed_index(filename)**:
   - Lee y retorna el último índice de producto procesado desde un archivo.
   - Si el archivo no existe, retorna 0.

4. **search_and_extract_image_url(driver, product_name)**:
   - Divide el nombre del producto en partes y crea términos de búsqueda.
   - Realiza una búsqueda en la página de medios y extrae la URL de la imagen del producto.
   - Realiza varios intentos en caso de excepciones durante la búsqueda.

## Flujo Principal del Programa
1. Intenta iniciar sesión inicialmente usando la función `login()`.
2. Navega a la página de medios.
3. Carga el archivo CSV `archivo.csv` y obtiene el último índice de producto procesado.
4. Itera sobre los productos en el archivo CSV:
   - Verifica y re-inicia sesión si es necesario.
   - Busca y extrae la URL de la imagen del producto o hereda la imagen del producto padre si está disponible.
   - Actualiza el DataFrame y guarda el índice del último producto procesado.
5. Guarda el DataFrame actualizado en un nuevo archivo CSV `archivo-updated.csv`.
6. En caso de cualquier excepción, registra el error y cierra el navegador.
7. Finalmente, guarda el índice del último producto procesado en un archivo y cierra el navegador.

## Instrucciones para la Ejecución
1. Asegúrate de tener instaladas las bibliotecas necesarias y el `chromedriver` correspondiente a tu versión de Chrome.
2. Ejecuta el script y revisa los registros para monitorear el progreso y detectar cualquier posible error.
