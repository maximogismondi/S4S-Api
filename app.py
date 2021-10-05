from typing import Collection
import os, json
from flask import Flask, json, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import algoritmo

app = Flask(__name__)
llaves = {
    "type": "service_account",
    "project_id": "proyectos4s-89b8a",
    "private_key_id": "06d29cceefcd0db3129889722a8e10ce01e3c7f6",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvcZRy3toLchmb\n+JLOmiJekF9q7ULlCxOAPUQuJDbWPQjpvlpSSywlqxc4V95lU8R0H2j955ErvhEh\nGDA/bC4fZSzM1Pp9z8WgCDr4v7SUBwOWGOcD94h47D3OFR+ehM8z2DbOB5NGyOPL\nJYYDnYEpFuVE1d/alx5TCqHyfCpuBPaB6e3DLAnG7DAI7VCxrp6Rc/cGFzNG1ZZ4\n4XNo2Cy1+iF8fZKLFJkhan3o0fl33FewpnNkOmwLx39csztDnCz5m/e6DvkeqLHY\n3wPq98zjtBq/gpp4vfeCUKIpQPIS4U2RMcwyo9fE0B/zZDP/E/jGzS0zXy15ubn9\nR3StVk9pAgMBAAECggEALaHnMLGSGSQGUTEoTiB9DAeVKeSoX5av7c0BrNayhKq/\nZLykFX+D7hBAK+F+8PAGywVYc6IFelEnd2opMnXa0UOpkWVb+dlO178MR6LlPxNL\n9YBopfl+P6WCtdV8sehtVFjKeHAz+FdMGIyb/Ni8vYk8/Nh8LwjbVFIRqVZuWsr1\nQvpJudP9oCf8BHuIB03OSpt8TS5GkG9urR9T1AdEbBy5aWQ17aRs6R7eFHjHaQj4\nSOI7+xvdAiwxwv6RoAe+NI2dj+zN0brTYVZtG03GhCjDuBTPzO91FXtRJYicOykY\nOovRcGg7mQllQMEJQRxQMD9eZZDvC7NU7/N6eN4ZWQKBgQDfrjDvR1vcOGIRL2jB\nHrSdo+4Vztr9Ok4UQLg4flvngN/BqpPSldEL6HTAddWUOhixjxkdlUbHvasHnLJW\nHwvtobdK8fpOQTSZFr4qB93zCcXkR7jV3Ex5VXBiti+8mVWYmzYOWmCChXixdByU\nIuZ3FaadnODsBSgXuUvRzE5TqwKBgQDIyyOVJPPHfbHqhPEx2R0uqsFl771uclKZ\nEZgj40Kfr7G8FwhOml5V9l9j1J8LUK50F7jvXTyCH4lpIm1/T36z4UhGGBeVtiBP\nAGWJokydeqp7ifPCuP0xFn4rbrcxg3AVJIn+est1L+NOgZaXBvS/lqpKbhq0ubT6\nIfm800QVOwKBgDX7C8QzLHARC1mqX1V724rPrP2GVkMWdxFcLRk1JWjRKS7Lw7Dm\nhvSgvMxVo52KB7uSFTWWeOZrV4MWxdMS2wYWKO3lR8rq4Y6wdmQeUen9Scy1ol26\nNJpzjBPGc+7H8mhJzNnZ5cCaBW6N3vfBFG1YxET1PzK2a96N0UZoT97RAoGAVbEk\nCWWQyEVjZaPAz7ZJ1v22tcs/u9/8UikJFd/KMh4oKw5lVC5bLjKL+S3nhkuzeAYb\nvcO7rAjLetvfgSKq/xeY4Zksj47/cNfJfZiPO/H6yehQ6HxMSePAisagVfgzIELM\nxZcgN23tgzaYzvGACDfDiyo8KX7LtqhDTYuYFbsCgYBwIlsA2ExJfFLszQF7jV/M\npzo4b8kCHdkTx2a51mbfsIlFcbWcJMXEpVJvnWYUGlsFT+0q3rCuiP5rz/fC7d2Q\nI5MK1/yLYW9CaB1QRtzrV0ITcM69aWVPZ6iV3Lf2piCndWuGOakDd7cW0bRDv6u9\n013I2Jkvy3MoKhsjTRpaLw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-2kpop@proyectos4s-89b8a.iam.gserviceaccount.com",
    "client_id": "108558504320900989171",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2kpop%40proyectos4s-89b8a.iam.gserviceaccount.com"
  }

cred = credentials.Certificate(llaves)
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

from flask_cors import CORS, cross_origin
from flask import Flask
import gunicorn
from datetime import datetime
import threading
from time import sleep

class Materia():
    def __init__(self, nombre, curso, posibleProfesores, posiblesAulas, cantModulos, modulosContinuos, color):
        self.nombre = nombre + "-" + curso
        self.curso = curso
        self.posibleProfesores = posibleProfesores
        self.posiblesAulas = posiblesAulas
        self.cantModulos = cantModulos
        self.modulosContinuos = modulosContinuos
        self.color = color

class Turno():
    def __init__(self, nombre, cantModulos):
        self.nombre = nombre
        self.cantModulos = cantModulos

class Posicion():
    def __init__(self, curso, dia, turno, modulo):
        self.curso = curso
        self.dia = dia
        self.turno = turno
        self.modulo = modulo

app = Flask("appUWU")
CORS(app)

