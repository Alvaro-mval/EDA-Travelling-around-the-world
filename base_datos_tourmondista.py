# %%
import hashlib
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json
import pprint
import re
from bs4 import BeautifulSoup as bs

#LeTourMondiste Asia
url_leTourMondiste_asia = "https://www.tourdumondiste.com/plus-beaux-pays-asie-du-sud-est"


asia = requests.get(url_leTourMondiste_asia)

print(asia.status_code, asia.reason)

ltm_asia = bs(asia.text, "html.parser")

# %%
Pays = []
Note_globale_sur_10 = []
Budget = []
Accueil = []
Communication = []
Culture = []
Affluence_touristique =[]
Gastronomie =[]
Logements =[]
Paysages =[]
Proprete=[]
Securite=[]
Tranquillite=[]
Transports=[]
Villes=[]

dict_asia={'Pais': Pays,
      'Nota Global': Note_globale_sur_10,
      'Presupuesto': Budget, 
      'Acogida': Accueil,
      'Comunicacion': Communication,
      'Cultura': Culture, 
      'Affluencia turistica': Affluence_touristique,
      'Gastronomia': Gastronomie,
      'Hoteles': Logements,
      'Paisajes': Paysages,
      'Limpieza': Proprete,
      'Seguridad': Securite,
      'Tranquilidad': Tranquillite,
      'Transportes': Transports,
      'Ciudades': Villes,

}

print(dict_asia)

# %%
paises_asia = ltm_asia.find_all("div", class_="Product__container") 
print(dict_asia) 
for pais in paises_asia: 
    #Pais
    Pays.append(pais.find("div", class_="Product__value productTitle").text.strip())

    # Nota Global
    note_div = pais.find("div", class_="Product__value globalNote")
    Note_globale_sur_10.append(float(note_div.find("div")["note"].replace(",", ".")))

    # Budget
    budget_div = pais.find("div", class_="Product__value budgetNote")
    Budget.append(float(budget_div.find("div")["notecritere"].replace(",", ".")))

    # Accueil
    accueil_div = pais.find("div", class_="Product__value welcomeNote")
    Accueil.append(float(accueil_div.find("div")["notecritere"].replace(",", ".")))

    # Communication
    communication_div = pais.find("div", class_="Product__value communicationNote")
    Communication.append(float(communication_div.find("div")["notecritere"].replace(",", ".")))

    # Culture
    culture_div = pais.find("div", class_="Product__value cultureNote")
    Culture.append(float(culture_div.find("div")["notecritere"].replace(",", ".")))

    # Affluence touristique
    affluence_div = pais.find("div", class_="Product__value masstourismNote")
    Affluence_touristique.append(float(affluence_div.find("div")["notecritere"].replace(",", ".")))

    # Gastronomie
    gastronomie_div = pais.find("div", class_="Product__value foodNote")
    Gastronomie.append(float(gastronomie_div.find("div")["notecritere"].replace(",", ".")))

    # Logements
    logements_div = pais.find("div", class_="Product__value accomodationNote")
    Logements.append(float(logements_div.find("div")["notecritere"].replace(",", ".")))

    # Paysages
    paysages_div = pais.find("div", class_="Product__value landscapeNote")
    Paysages.append(float(paysages_div.find("div")["notecritere"].replace(",", ".")))

    # Propreté
    proprete_div = pais.find("div", class_="Product__value cleanNote")
    Proprete.append(float(proprete_div.find("div")["notecritere"].replace(",", ".")))

    # Sécurité
    securite_div = pais.find("div", class_="Product__value securityNote")
    Securite.append(float(securite_div.find("div")["notecritere"].replace(",", ".")))

    # Tranquillité
    tranquillite_div = pais.find("div", class_="Product__value peaceNote")
    Tranquillite.append(float(tranquillite_div.find("div")["notecritere"].replace(",", ".")))

    # Transports
    transports_div = pais.find("div", class_="Product__value transportNote")
    Transports.append(float(transports_div.find("div")["notecritere"].replace(",", ".")))

    # Villes
    villes_div = pais.find("div", class_="Product__value cityNote")
    Villes.append(float(villes_div.find("div")["notecritere"].replace(",", ".")))

# %%
df_paises_asia = pd.DataFrame(dict_asia)

# %%
#LeTourMondiste Asia
paises_urls =[("Argentina","https://www.tourdumondiste.com/avis-conseils-bons-plans-argentine"),
              ("Brasil","https://www.tourdumondiste.com/avis-conseils-bons-plans-bresil"),
              ("Chile","https://www.tourdumondiste.com/avis-voyage-chili"),
              ("Bolivia","https://www.tourdumondiste.com/avis-conseils-bons-plans-bolivie"),
              ("Colombia","https://www.tourdumondiste.com/avis-conseils-bons-plans-colombie"),
              ("Mexico","https://www.tourdumondiste.com/avis-conseils-bons-plans-mexique"),
              ("Peru","https://www.tourdumondiste.com/avis-conseils-bons-plans-perou"),
              ("Australia","https://www.tourdumondiste.com/avis-conseils-bons-plans-australie"),
              ("Nueva Zelanda","https://www.tourdumondiste.com/avis-voyage-nouvelle-zelande"),
              ("China","https://www.tourdumondiste.com/avis-voyage-chine")
]

# %%
Pays = []
Note_globale_sur_10 = []
Budget = []
Accueil = []
Communication = []
Culture = []
Affluence_touristique =[]
Gastronomie =[]
Logements =[]
Paysages =[]
Proprete=[]
Securite=[]
Tranquillite=[]
Transports=[]
Villes=[]

