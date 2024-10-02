import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Solicitar al usuario que ingrese varias palabras clave separadas por comas
keywords = ["analista", "especialista", "ejecutivo", "software", "desarrollador", "developer", "product",
            "automatizador", "manager"]

# Limpiar las palabras clave (eliminar espacios en blanco alrededor de cada palabra)
keywords = [keyword.strip().lower() for keyword in keywords]

# Lista para almacenar los resultados
job_results = []

# Abrir la página
url = "https://www.chiletrabajos.cl/encuentra-un-empleo?2=&13=1022&fecha=2&categoria=&8=&14=&inclusion=&f=1"
driver = webdriver.Chrome()
driver.get(url)

try:
    while True:
        # Intentar cerrar el pop-up si aparece
        try:
            # Esperar a que el botón de cerrar esté presente
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dismiss-button"))
            )
            close_button.click()  # Hacer clic en el botón "Cerrar"
            print("Pop-up cerrado.")
            time.sleep(1)  # Esperar un segundo para asegurarnos de que el anuncio se cierra

        except Exception as e:
            print("No hay pop-up o error:", e)

        # Esperar a que los trabajos estén cargados
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-item.with-thumb.destacado.no-hover"))
        )

        # Encontrar todos los elementos que contienen el título y el enlace
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-item.with-thumb.destacado.no-hover")

        # Extraer el título y el enlace de cada trabajo
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, ".title.overflow-hidden a")
                title = title_element.text  # Texto del título del trabajo
                link = title_element.get_attribute("href")  # Obtener el enlace de la oferta

                # Inicializar una variable para guardar la palabra que coincide
                matching_keyword = None

                # Filtrar por las palabras clave en el título (insensible a mayúsculas/minúsculas)
                for keyword in keywords:
                    if keyword in title.lower():
                        matching_keyword = keyword  # Guardar la palabra que coincide
                        break  # Si encuentra una coincidencia, no es necesario seguir buscando

                if matching_keyword:
                    # Almacenar los resultados en un diccionario
                    job_results.append({
                        "title": title,
                        "matching_keyword": matching_keyword,
                        "link": link
                    })
                    print(f"Título: {title}\nPalabra coincidente: {matching_keyword}\nEnlace: {link}\n")

            except Exception as e:
                print(f"Error al procesar un trabajo: {e}")

        # Intentar ir a la siguiente página
        try:
            next_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.page-link[rel="next"]'))
            )
            next_button.click()  # Hacer clic en el botón "Siguiente"
            time.sleep(3)  # Esperar a que se carguen los nuevos trabajos
        except Exception as e:
            print("No se pudo encontrar el botón 'Siguiente':", e)
            # Recargar la página si hay problemas
            print("Recargando la página debido a un error...")
            driver.refresh()
            time.sleep(3)  # Esperar a que la página se recargue

except Exception as e:
    print(f"Error: {e}")

finally:
    # Guardar los resultados en un archivo JSON
    with open('job_chiletrabajos.json', 'w', encoding='utf-8') as json_file:
        json.dump(job_results, json_file, ensure_ascii=False, indent=4)
    print("Resultados guardados en job_results.json.")

    # Cerrar el navegador
    driver.quit()

