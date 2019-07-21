# -*- coding: utf-8 -*-
__author__ = 'DanielMarco'

from bs4 import BeautifulSoup
from pathlib import Path
import requests

DOMAIN = "http://play.cadenaser.com"
URL = DOMAIN + "/programa/nadie_sabe_nada"
DOWNLOAD_DIR = "F:/Descargas/Jdownloader/audio/"
translation_table = dict.fromkeys(map(ord, '?.!/;:@#$"'), None)

class Podcast:
    def __init__(self, title, link):
        self.title = title
        self.link = link

############################################
#Obtiene todas las entradas de una pagina
############################################
def getPagina(urlpagina):
    # Realizamos la petición a la web
    req = requests.get(urlpagina)
    objects = []
    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code
    if status_code == 200:

        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")

        # Obtenemos todos los divs donde están las entradas
        listado = html.find('ul', {'class': 'listado'})

        # Recorremos todas las entradas para extraer el título y el enlace
        entradas = listado.find_all('li', {'class': 'btnlistener'})

        for i, entrada in enumerate(entradas):
            enlace = entrada.find('a')
            podcastElem = Podcast(enlace["title"], enlace["href"])
            #print("Title: %s | href: %s" % (podcastElem.title , podcastElem.link))
            objects.append(podcastElem)
    else:
        print ("Status Code %d" % status_code)

    return objects;

############################################
#Desde la pagina principal obtenemos la maxima paginacion
############################################
def getNumPaginas(urlpagina):
    # Realizamos la petición a la web
    req = requests.get(urlpagina)
    totalPags = ""
    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code
    if status_code == 200:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")
        # Obtenemos todos los divs donde están las entradas de paginacion
        paginacion = html.find('div', {'class': 'paginacion'})
        #Obtenemos el texto
        txt = paginacion.find('span', {'class': 'txt'})
        #Obtenemos el numero de paginas del programa
        entradas = txt.find_all('span')

        for i, entrada in enumerate(entradas):
            totalPags = entrada.getText().strip()
    return totalPags;

############################################
#Obtiene el fichero de audio de una entrada
############################################
def getAudioFile(urlpodcast):
    audioUrl = ""
    podcastFile = ""
    # Realizamos la petición a la web
    req = requests.get(urlpodcast)
    # Comprobamos que la petición nos devuelve un Status Code = 200
    status_code = req.status_code
    if status_code == 200:
        # Pasamos el contenido HTML de la web a un objeto BeautifulSoup()
        html = BeautifulSoup(req.text, "html.parser")
        audioUrl = html.find('meta', {'itemprop': 'contentUrl'})
        audioFilename = html.find('meta', {'itemprop': 'name'})
        podcastFile = Podcast(audioFilename["content"], audioUrl["content"])

    return podcastFile;

############################################
#Descarga un fichero desde una url
############################################
def downloadRequest(url, filename):
    r = requests.get(url, stream=True)
    total = int(r.headers.get('content-length'))
    downloaded = 0
    print("Response: %s" % r.status_code)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
            downloaded += len(chunk)
            done = int(50*downloaded/total)
            f.write(chunk)
            print ('\r[{}{}]'.format('█' * done, '.' * (50-done)), end="\r")
            
            

#########################################################################
#main
#########################################################################
totalPags = getNumPaginas(URL)
print("Total pages to download: " + totalPags)

#Para empezar la descarga de cada pagina, debe ser >= 1
iniPage = 1
#Para empezar por la primera entrada de una pagina, especificar 0
iniEntry = 0

for i in range(iniPage, int(totalPags)+1):
    pageUrl = URL + "/%d" % i
    print("Obtaining Podcasts from page: " + pageUrl)
    objects = getPagina(pageUrl)
    for j, element in enumerate(objects):
        if j >= iniEntry:
            urlPodcast = DOMAIN + element.link
            podcastFile = getAudioFile(urlPodcast)
            print("Downloading file: %s, text: %s" % (podcastFile.link, podcastFile.title))
            cleanFileTitle = podcastFile.title.translate(translation_table)
            filepath = DOWNLOAD_DIR +  cleanFileTitle + Path(podcastFile.link).suffix
            downloadRequest(podcastFile.link, filepath)
            print("File downloaded in %s" % filepath)
    iniEntry = 0
