from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
import pandas as pd
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Iniciar el navegador y abrir la página de inicio de sesión
driver = webdriver.Chrome()  # Asegúrate de tener el chromedriver correspondiente a tu versión de Chrome

# Función para iniciar sesión
def login():
    driver.get("https://www.luxestudio.es/login")
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Correo electrónico']"))
    )
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Contraseña']"))
    )
    
    email_field.send_keys("email@test.com")
    password_field.send_keys("password")
    password_field.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Contenidos')]"))
    )
    logging.info("Inicio de sesión confirmado.")

# Función para verificar si la sesión se ha cerrado y volver a iniciar sesión si es necesario
def check_session_and_relogin():
    if "login" in driver.current_url:
        logging.info("La sesión se ha cerrado. Reintentando iniciar sesión...")
        login()
        driver.get("https://www.luxestudio.es/media?filters=&title=")

# Función para obtener el último índice de producto procesado
def get_last_processed_index(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

# Función para buscar la imagen y extraer la URL
def search_and_extract_image_url(driver, product_name):
    # Separar el nombre del producto por espacios
    parts = product_name.split(' ')
    
    # Crear términos de búsqueda con combinaciones de guiones bajos
    search_terms = [
        '__'.join(parts).replace('/', '_'),
        '_'.join(parts[:2]) + '__' + '__'.join(parts[2:]).replace('/', '_'),
        '__'.join(parts[:2]) + '_' + '_'.join(parts[2:]).replace('/', '_')
    ]

    for search_term in search_terms:
        for attempt in range(3):
            try:
                check_session_and_relogin()  # Verificar sesión antes de buscar
                search_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar']"))
                )
                search_field.clear()
                search_field.send_keys(search_term)
                search_field.send_keys(Keys.RETURN)
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.card"))
                )
                time.sleep(2)
                
                articles = driver.find_elements(By.CSS_SELECTOR, "article.card")
                for article in articles:
                    title = article.find_element(By.CSS_SELECTOR, 'h2.one-line').text
                    if title == f"0{search_term}_030A":
                        image_src = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                        if image_src:
                            transformed_url = image_src.replace('-resized', '')
                            transformed_url = transformed_url.replace('.eu-west-3', '')
                            transformed_url = transformed_url.replace('medium/medium-', '')
                            return transformed_url
                logging.warning(f"Artículo con título {search_term} no encontrado. Intentando alternativa...")
            except StaleElementReferenceException:
                logging.warning(f"StaleElementReferenceException en intento {attempt + 1}. Reintentando...")
                time.sleep(1)
            except NoSuchElementException:
                logging.warning(f"No se encontró el elemento buscado para {search_term} en intento {attempt + 1}. Reintentando...")
                time.sleep(1)
            except Exception as e:
                logging.error(f"Error al buscar la imagen para el producto {product_name}: {e}")
                return None

# Intentar iniciar sesión inicialmente
login()

# Navegar a la página de medios
driver.get("https://www.luxestudio.es/media?filters=&title=")
logging.info("Navegación a la página de medios completada.")

try:
    # Cargar el archivo CSV y obtener el último índice procesado
    df = pd.read_csv('archivo.csv')
    df['base_image'] = df['base_image'].astype(str)
    last_processed_index = get_last_processed_index('ultimo_producto.txt')

    processed_count = 0
    parent_images = {}

    # Iterar sobre los productos en el archivo CSV
    for index, row in df.iterrows():
        if index <= last_processed_index:  # Saltar productos ya procesados
            continue

        check_session_and_relogin()  # Verificar sesión antes de procesar cada producto

        product_name = row['name']
        sku = row['sku']
        parent_sku = row['parent_sku']
        logging.info(f'Procesando producto: {product_name} con SKU: {sku}')
        
        if pd.isna(row['parent_sku']):
            imagen_url = search_and_extract_image_url(driver, product_name)
            if imagen_url:
                df.loc[df['name'] == product_name, 'base_image'] = imagen_url
                parent_images[sku] = imagen_url
                logging.info(f"Imagen encontrada para {product_name}: {imagen_url}")
        else:
            if parent_sku in parent_images:
                df.loc[df['sku'] == sku, 'base_image'] = parent_images[parent_sku]
                logging.info(f"Imagen heredada de padre para {product_name}: {parent_images[parent_sku]}")

        processed_count += 1
        last_processed_index = index

        if processed_count % 10 == 0:
            df.to_csv('archivo-final3-updated.csv', index=False)
            logging.info(f"Se han procesado {processed_count} productos. El archivo CSV se ha guardado.")
            with open('ultimo_producto.txt', 'w') as file:
                file.write(str(last_processed_index))

    df.to_csv('archivo-updated.csv', index=False)
    logging.info("Proceso completado. El archivo CSV ha sido actualizado.")

except Exception as e:
    logging.error(f"Error durante el proceso: {e}")
finally:
    driver.quit()

    # Guardar el índice del último producto procesado
    with open('ultimo_producto.txt', 'w') as file:
        file.write(str(last_processed_index))
