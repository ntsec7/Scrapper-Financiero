
Scraper en Python que recopila datos financieros de Yahoo Finance y mostra una gráfica con el precio a lo largo del tiempo

Para poder usar el programa hará falta tener:
 - Chrome instalado
 - chromedriver(misma versión del chrome) ubicado en la misma carpeta en la que tengas los ejecutables
 - Las bibliotecas: selenium, beautifulsoup, pandas, matplotlib y seaborn *(Instalación con: pip install selenium beautifulsoup4 pandas matplotlib seaborn)*.

Hay dos ejecutables:
   
  - **scraper.py**: Recopila los datos de Yahoo Finance. Busca los datos de las empresas que están apuntadas en *empresas.txt* (debe estar el nombre de cada empresa en una línea distinta), muestra los resultados           por pantalla y los guarda en *historico.csv*. Recomiendo programar una ejecución periódica automática con el comando cron.

   - **grafica.py**: Muestra un menú interactivo con el que crea una gráfica de la evolución de los precios de una empresa en particular o de todas las empresas. Recoge los datos del archivo que se le pase como          o de *historico.csv* por defecto.


## Licencia
Este proyecto está licenciado bajo la [Licencia MIT](./LICENSE).  

