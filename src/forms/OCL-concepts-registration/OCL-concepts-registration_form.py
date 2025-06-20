from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import json

# Configuración inicial
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
driver_path = "C:\\WebDriver\\chromedriver.exe"

# Crear un objeto Service para el controlador de Chrome
service = Service(driver_path)

# Opciones para el navegador Brave
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Inicializa el driver con el objeto Service
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# Accede a la página de inicio de sesión
driver.get("https://app.openconceptlab.org/#/orgs/PeruHCE/sources/sihsalus/concepts/?q=&isTable=true&isList=false&page=1")

try:
    # Esperar a que cargue la página
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Presionar botón Sign In
    sign_in_button = driver.find_element(By.XPATH, "//a[contains(text(),'Sign In')]")
    sign_in_button.click()

    # Esperar a que cargue la página de login
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
	
    #===========================================================================
    #===============IMPORTANTE===================================================
    #==========================================================================
    # Ingresar credenciales (Ingresa tus credenciales personalizadas)
    driver.find_element(By.ID, "username").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")

    # Presionar el botón de Sign In
    driver.find_element(By.ID, "kc-login").click()

    # Esperar redirección y seleccionar PeruHCE
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "PeruHCE")))
    driver.find_element(By.LINK_TEXT, "PeruHCE").click()

    # Esperar redirección y seleccionar sihsalus
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "sihsalus")))
    driver.find_element(By.LINK_TEXT, "sihsalus").click()

    # Esperar carga de la página de conceptos
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Manage Content']")))

    # Presionar botón Add
    add_button = driver.find_element(By.XPATH, "//button[@aria-label='Manage Content']")
    add_button.click()
    time.sleep(2)

    # Seleccionar Add Concept del dropdown
    add_concept = driver.find_element(By.XPATH, "//li[contains(text(),'Add Concept')]")
    add_concept.click()
    time.sleep(3)

    # Datos a procesar
    concepto = "Arabela"
    sinonimos = ["Tapueyocuaca", "Chiripuno"]
    
    # Definir la variable wait antes de su uso
    wait = WebDriverWait(driver, 10)

    
    # Seleccionar el dropdown de Concept Class
    dropdown_button = wait.until(EC.element_to_be_clickable((By.ID, "fields.concept_class")))
    dropdown_button.click()
    time.sleep(1)
    concept_class_value = "fields.concept_class-option-0"  # Cambiar el índice según necesidad
    option = wait.until(EC.element_to_be_clickable((By.ID, concept_class_value)))
    option.click()
    time.sleep(1)
    driver.find_element(By.ID, "fields.concept_class").send_keys(Keys.TAB)
    time.sleep(1)
    
    # Definir la variable wait antes de su uso
    wait = WebDriverWait(driver, 10)
    # Seleccionar el dropdown de Datatype
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "fields.datatype")))
    datatype_variable =driver.find_element(By.ID, "fields.datatype-option-1")
    datatype_variable.click()
    time.sleep(1)
    

    
    # Llenar el primer grupo
    driver.find_element(By.ID, "fields.names.0.locale").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fields.names.0.locale-listbox")))
    driver.find_element(By.ID, "fields.names.0.locale-option-0").click()

    driver.find_element(By.ID, "fields.names.0.name_type").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fields.names.0.name_type-listbox")))
    driver.find_element(By.ID, "fields.names.0.name_type-option-0").click()  # Fully-Specified

    driver.find_element(By.ID, "fields.names.0.name").send_keys(concepto)
    preferred_checkbox = driver.find_element(By.NAME, "preferred")
    preferred_checkbox.click()
    time.sleep(1)
    
    #===============================================
    #=================AUMENTAR POTENZIA
    #====================================================
    try:
        for _ in range(len(sinonimos)+1):
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[h3[text()='Names & Synonyms']]/following-sibling::div[@class='col-md-4']/button")))
            element.click()
            time.sleep(1)
    except Exception as e:
        print(f"Ocurrió un error en aumentar los sinonimos: {e}")
    #===============================================
    #=================FINALIZAR POTENZIA
    #====================================================
    # Datos Fijo en grupo 2
    etnia = "Etnia"
    # Llenar el segundo grupo
    driver.find_element(By.ID, "fields.names.1.locale").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fields.names.1.locale-listbox")))
    driver.find_element(By.ID, "fields.names.1.locale-option-0").click()

    driver.find_element(By.ID, "fields.names.1.name_type").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fields.names.1.name_type-listbox")))
    driver.find_element(By.ID, "fields.names.1.name_type-option-2").click()  # Index

    driver.find_element(By.ID, "fields.names.1.name").send_keys(etnia)
    time.sleep(1)

    # Llenar los demas grupos
    try:
        for i in range(2, 2 + len(sinonimos)):  # Comienza desde 2 y hace #sinonimos de iteraciones
            termino_ga = sinonimos[i-2]
            # Llenar desdeel grupo i
            driver.find_element(By.ID, f"fields.names.{i}.locale").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"fields.names.{i}.locale-listbox")))
            driver.find_element(By.ID, f"fields.names.{i}.locale-option-0").click()

            driver.find_element(By.ID, f"fields.names.{i}.name_type").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"fields.names.{i}.name_type-listbox")))
            driver.find_element(By.ID, f"fields.names.{i}.name_type-option-2").click()  # Index

            driver.find_element(By.ID, f"fields.names.{i}.name").send_keys(termino_ga)
            time.sleep(1)
    except Exception as e:
        print(f"Ocurrió un error en la insercion de grupo 3 n adelante {e}")
        
    try:    
        # Presionar el botón Create
        create_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'Create')]")
        create_button.click()
        print("Formulario completado y enviado correctamente con los datos proporcionados.")
    except Exception as e:
        print(f"Ocurrió un error en el registro {e}")
        
except Exception as e:
    print(f"Ocurrió un error en el codigo: {e}")

finally:
    # Cerrar el navegador después de 5 segundos
    time.sleep(5)
    driver.quit()