dict_paises={'Pais': Pays,
      'Nota Global': Note_globale_sur_10,
      'Presupuesto': Budget, 
      'Acogida': Accueil,
      'Comunicacion': Communication,
      'Cultura': Culture, 
      'Affluencia turistica': Affluence_touristique,
      'Gastronomia': Gastronomie,
      'Hoteles': Logements,
      'Paisajes': Paysages,
      'Limpieza': Proprete,
      'Seguridad': Securite,
      'Tranquilidad': Tranquillite,
      'Transportes': Transports,
      'Ciudades': Villes,

}

print(dict_paises)

# %%
for pais_nombre, url in paises_urls:
    html = requests.get(url).text
    soup = bs(html, "html.parser")       

# País se añade a mano porque la URL cambia en cada pais y no hay una tabla como en el caso de Asia. 
# La nota media tampoco aparece asique la calcularemos luego con la media de los demas parametros.
#El budget tampoco esta y se le asignara mas tarde.

    Pays.append(pais_nombre)
    Note_globale_sur_10.append("NaN")
    Budget.append("NaN")


    cols = soup.find_all("div", class_="col-sm-6") #buscamos todos los col-sm-6 donde estan las notas que nos interesan y la categoria.

    for col in cols:
        label_tag = col.find("p", class_="label-progressbar") #obtenemos la categoria (nombre de cada columna)
        prog_div = col.find("div", class_=re.compile(r"prog\d+"))  #Buscamos dentro del bloque un <div> cuya clase contenga la palabra “prog” seguida de números.
        
        #por ejemplo, estas variables de arriba nos daran algo como ["paysages", "prog94"]


        if not label_tag or not prog_div:
            continue  # si no hay datos, saltar. Esto nos evita que el codigo se pare si no encuentra ningun label_tag o prog_div
        
        nombre = label_tag.text.strip() #para el nombre, solo cogemos nuestro label_tag y lo ponemos en formato texto para luego asignarlo a la clave correspondiente de nuestro dict
        
        # extraer número de la clase progXX
        #Como el numero (nota) "solo" no esta en html sino que es un ::before (el admin pone el numero externamente),
        #tenemos que sacar nuestro dato de la barra de powerbar utilizando este metodo. Luego esa parte del string lo separamos y lo pasamos a float.

        clases = " ".join(prog_div["class"])  #esta funcion convierte la lista de clases del div en una cadena de texto separada por espacios. Algo asi como "paysage prog94"
        match = re.search(r"prog(\d+)", clases) #aqui buscamos dentro de la cadena el patrón "prog" seguido de un número. Y (\d+) captura los números en un grupo.

        if not match:
            continue
        
        valor = float(match.group(1)) / 10.0 # pasamos esos numeros a float

        # Asignar el valor a la lista correspondiente media
        if "Accueil" in nombre:
            Accueil.append(valor)
        elif "Communication" in nombre:
            Communication.append(valor)
        elif "Culture" in nombre:
            Culture.append(valor)
        elif "Épargné" in nombre or "Affluence" in nombre:
            Affluence_touristique.append(valor)
        elif "Gastronomie" in nombre:
            Gastronomie.append(valor)
        elif "Logements" in nombre:
            Logements.append(valor)
        elif "Paysages" in nombre:
            Paysages.append(valor)
        elif "Propreté" in nombre:
            Proprete.append(valor)
        elif "Sécurité" in nombre:
            Securite.append(valor)
        elif "Tranquillité" in nombre:
            Tranquillite.append(valor)
        elif "Transports" in nombre:
            Transports.append(valor)
        elif "Villes" in nombre:
            Villes.append(valor)



# %%
df_paises = pd.DataFrame(dict_paises)

# %%
#añadimos una marca de Presupuesto basandones en opiniones de la web, dando menor nota a los paises mas caros.

df_paises.loc[df_paises['Pais'].isin(['Australia', 'Nueva Zelanda']), 'Presupuesto'] = 5.3
df_paises.loc[df_paises['Pais'].isin(['Argentina', 'Chile']), 'Presupuesto'] = 6.5
df_paises.loc[df_paises['Pais'].isin(['China']), 'Presupuesto'] = 7.5
df_paises.loc[df_paises['Pais'].isin(['Brasil', 'Colombia']), 'Presupuesto'] = 8.4
df_paises.loc[df_paises['Pais'].isin(['Mexico', 'Peru']), 'Presupuesto'] = 8.9
df_paises.loc[df_paises['Pais'].isin(['Bolivia']), 'Presupuesto'] = 9.5
df_paises['Presupuesto'] = df_paises['Presupuesto'].astype(float)

# %%
#Concatenamos las dos listas para tener nuestro dataset de opiniones de turistas para 17 paises.

df_mundo = pd.concat([df_paises, df_paises_asia], ignore_index=True)

#Calculamos el total de "puntos" de cada pais y hacemos la media (nota global)
df_mundo["Nota Global"] = round(df_mundo.loc[:, "Presupuesto":"Ciudades"].mean(axis=1),2)

#Renombramos los paises de asia que aún estan en francés
df_mundo['Pais'] = df_mundo['Pais'].replace({
    'Indonésie': 'Indonesia',
    'Philippines': 'Filipinas',
    'Thaïlande': 'Tailandia',
    'Malaisie': 'Malasia',
    'Cambodge': 'Camboya',
})

df_mundo1 = df_mundo

