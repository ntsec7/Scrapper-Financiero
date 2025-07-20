# Genera una gráfica comparativa del precio de las acciones de las distintas empresas a lo largo del tiempo

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

#os.system para ejecutar en la terminal. Si esta en windows(nt) ejecuta cls, si no ejecuta clear
def borrar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')    

def arreglar_precio(numero):
    
    if isinstance(float, (int,float) ): #Si ya esta formateado lo devuelve tal cual
        return numero
    elif pd.isna(numero) or not isinstance(numero,str): #Si no es None, Nan o no es texto devuelve None
        return None
    
    
    numero=numero.replace(".","") #Quito el separador de miles
    numero=numero.replace(",",".") #Cambio el , decimal por .
    
    try:
        return float(numero)
    except ValueError:
        return None

    
    
def limpiar_datos(df):
    
   #Convertimos la fecha a datetime
    df["Fecha"]= pd.to_datetime(df["Fecha"],format="%d-%m-%Y %H:%M:%S", errors="coerce") #coerce evita errores si hay algun error
    
    #Conversión del precio a número
    df["Precio actual"]= df["Precio actual"].apply(arreglar_precio) 
    
    return df


def grafico_empresa(archivo, empresa):
    
    df= pd.read_csv(archivo)
    
    #Filtro para la empresa concreta
    df=df[df["Nombre"]==empresa].copy()
    
    if df.empty:
        print(f"No existen datos de {empresa}")
        return
    
    df=limpiar_datos(df)
    
    #Creo el gráfico
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x="Fecha", y="Precio actual")
    plt.title("Evolución en el precio de las acciones")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.tight_layout() #Para que no se solapen las etiquetas
    
    return plt
       
    
def grafico_todas(archivo):
    
    df= pd.read_csv(archivo)
    
    df=limpiar_datos(df)
    
     #Creo el gráfico
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x="Fecha", y="Precio actual", hue="Nombre") #Cada empresa(nombre) se representa por un color distinto
    plt.title("Evolución en el precio de las acciones")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.tight_layout() #Para que no se solapen las etiquetas
    
    return plt
    

if __name__== "__main__":
    
    #Busca en el archivo que le pasan por argumento o en historico.csv por defecto
    archivo="historico.csv"
    
    if len(sys.argv) >= 2:
        archivo=sys.argv[1]

    
    opcion= -1
    
    while opcion!=1 and opcion!=2 and opcion!=3:
        borrar_pantalla()
        print("\033[0;32m Seleccione que quiere hacer \033[0m")
        print("\033[0;36m 1.\033[0m Evolución del precio de las acciones de una empresa")
        print("\033[0;36m 2.\033[0m Comparativa del precio de las acciones de todas las empresas")
        print("\033[0;36m 3.\033[0m Salir")
    
        opcion= int(input(""))
        
    borrar_pantalla()
    
    if opcion==1:
        
        opcion2=-1
        
        #Guardamos las posibles empresas sin que se repitan
        df = pd.read_csv(archivo)
        empresas= df["Nombre"].dropna().unique() #dropna quita los valores NaN
        
        while opcion2<1 or opcion2>len(empresas):
            borrar_pantalla()
            print("\033[0;32m Seleccione una empresa: \033[0m")
            for i, nombre in enumerate(empresas):
                print(f"\033[0;36m{i+1}.\033[0m {nombre}")
                
            opcion2=int(input(""))
            
        empresa=empresas[opcion2-1]
        grafico=grafico_empresa(archivo, empresa)
        
    elif opcion==2:
        grafico=grafico_todas(archivo)
        
    elif opcion==3:
        exit()
        
        
    borrar_pantalla()
    grafico.show()