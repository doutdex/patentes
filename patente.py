import requests
from termcolor import colored
from bs4 import BeautifulSoup
import exceptions


print colored("""
  ___          _                  _              
 | _ \  __ _  | |_   ___   _ _   | |_   ___   ___
 |  _/ / _` | |  _| / -_) | ' \  |  _| / -_) (_-<
 |_|   \__,_|  \__| \___| |_||_|  \__| \___| /__/
 

    v0.1
""","magenta",attrs=['bold'])
print colored("\t Informacion por patente vehicular.\n","green",attrs=['underline'])
print colored("Formato 'XXXXXX'.Ejemplo: AA1111 \n Si es Motocicleta rellena con '0' ",'red',attrs=['bold'])

#extrae informacion del texto(pagina) que es devuelto
def destripa(pag):
    #trabajamos con sopa
    soup = BeautifulSoup(pag,"html.parser")
    panel = soup.findAll("div",{"class":"col-lg-4"})
    info = panel[0].findAll("div",{"class":"panel-body"})
    contents = info[0].findAll("pre")
    names = info[0].findAll("p")
    #recorre parametros devueltos y los imprime
    for i in range(0,len(names)-1):
        print names[i].text+ ":" + contents[i].text
        print "*------------------------------------*"


#La pagina de Porpietario es un poco diferente
#por lo que necesitaba su metodo aparte
def destripaPt(pag):
    soup = BeautifulSoup(pag,"html.parser")
    panel = soup.findAll("div",{"class":"list-group"})
    body = panel[0]
    print "Propietario: ",body.text


#crea la coneccion
def search(patent):
    with requests.Session() as c:
        url = 'http://www.multidata.cl/warpit/html/login/main/'
        user = "correos.11235@gmail.com"
        passwd = "ot5qlzzeru"
        c.get(url)
        login_data = dict(ususer=user,uspass=passwd,next="/") 
        #nos logeamos
        c.post(url,data=login_data,headers={"referer":"http://www.multidata.cl/"})
        c.get("http://www.multidata.cl/warpit/html/cars/main/")
        try:
            #obtenemos informacion del vehiculo
            patent_data = dict(plate = patent,action="car",objid="new",fkey = "plate",fields="action,plate")
            p =c.post("http://www.multidata.cl/warpit/html/cars/main/",data=patent_data,headers={"referer":"http://www.multidata.cl/warpit/html/login/main/"})               
            destripa(p.text)
        except exceptions.AttributeError:
            print colored("\n No hay registros para tal patente \n","red",attrs=['bold'])
        except Exception as e:
            print "error: ",type(e),e
        try:
            #obtenemos informacion de propietarios
            patent_data = dict(plate = patent,action="owners",objid="new",fkey = "plate",fields="action,plate")
            owners =c.post("http://www.multidata.cl/warpit/html/cars/main/",data=patent_data,headers={"referer":"http://www.multidata.cl/warpit/html/login/main/"})
            destripaPt(owners.text) 
        except Exception:
            print colored("\n No se han encontrado datos de propietarios \n","red",attrs=['bold'])
        try:
            #obtenemos informacion policial
            patent_data = dict(plate = patent,action="extra",objid="new",fkey = "plate",fields="action,plate")
            police =c.post("http://www.multidata.cl/warpit/html/cars/main/",data=patent_data,headers={"referer":"http://www.multidata.cl/warpit/html/login/main/"})
            destripa(police.text)
        except Exception:
            print colored("\n No se han encontrado datos policiales \n","red",attrs=['bold'])


#ciclo de nuestro script
while(True):
    try:
        patent = raw_input("Patente:")
        search(patent)
        op=(raw_input("Salir?s/n")).upper()
        if(op=='S'):
            print "Hasta la proxima!"
            break
    except exceptions.AttributeError as error:
        print "error con patente",error,type(error)
    except KeyboardInterrupt:
        print "saliendo..."
        break
    except exceptions.EOFError:
        print "saliendo..."
        break
    except BaseException as error:
        print "error",type(error),error
