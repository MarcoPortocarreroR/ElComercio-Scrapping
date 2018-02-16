from bottle import  post, run, response, request, route, hook
from bs4 import BeautifulSoup
import urllib
from datetime import timedelta, date
import time
import json
import collections


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

# yy/mm/dd
fecha_inicial = date(int(time.strftime("%Y")),int(time.strftime("%m")), int(time.strftime("%d")))
fecha_final = date(int(time.strftime("%Y")),int(time.strftime("%m")), int(time.strftime("%d")))
url_original = 'http://elcomercio.pe/archivo/todas'



titulares_total = []

for fecha in daterange(fecha_inicial,fecha_final):
    fecha_string = fecha.strftime('%Y-%m-%d')
    
    url_fecha = url_original + fecha_string
    r = urllib.request.urlopen(url_fecha).read()

    soup = BeautifulSoup(r,"lxml")
    letters = soup.find_all("article")
    titulares = [None]*len(letters)
    i = 0;
    for element in letters:
        titulares[i] = element.h2.get_text()
        i=i+1

    for i in range(len(titulares)):
        titulares[i] = titulares[i].replace('\n','')
        titulares[i] = titulares[i].strip(' ')
    
    for i in range(len(titulares)):
        fuente = collections.OrderedDict()
        fuente['id'] = "El Comercio"
        fuente['name'] = "El Comercio"

        articulo = collections.OrderedDict()
        articulo['source'] = fuente
        articulo['title'] = titulares[i]
        #print(json.dumps(articulo,ensure_ascii=False))
        #print(titulares[i])
        titulares_total.append(articulo);

noticias = collections.OrderedDict()
#print(titulares_total)
noticias['articles'] = titulares_total

#print(json.dumps(noticias,ensure_ascii=False))

    
@route('/')
def infoComercio():
    dato_json = json.dumps(titulares_total,ensure_ascii=False)
    return dato_json


@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@post('/cors')
def lvambience():
    response.headers['Content-Type'] = 'application/json'
    return "[1]"

run(host='localhost', port=3030, debug=True)
