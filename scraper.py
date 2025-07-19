import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# El ticker es un código que identifica a una empresa en Bolsa
def buscar_ticker(nombre_empresa):
    
    #Usamos webdriver para iniciar el navegador
    service= Service("./chromedriver")
    options= webdriver.ChromeOptions()
    #options.add_argument("--headless") #Para que no abra una ventana
    
    driver= webdriver.Chrome(service=service, options=options)
    driver.get("https://es.finance.yahoo.com")
    
    
    try:
        
        #Rechazar cookies
        try:
            # Esperar a que estemos en la página de consentimiento
            WebDriverWait(driver, 10).until(
                lambda d: "consent.yahoo.com" in d.current_url #Funcion que toma un parametro d(driver) y devuelve true si el url contiene "consent.yahoo.com" o false si no
            )
 
           #Esperar y hacer clic en el botón "Ir al final"
            scroll_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "scroll-down-btn"))
            )
            scroll_button.click()

            #Esperar y hacer clic en el botón "Rechazar todo"
            rechazar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))
            )
            rechazar.click()

        except Exception as e:
            print("No se pudo rechazar el consentimiento:", e)
        
        
        #Espera máximo 10 segundos hasta que cargue la barra de busqueda
        WebDriverWait(driver,10).until( 
            EC.presence_of_element_located((By.ID, "ybar-sbq"))
        )
        
        #Hace la busqueda por nombre
        search_box= driver.find_element(By.ID, "ybar-sbq")
        search_box.send_keys(nombre_empresa)
        search_box.send_keys(Keys.RETURN)
                
        # Esperamos que cambie de URL
        WebDriverWait(driver, 10).until(
            lambda d: "/quote/" in d.current_url
        )
        
        # Extraemos el ticker de la URL
        current_url = driver.current_url
        return current_url
        
    except Exception as e:
        print("Error: ", e)
        return None
        
    finally:
        driver.quit()
    
    
if __name__ == "__main__":

    nombre_empresa= input("Introduzca el nombre de la empresa: ")
    ticker= buscar_ticker(nombre_empresa)
    if ticker:
        print(f"El ticker de {nombre_empresa} es {ticker}") #f para que sustituya las variables
    else:
        print("No se hayaron resultados")