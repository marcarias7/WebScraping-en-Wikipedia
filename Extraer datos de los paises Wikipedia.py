import requests
from bs4 import BeautifulSoup
import pandas as pd

numHabitantes = list()
Pais = list()
Continente = []
Oceania = list()
America = list()
Africa = list()
Asia = list()
Europa = list()

def buscarContinente(country):
    if country in Oceania:
        return "Oceania"

    elif country in America:
        return "America"

    elif country in Africa:
        return "Africa"

    elif country in Asia:
        return "Asia"
            
    elif country in Europa:
        return "Europa"
    else:
        return "NO ENCONTRADO"

#Capturando el html
URL = 'https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_y_territorios_dependientes_por_poblaci%C3%B3n'
URL2 = 'https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_continentes'
page = requests.get(URL)
page2 = requests.get(URL2)
soup = BeautifulSoup(page.content,'html.parser')
soup2 = BeautifulSoup(page2.content,'html.parser')


#Preparando lista de continentes
div = soup2.body.find('div', class_="mw-parser-output")
continentes = div.find_all('table')

#Copiando paises Europa
search = continentes[1].find_all('td',align="center")
for i in search:
    Europa.append(str(i.contents[2].text))


#Copiando paises de Asia
search = continentes[3].find_all('td',align="center")
for i in search:
    Asia.append(str(i.contents[2].text))

#Copiando paises de Africa
search = continentes[7].find_all('tr')
index = 0
for i in search:
    if index == 0:
        index += 1
        continue
    else:
        show = i.find('td').find_all('a')
        Africa.append(str(show[0].text))

#Copiando paises de America
search = continentes[8].find_all('td',align="center")
for i in search:
    America.append(str(i.contents[2].text))

#Copiando paises de Oceania
search = continentes[11].find_all('tr')
index = 0
for i in search:
    if index == 0:
        index += 1
        continue
    else:
        td = i.find('td').find_all('a')
        a = list(td)        
        Oceania.append(str(a[0].text))

#Copiando paises
td_paises = soup.table.tbody.find_all('td')
td_search = list(td_paises)
pos = 0
for i in range(1,2920,12):
    Pais.append(str(td_search[i].find('a').text))
    Continente.append(buscarContinente(str(td_search[i].find('a').text)))

#Copiando cantidad de habitantes
contenido = soup.table.find('tbody')
tr = contenido.find_all('tr')

for i in range(1,245):
    search = tr[i].find('td',text=f"{i}")
    iterable_hermanos = search.find_next_siblings('td')
    lista = list(iterable_hermanos)
    aux = lista[7].text.split()
    index = 0
    for z in aux:
        if z == " ":
            aux.pop(index)
            index += 1
        index += 1    
    nHab = "".join(aux)
    numHabitantes.append(nHab)


df = pd.DataFrame({'Paises':Pais, 'Continente':Continente, 'Cantidad de habitantes':numHabitantes})

inds = []

for k in range(len(Continente)):
    if Continente[k] == "NO ENCONTRADO":
        inds.append(k)

df2 = df.drop(inds, axis = 0)
"""df2.to_csv('Pais.txt', index = False)"""
print(df)
print(df2)
print("SE HAN ELIMINADO LOS ELEMENTOS SIN DATOS EN LA COLUMNA 'Continente'")
print("\n\nEL ARCHIVO FUE EXPORTADO EN FORMATO .CSV")