@app.route('/adminONO', methods=['GET'])
def  esAdminOnoEsAdmin():
    idUsuario = request.args.get('idUsuario')
    print(idUsuario)
    doc_ref = db.collection(u'users').document(idUsuario)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data:')
    else:
        return(u'No such document!')
 
    docDiccionario = doc.to_dict()
    print(docDiccionario.get("emailVerified"))
    return str(docDiccionario.get("emailVerified"))

@app.route('/')
def hello_world():
    return "A"

@app.route('/algoritmo', methods=['GET'])
def  hilos():
    idColegio = request.args.get('idColegio')
    hora = str(datetime.fromisoformat( datetime.now().isoformat(timespec='minutes') ))
    def math_fun():
        # The sleep here is simply to make it clear that this happens in the background
        sleep(1) 
        runAlgorithm(idColegio, hora)

    def fun():
        # Create thread to run math_fun for each argument in x 
        t = threading.Thread(target=math_fun)
        t.setDaemon(False)
        t.start()
        print("Ejecutado prro")

    fun()
    return hora

def runAlgorithm(idColegio = "jejeboi", hora = "algo fallo"):
    print(idColegio)
    doc_ref = db.collection(u'schools').document(idColegio)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document found!')
    else:
        return(u'No such document!')
    

    #docDiccionario es un diccionario de la escuela
    docDiccionario = doc.to_dict()
    aulas = []
    profesores = []
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    cursos = []
    turnos = []
    materias = []
    horarios = []
    modulos = []
    disponibilidad = {}
    [cursos.append(i.get("nombre")) for i in docDiccionario["cursos"]]
    [aulas.append(i.get("nombre")) for i in docDiccionario["aulas"]]
    [profesores.append(i.get("nombre") + " " + i.get("apellido")) for i in docDiccionario["profesores"]]
    for i in docDiccionario["profesores"]:
        disponibilidad[i.get("nombre") + " " + i.get("apellido")] = i.get("disponibilidad")

    for i in docDiccionario["turnos"]:
        if len(i.get("modulos")) > 0:
            nombreT = str(i.get("turno"))
            cantidadModulosT = len(i.get("modulos"))
            for i in i.get("modulos"):
                modulos.append(i)
            t = Turno(nombreT, cantidadModulosT)
            turnos.append(t)

    for curso in cursos:
        materias.append([Materia("Hueco", curso, [], [], 0, 99, "white")])

    for i in docDiccionario["materias"]:
        nombreM = i.get("nombre")
        cursoM = i.get("curso")
        posiblesProfesoresM = []
        for profesor in i.get("profesoresCapacitados"):
            if (i.get("profesoresCapacitados")[profesor]):
                posiblesProfesoresM.append(profesor)
        posiblesAulasM = []
        for aula in i.get("aulasMateria"):
            if (i.get("aulasMateria")[aula]):
                posiblesAulasM.append(aula)
        cantidadDeModulosTotalM = i.get("cantidadDeModulosTotal")
        cantidadMaximaDeModulosPorDiaM = i.get("cantidadMaximaDeModulosPorDia")
        a = Materia(nombreM, cursoM, posiblesProfesoresM, posiblesAulasM, cantidadDeModulosTotalM, cantidadMaximaDeModulosPorDiaM, "red")
        materias[cursos.index(a.curso)].append(a)

    horarioDeDisponibilidad = []
    for j in dias:
        horarioDeDisponibilidad.append([])
        indexModulos = 0
        for k in turnos:
            horarioDeDisponibilidad[dias.index(j)].append([])
            for f in range(k.cantModulos):
                horarioDeDisponibilidad[dias.index(j)][turnos.index(k)].append(["Hueco"])
                for n in profesores:
                    if modulos[indexModulos]["inicio"] in disponibilidad[n][j][k.nombre] and disponibilidad[n][j][k.nombre][modulos[indexModulos]["inicio"]]:
                        horarioDeDisponibilidad[dias.index(j)][turnos.index(k)][f].append(n)
                indexModulos += 1

    try:
        horarios, materiasProfesores, horariosAulas = algoritmo.algoritmo(aulas, profesores, dias, cursos, turnos, materias, horarioDeDisponibilidad)
    except:
        print("An exception occurred in your pp") 
    
    horariosDiccionario = {}
    for curso in range(len(cursos)):
        horariosDiccionario[cursos[curso]] = {}
        for dia in range(len(dias)):
            horariosDiccionario[cursos[curso]][dias[dia]] = {}
            for turno in range(len(turnos)):
                horariosDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre] = {}
                for modulo in range(turnos[turno].cantModulos):
                    horariosDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre][str(modulo+1)] = horarios[curso][dia][turno][modulo].nombre


    horariosAulasDiccionario = {}
    for curso in range(len(cursos)):
        horariosAulasDiccionario[cursos[curso]] = {}
        for dia in range(len(dias)):
            horariosAulasDiccionario[cursos[curso]][dias[dia]] = {}
            for turno in range(len(turnos)):
                horariosAulasDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre] = {}
                for modulo in range(turnos[turno].cantModulos):
                    horariosAulasDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre][str(modulo+1)] = horariosAulas[curso][dia][turno][modulo]
    
    diccionarioColegio = {"horarios":horariosDiccionario, "materiasProfesores":materiasProfesores, "horariosAulas":horariosAulasDiccionario}
    escribir(diccionarioColegio, hora, idColegio)

def idGenerator():
    doc_ref = db.collection(u'school').document()
    return doc_ref.id

def escribir(my_data, hora, idColegio):

    db.document(u"horariosHechos/"+idColegio+"/horarios/"+hora).set(my_data)
    
    try:
        id = idGenerator()
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 3304))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)

#fijarse cuando se sube algo
#importar algoritmo