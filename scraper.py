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
def buscar(nombre_empresa):
    
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
            deny = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reject-all"))
            )
            deny.click()

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
        
        url= driver.current_url
        
        # Entramos en la URL sin el panel de busqueda
        driver.get(url)
        
        # Recopilamos los datos de la empresa
        #Obtenemos el html completo de la página
        html=driver.page_source
        
        #Creamos el objeto beautiful soup
        soup= BeautifulSoup(html, "html.parser")    #Para que podamos navegar por los contenidos como si fuese un arbol
        
        datos={}
        
        #Nombre
        name=soup.find("h1", class_="yf-4vbjci")
        datos["Nombre"]= name.text if name else "N/A"
        
        #Precio actual
        price=soup.find(attrs={"data-testid":"qsp-price"})
        datos["Precio actual"]= price.text if price else "N/A"
        
        #Cambio diario (valor + porcentaje)
        change=soup.find(attrs={"data-testid":"qsp-price-change"})
        percent=soup.find(attrs={"data-testid":"qsp-price-change-percent"})
        if change and percent:
            datos["Cambio diario"]= f"{change.text} ({percent.text})"
        else:
            datos["Cambio diario"]="N/A"
                
        #Resto de datos
        for li in soup.find_all("li", class_="yf-z3c4f6"):
            spans=li.find_all("span")
            if len(spans)>=2:
                clave=spans[0].text.strip() #strip para eliminar los espacios extras o saltos de linea
                valor=spans[1].text.strip()
                datos[clave]=valor
        
        return datos
        
        
    except Exception as e:
        print("Error: ", e)
        return None
        
    finally:
        driver.quit()
    
    
if __name__ == "__main__":

    nombre_empresa= input("Introduzca el nombre de la empresa: ")
    datos= buscar(nombre_empresa)
    if datos:
        print(f"Los datos de {nombre_empresa} son {datos}") #f para que sustituya las variables
    else:
        print("No se hayaron resultados")