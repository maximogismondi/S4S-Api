from typing import Collection
import os
from flask import Flask, json, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
app = Flask(__name__)
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

from flask_cors import CORS, cross_origin
from flask import Flask
import gunicorn
import copy, random, time
import copy, operator
import plotly.graph_objects as go
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

def algoritmo(aulas, profesores, dias, cursos, turnos, materias):

    #Funcion que revisa si en determinado modulo, el aula esta disponible
    def aulaDisponible(aula, horarioVerificar, dia, turno, modulo, cursoExcepcion):
        for curso in cursos:
            if curso != cursoExcepcion:
                if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre.split('-')[0] != "Hueco" and horariosAulas[cursos.index(curso)][dia][turno][modulo] == aula:
                    return False
        return True

    #Funcion que revisa si en determinado modulo, el profesor esta disponible
    def profesorDisponible(profesor, horarioVerificar, dia, turno, modulo, cursoExcepcion):
        for curso in cursos:
            if curso != cursoExcepcion:
                if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre.split('-')[0] != "Hueco" and materiasProfesores[horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre] == profesor:
                    return False
        return True

    def validarModulosContinuos(horariosChequear, cursoChequear, diaChequear, turnoChequear, moduloChequear):

        materiaChequear = horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear]

        #Chequeo q no corte una materia a la mitad 
        if moduloChequear != 0 and moduloChequear != turnos[turnoChequear].cantModulos - 1 and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre == horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear + 1].nombre and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre != horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear].nombre:
            return False

        #Chequeo q no corte un hueco
        if materiaChequear.nombre.split('-')[0] != "Hueco":
            if turnoChequear == 0 and moduloChequear == 0 and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear + 1].nombre.split("-")[0] == "Hueco":
                return False
            elif turnoChequear == len(turnos) - 1 and moduloChequear == turnos[turnoChequear].cantModulos - 1 and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre.split("-")[0] == "Hueco":
                return False


        #Caso q quiera swappear un hueco
        else:
            #Si arranca el dia en un hueco
            if turnoChequear == 0:
                for modulo in range(moduloChequear):
                    if horariosChequear[cursoChequear][diaChequear][turnoChequear][modulo].nombre.split("-")[0] != "Hueco":
                        break
                else:
                    return True

            #Si termina el dia en un hueco
            elif turnoChequear == len(turnos)-1:    
                for modulo in range(moduloChequear + 1, turnos[turnoChequear].cantModulos):
                    if horariosChequear[cursoChequear][diaChequear][turnoChequear][modulo].nombre.split("-")[0] != "Hueco":
                        break
                else:
                    return True

            #Si el hueco dura varios turnos hacia adelante
            for turno in range(turnoChequear,len(turnos)):
                if turno == turnoChequear:
                    for modulo in range(moduloChequear, turnos[turnoChequear].cantModulos):
                        if horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre.split("-")[0] != "Hueco": 
                            break
                    
                    else:
                        continue
                    break

                else:
                    for modulo in range(turnos[turnoChequear].cantModulos):
                        if horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre.split("-")[0] != "Hueco": 
                            break

                    else:
                        continue
                    break
            
            else:
                return True

            #Si el hueco dura varios turnos hacia atras
            for turno in range(turnoChequear + 1):
                if turno == turnoChequear:
                    for modulo in range(moduloChequear + 1):
                        if horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre.split("-")[0] != "Hueco": 
                            break
                    
                    else:
                        continue
                    break
                
                else:
                    for modulo in range(turnos[turnoChequear].cantModulos):
                        if horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre.split("-")[0] != "Hueco": 
                            break

                    else:
                        continue
                    break

            else:
                return True

            return False
            
        #Casos normales
        repticionesModulos = 0
        huecoBool = False
        turnoBool = False
        for turno in range(len(turnos)):
            for modulo in range(turnos[turno].cantModulos):
                if horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre == materiaChequear.nombre and (huecoBool or turnoBool):
                    return False

                elif horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre == materiaChequear.nombre:
                    repticionesModulos += 1
                
                elif repticionesModulos > 0:
                    huecoBool = True
            if repticionesModulos > 0:
                turnoBool = True
            
        if repticionesModulos > materiaChequear.modulosContinuos:
            return False
        
        return True

    def imprimirHorario(horariosImrimir, curso, diaS, turnoS, moduloS, diaSwap, turnoSwap, moduloSwap):
        print("Curso "+ str(curso) + " - " + horariosImrimir[cursos.index(curso)][diaS][turnoS][moduloS].nombre)
        for turno in range(len(turnos)):
            for modulo in range(turnos[turno].cantModulos):
                moduloPrint = ""
                for dia in range(5):
                    if (turno == turnoS and modulo == moduloS and dia == diaS) or (turno == turnoSwap and modulo == moduloSwap and dia == diaSwap):
                        moduloPrint += '\033[93m ' + horariosImrimir[cursos.index(curso)][dia][turno][modulo].nombre + '\033[0m '

                    else:
                        moduloPrint += " " + horariosImrimir[cursos.index(curso)][dia][turno][modulo].nombre + " "

                print(moduloPrint)
            print()
        print()
        print()

    # Todas las validaciones y resticciones se implementan aca
    def swapValido(horariosAValidar, posMateria1, posMateria2, posibleProfesor, aula):

        materia1 = horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
        materia2 = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo]
        
        #disponibilidad profesores
        if not profesorDisponible(materiasProfesores[materia2.nombre], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
            return False

        if not profesorDisponible(posibleProfesor, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
            return False
        
        #disponibilidad aulas
        if not aulaDisponible(horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
            return False

        if not aulaDisponible(aula, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
            return False

        #continiudad modulos
            #swap temporal para probar si qda bien
        horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]

        if not validarModulosContinuos(horariosAValidar, posMateria1.curso, posMateria1.dia, posMateria1.turno, posMateria1.modulo):
            #saco el swap temporal
            horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
            return False

        if not validarModulosContinuos(horariosAValidar, posMateria2.curso, posMateria2.dia, posMateria2.turno, posMateria2.modulo):
            #saco el swap temporal
            horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
            return False

            #saco el swap temporal
        horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]

        #Resticciones extras ACA

        return True

    #Inicializo las posiciones de los horarios
    horarios = []
    for i in range(len(cursos)):
        horarios.append([])
        for j in range(len(dias)):
            horarios[i].append([])
            for k in range(len(turnos)):
                horarios[i][j].append([])
                for _ in range(turnos[k].cantModulos):
                    horarios[i][j][k].append(None)

    #Inicializo las posciciones de las materias
    materiasProfesores = {}
    for materia in materias:
        materiasProfesores[materia.nombre] = None

    #Inicializo las posiciones de las aulas
    horariosAulas = []
    for i in range(len(cursos)):
        horariosAulas.append([])
        for j in range(len(dias)):
            horariosAulas[i].append([])
            for k in range(len(turnos)):
                horariosAulas[i][j].append([])
                for _ in range(turnos[k].cantModulos):
                    horariosAulas[i][j][k].append(None)

    #Copia para poder ir restando los modulos
    copiaMaterias = copy.deepcopy(materias)

    #Inserto en horarios, las materias siempre y cuando el profe este disponible, tmb actualizo materiasProfesores y horariosAulas
    for curso in cursos:
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    for materia in copiaMaterias:
                        #Chequea que la materia corresponda al curso, que le falten modulos, que el profesor de la materia sea nulo o el que esta comparando y que el profesor este disponible
                        if materia.curso == curso and materia.cantModulos > 0:
                            #Obtengo el objeto materia y lo guardo en horarios
                            for materiaOriginal in materias:
                                if materiaOriginal.nombre == materia.nombre:
                                    horarios[cursos.index(curso)][dia][turno][modulo] = materiaOriginal
                                    materia.cantModulos -= 1  
                                    break

                            #Actualizo el profe
                            if materiasProfesores[materia.nombre] is None:
                                materiasProfesores[materia.nombre] = materia.posibleProfesores[0]
                                
                            #Actualizo el aula
                            horariosAulas[cursos.index(curso)][dia][turno][modulo] = materia.posiblesAulas[0]
                            break
                        
    #Una vez generado el horario inical toca arreglarlo
    #Primero relleno los huecos con las materias q me cantFaltante
    for materia in copiaMaterias:
        if materia.cantModulos > 0:
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horarios[cursos.index(materia.curso)][dia][turno][modulo] is None:
                            for materiaOriginal in materias:
                                if materiaOriginal.nombre == materia.nombre:
                                    horarios[cursos.index(materia.curso)][dia][turno][modulo] = materiaOriginal
                                    materia.cantModulos -= 1  
                                    break
                        if materia.cantModulos == 0:
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break

    #Cambio los none por materias hueco
    for curso in range(len(cursos)):
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    if horarios[curso][dia][turno][modulo] == None:
                        horarios[curso][dia][turno][modulo] = materias[len(materias)-1-curso]
                        horariosAulas[curso][dia][turno][modulo] = aulas[-1]

        materiasProfesores[materias[len(materias)-1-curso].nombre] = profesores[-1]


    #Hay que asignar un profesor a las materias que no lo tengan, pero no se puede hacer sin q se superpongan, x lo q habria q emepzar a swappear las materias del horario
    def swap(horarios):
        for materia in materias:
            if materia.nombre.split('-')[0] == "Hueco":
                break

            posiblesProfesoresOrdenadosMap = {}
            posiblesProfesoresOrdenados = []

            for posibleProfesor in materia.posibleProfesores:
                posiblesProfesoresOrdenadosMap[posibleProfesor] = 0
                for materiaProfesor in materiasProfesores.values():
                    if materiaProfesor == posibleProfesor:
                        posiblesProfesoresOrdenadosMap[posibleProfesor] += 1

            for _ in range(len(materia.posibleProfesores)):
                posiblesProfesoresOrdenados.append(min(posiblesProfesoresOrdenadosMap.items(), key=operator.itemgetter(1))[0])
                del posiblesProfesoresOrdenadosMap[min(posiblesProfesoresOrdenadosMap.items(), key=operator.itemgetter(1))[0]]        

            for posibleProfesor in posiblesProfesoresOrdenados:
                #me guardo una copia para swappear tranqui
                copiaHorarios = copy.deepcopy(horarios)
                #buscar la materia en el horario 
                for dia in range(len(dias)):
                    for turno in range(len(turnos)):
                        for modulo in range(turnos[turno].cantModulos):
                            posMateria1 = Posicion(cursos.index(materia.curso), dia, turno, modulo)
                            
                            #pruebo swappear todos los modulos que tengan un error (swwap valido sobre si mismo sirve para eso)
                            if horarios[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo].nombre == materia.nombre and not swapValido(copiaHorarios, posMateria1, posMateria1, materiasProfesores[materia.nombre], horariosAulas[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]):
                                for diaSwap in range(len(dias)):
                                    for turnoSwap in range(len(turnos)):
                                        for moduloSwap in range(turnos[turnoSwap].cantModulos):
                                            for posibleAula in materia.posiblesAulas:
                                                materiaSwap = copiaHorarios[cursos.index(materia.curso)][diaSwap][turnoSwap][moduloSwap]
                                                posMateria2 = Posicion(cursos.index(materiaSwap.curso), diaSwap, turnoSwap, moduloSwap)
                                                #chequeo si el swap es valido
                                                if materiaSwap.nombre != materia.nombre:     
                                                    if swapValido(copiaHorarios, posMateria1, posMateria2, posibleProfesor, posibleAula):
                                                        copiaHorarios[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], copiaHorarios[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = copiaHorarios[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], copiaHorarios[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
                                                        horariosAulas[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], posibleAula
                                                        break
                                    
                                            else:
                                                continue
                                            break
                                        
                                        else:
                                            continue
                                        break
                                                    
                                    #la cadena de abajo de los else break continue, chequea si se realizo o no un swap, si no se hizo, significa q no soluciono, es deci q este profe no sirve
                                    else:
                                        continue
                                    break
                                else:
                                    break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                
                else:
                    horarios = copy.deepcopy(copiaHorarios)
                    materiasProfesores[materia.nombre] = posibleProfesor
                    break
        return horarios

    #Hay q cambiar el numero por, hasta q se arregle
    iteraciones = 100

    from os import system

    while iteraciones > 0:
        horarios = swap(horarios)
        # system("clear")
        for curso in range(len(cursos)):
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        posicion = Posicion(curso, dia, turno, modulo)
                        if not swapValido(horarios, posicion, posicion, None, None):
                            swapValido(horarios, posicion, posicion, None, None)
                            # system("clear")
                            # imprimirHorario(horarios, cursos[curso], dia, turno, modulo, dia, turno, modulo)
                            # input()
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            iteraciones = 0
        iteraciones -= 1
        print (iteraciones)

    #devuelve las posibles posiciones donde se puede poner una materia para que este cerca de otra
    def checkearPosicionValidaMinimos(horarios, materia):
        posiblesPosiciones = []
        for curso in range(len(cursos)):
            for dia in range(5): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horarios[curso][dia][turno][modulo].nombre == materia.nombre:
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo >= 0:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo + cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                            if cantidadModulos < horarios[curso][dia][turno][modulo].modulosContinuos:
                                if modulo == 0:
                                    if (horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre):
                                        posiblesPosiciones.append([curso, dia, turno, modulo + 1])
                                elif modulo + 1 == turnos[turno].cantModulos:
                                    if (horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre):
                                        posiblesPosiciones.append([curso, dia, turno, modulo - 1])
                                elif (horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre or horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre):
                                    if horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre:
                                        posiblesPosiciones.append([curso, dia, turno, modulo + 1])
                                    if horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre:
                                        posiblesPosiciones.append([curso, dia, turno, modulo - 1])
        return posiblesPosiciones


    def buscarEspaciosVacios(horarios, curso):
        posiblesPosiciones = []

        for dia in range(len(dias)): 
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    if horarios[curso][dia][turno][modulo].nombre.split('-')[0] == "Hueco":
                        posiblesPosiciones.append([curso, dia, turno, modulo])

        return posiblesPosiciones
    # def buscarTurnosVacios(horarios, curso):
    #     posiblesPosiciones = []
    #     noVacio = True
    #     for dia in range(len(dias)): 
    #         for turno in range(len(turnos)):
    #             noVacio = True
    #             for modulo in range(turnos[turno].cantModulos):
    #                 if horarios[curso][dia][turno][modulo].nombre.split('-')[0] != "Hueco":
    #                     noVacio = False
    #                     break
    #             if noVacio:
    #                 posiblesPosiciones.append([curso, dia, turno])
                        

    #     return posiblesPosiciones
    # print(buscarTurnosVacios(horarios, 2))
                            
    boolAgrupador = True
    interacion = 0
    while boolAgrupador:
        interacion = interacion + 1
        horariosPrueba = copy.deepcopy(horarios)
        for curso in range(len(cursos)):
            for dia in range(len(dias)): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horarios[curso][dia][turno][modulo].nombre.split('-')[0] != "Hueco":
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo >= 0:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo + cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                            
                            if cantidadModulos < 5:
                                posibles = checkearPosicionValidaMinimos(horarios, horarios[curso][dia][turno][modulo])
                                desplazado = False
                                for posiblePosicion in posibles:
                                    if (profesorDisponible(materiasProfesores[horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]].nombre], horariosPrueba, dia, turno, modulo, curso) and profesorDisponible(materiasProfesores[horariosPrueba[curso][dia][turno][modulo].nombre], horariosPrueba, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], posiblePosicion[0])):
                                        if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosPrueba, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horariosPrueba, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], cursos[posiblePosicion[0]])):
                                    
                                            horariosPrueba[curso][dia][turno][modulo], horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosPrueba[curso][dia][turno][modulo]
                                            if validarModulosContinuos(horariosPrueba, posiblePosicion[0], posiblePosicion[1], posiblePosicion[2], posiblePosicion[3]) and validarModulosContinuos(horariosPrueba, curso, dia, turno, modulo):
                                                
                                                    horariosAulas[curso][dia][turno][modulo], horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosAulas[curso][dia][turno][modulo]
                                            
                                                    horarios = copy.deepcopy(horariosPrueba)
                                                    desplazado = True
                                            else:
                                                    horariosPrueba = copy.deepcopy(horarios)
                                if not desplazado and cantidadModulos == 1:
                                    for modulo2 in range(turnos[turno].cantModulos):
                                        if (profesorDisponible(materiasProfesores[horariosPrueba[curso][dia][turno][modulo2].nombre], horariosPrueba, dia, turno, modulo, curso) and profesorDisponible(materiasProfesores[horariosPrueba[curso][dia][turno][modulo].nombre], horariosPrueba, dia, turno, modulo2, curso)):
                                            if (aulaDisponible(horariosAulas[curso][dia][turno][modulo2], horariosPrueba, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horariosPrueba, dia, turno, modulo2, cursos[curso])):
                                                horariosPrueba[curso][dia][turno][modulo], horariosPrueba[curso][dia][turno][modulo2] = horariosPrueba[curso][dia][turno][modulo2], horariosPrueba[curso][dia][turno][modulo]
                                                if validarModulosContinuos(horariosPrueba, curso, dia, turno, modulo2) and validarModulosContinuos(horariosPrueba, curso, dia, turno, modulo):

                                                    horariosAulas[curso][dia][turno][modulo], horariosAulas[curso][dia][turno][modulo2] = horariosAulas[curso][dia][turno][modulo2], horariosAulas[curso][dia][turno][modulo]

                                                    horarios = copy.deepcopy(horariosPrueba)
                                                    desplazado = True
                                                else:
                                                    horariosPrueba = copy.deepcopy(horarios)
                                    if not desplazado:
                                        posibles = buscarEspaciosVacios(horarios, curso)
                                        for posiblePosicion in posibles:
                                            if (profesorDisponible(materiasProfesores[horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]].nombre], horariosPrueba, dia, turno, modulo, curso) and profesorDisponible(materiasProfesores[horariosPrueba[curso][dia][turno][modulo].nombre], horariosPrueba, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], posiblePosicion[0])):
                                                if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosPrueba, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horariosPrueba, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], cursos[posiblePosicion[0]])):
                                            
                                                    horariosPrueba[curso][dia][turno][modulo], horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosPrueba[curso][dia][turno][modulo]
                                                    if validarModulosContinuos(horariosPrueba, posiblePosicion[0], posiblePosicion[1], posiblePosicion[2], posiblePosicion[3]) and validarModulosContinuos(horariosPrueba, curso, dia, turno, modulo):
                                                        
                                                            horariosAulas[curso][dia][turno][modulo], horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosAulas[curso][dia][turno][modulo]
                                                    
                                                            horarios = copy.deepcopy(horariosPrueba)
                                                            desplazado = True
                                                    else:
                                                            horariosPrueba = copy.deepcopy(horarios)
                                    # if not desplazado:
                                    #     posibles = buscarTurnosVacios(horarios, curso)
                                    #     for posiblePosicion in posibles:
                                    #         if (profesorDisponible(materiasProfesores[horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0].nombre], horariosPrueba, dia, turno, modulo, curso) and profesorDisponible(materiasProfesores[horariosPrueba[curso][dia][turno][modulo].nombre], horariosPrueba, posiblePosicion[1], posiblePosicion[2], 0, posiblePosicion[0])):
                                    #             if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0], horariosPrueba, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horariosPrueba, posiblePosicion[1], posiblePosicion[2], 0, cursos[posiblePosicion[0]])):
                                            
                                    #                 horariosPrueba[curso][dia][turno][modulo], horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0] = horariosPrueba[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0], horariosPrueba[curso][dia][turno][modulo]
                                    #                 if validarModulosContinuos(horariosPrueba, posiblePosicion[0], posiblePosicion[1], posiblePosicion[2], 0) and validarModulosContinuos(horariosPrueba, curso, dia, turno, modulo):
                                                        
                                    #                         horariosAulas[curso][dia][turno][modulo], horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0] = horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][0], horariosAulas[curso][dia][turno][modulo]
                                                    
                                    #                         horarios = copy.deepcopy(horariosPrueba)
                                    #                         desplazado = True
                                    #                 else:
                                    #                         horariosPrueba = copy.deepcopy(horarios)
                                        
    
        casillerosLibres = True
        for curso in range(len(cursos)):
            for dia in range(len(dias)): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horarios[curso][dia][turno][modulo].nombre.split('-')[0] != "Hueco":
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo >= 0:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo + cuentaModulo].nombre:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                        if cantidadModulos == 1 and horarios[curso][dia][turno][modulo].cantModulos:
                            casillerosLibres = False
        if casillerosLibres or interacion == 100:
            boolAgrupador = False

    def checkearPosicionValidaMinimosAulas(horarios, aula):
        posiblesPosiciones = []
        for curso in range(len(cursos)):
            for dia in range(5): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horariosAulas[curso][dia][turno][modulo] == aula:
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo > 0:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo - cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo + cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                            if modulo == 0:
                                if (horariosAulas[curso][dia][turno][modulo + 1] != aula):
                                    posiblesPosiciones.append([curso, dia, turno, modulo + 1])
                            elif modulo + 1 == turnos[turno].cantModulos:
                                if (horariosAulas[curso][dia][turno][modulo - 1] != aula):
                                    posiblesPosiciones.append([curso, dia, turno, modulo - 1])
                            elif (horariosAulas[curso][dia][turno][modulo + 1] != aula or horariosAulas[curso][dia][turno][modulo - 1] != aula):
                                if horariosAulas[curso][dia][turno][modulo + 1] != aula:
                                    posiblesPosiciones.append([curso, dia, turno, modulo + 1])
                                if horariosAulas[curso][dia][turno][modulo - 1] != aula:
                                    posiblesPosiciones.append([curso, dia, turno, modulo - 1])
        return posiblesPosiciones



    boolAgrupador = True
    interacion = 0
    while boolAgrupador:
        interacion = interacion + 1
        horariosPrueba = copy.deepcopy(horarios)
        for curso in range(len(cursos)):
            for dia in range(len(dias)): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horariosAulas[curso][dia][turno][modulo] != "Hueco":
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo > 0:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo - cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo + cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                            
                            posibles = checkearPosicionValidaMinimosAulas(horariosAulas, horariosAulas[curso][dia][turno][modulo])
                            desplazado = False
                            for posiblePosicion in posibles:
                                if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosPrueba, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horariosPrueba, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], cursos[posiblePosicion[0]])):
                                    if horariosAulas[curso][dia][turno][modulo] in horarios[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]].posiblesAulas and horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] in horarios[curso][dia][turno][modulo].posiblesAulas:
                                        horariosAulas[curso][dia][turno][modulo], horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosAulas[curso][dia][turno][modulo]
                                        desplazado = True
                            
                            if not desplazado and cantidadModulos == 1:
                                for modulo2 in range(turnos[turno].cantModulos):
                                    if (aulaDisponible(horariosAulas[curso][dia][turno][modulo2], horarios, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo2, cursos[curso])):
                                        if horariosAulas[curso][dia][turno][modulo] in horarios[curso][dia][turno][modulo2].posiblesAulas and horariosAulas[curso][dia][turno][modulo2] in horarios[curso][dia][turno][modulo].posiblesAulas:
                                            horariosAulas[curso][dia][turno][modulo], horariosAulas[curso][dia][turno][modulo2] = horariosAulas[curso][dia][turno][modulo2], horariosAulas[curso][dia][turno][modulo]
                                            desplazado = True
                            

        casillerosLibres = True
        for curso in range(len(cursos)):
            for dia in range(len(dias)): 
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horariosAulas[curso][dia][turno][modulo] != "Hueco":
                            cantidadModulos = 0
                            for cuentaModulo in range(turnos[turno].cantModulos):
                                if modulo - cuentaModulo >= 0:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo - cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                                if modulo + cuentaModulo < turnos[turno].cantModulos:
                                    if horariosAulas[curso][dia][turno][modulo] == horariosAulas[curso][dia][turno][modulo + cuentaModulo]:
                                        cantidadModulos = cantidadModulos + 1
                            cantidadModulos = cantidadModulos - 1 #Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
                        if cantidadModulos == 1:
                            casillerosLibres = False
        if casillerosLibres or interacion == 100:
            boolAgrupador = False

    for curso in range(len(cursos)):
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    materia = horarios[curso][dia][turno][modulo]
                    if materia.nombre.split('-')[0] == "Hueco":
                        break
                    if horariosAulas[curso][dia][turno][modulo] not in materia.posiblesAulas:
                        print(materia.nombre, horariosAulas[curso][dia][turno][modulo])
                    if aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo, curso):
                        print(materia.nombre, horariosAulas[curso][dia][turno][modulo])

    # horarioAux = []
    # for i in range(len(cursos)):
    #     horarioAux.append([])
    #     for j in range(len(dias)):
    #         horarioAux[i].append([])
    #         for k in range (len(turnos)):
    #             horarioAux[i][j].append([])
    #             for l in range(turnos[k].cantModulos):
    #                 if horarios[i][j][k][l].nombre.split('-')[0] == "Hueco":
    #                     horarioAux[i][j][k].append("")
    #                 else:
    #                     horarioAux[i][j][k].append(horarios[i][j][k][l].nombre.split("-")[0] + " - " + materiasProfesores[horarios[i][j][k][l].nombre] + " - " + horariosAulas[i][j][k][l])


    # horariosColores = []
    # for i in range(len(cursos)):
    #     horariosColores.append([])
    #     for j in range(len(dias)):
    #         horariosColores[i].append([])
    #         for k in range (len(turnos)):
    #             for l in range(turnos[k].cantModulos):
    #                 horariosColores[i][j].append(horarios[i][j][k][l].color)
    #             if k != len(turnos)-1:
    #                 horariosColores[i][j].append("white")
                
    # for i in range(len(cursos)):
    #     fig = go.Figure(data=[go.Table(
    #     header = dict(values=['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes'],
    #                 line_color='darkslategray',
    #                 fill_color='lightskyblue',
    #                 align='left'),
    #     cells = dict(values=[
    #                         horarioAux[i][0][0]+[""]+horarioAux[i][0][1],
    #                         horarioAux[i][1][0]+[""]+horarioAux[i][1][1],
    #                         horarioAux[i][2][0]+[""]+horarioAux[i][2][1],
    #                         horarioAux[i][3][0]+[""]+horarioAux[i][3][1],
    #                         horarioAux[i][4][0]+[""]+horarioAux[i][4][1]
    #                         ],
    #                 line_color='darkslategray',
    #                 fill_color= horariosColores[i],
    #                 align='left'))
    #     ])

    #     fig.update_layout(width=1000, height=1000)
    #     fig.show()
    return horarios, materiasProfesores, horariosAulas

@app.route('/')
def hello_world():
    return "a"

@app.route('/ayuda', methods=['POST'])
def a():
    idColegio = request.form.get('id')
    def math_fun():
        # The sleep here is simply to make it clear that this happens in the background
        sleep(1) 
        runAlgorithm(idColegio)


    def fun():
        # Create thread to run math_fun for each argument in x 
        t = threading.Thread(target=math_fun)
        t.setDaemon(False)
        t.start()
        print("Ejecutado prro")

    fun()
    return idColegio

@app.route('/algoritmo')
def runAlgorithm(id = "hTbz9pWNNHSlif1LAvpVRxEwM6zCF1Npws8Mm58SH0uIdV1cagrwMkwZCokQvV"):
    print(id)
    doc_ref = db.collection(u'schools').document(u'hTbz9pWNNHSlif1LAvpVRxEwM6zCF1Npws8Mm58SH0uIdV1cagrwMkwZCokQvV')
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data:')
    else:
        return(u'No such document!')

    #docDiccionario es un diccionario de la escuela
    docDiccionario = doc.to_dict()
    print(docDiccionario)
    aulas = []
    profesores = []
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    cursos = []
    turnos = []
    materias = []

    [cursos.append(i.get("nombre")) for i in docDiccionario["cursos"]]
    [aulas.append(i.get("nombre")) for i in docDiccionario["aulas"]]
    [profesores.append(i.get("nombre")) for i in docDiccionario["profesores"]]
    for i in docDiccionario["turnos"]:
        nombreT = str(i.get("turno"))
        cantidadModulosT = len(i.get("modulos"))
        t = Turno(nombreT, cantidadModulosT)
        turnos.append(t)
    for i in docDiccionario["materias"]:
        nombreM = i.get("nombre")
        cursoM = i.get("curso")
        posiblesProfesoresM = []
        for j in i.get("profesoresCapacitados"):
            if j == True:
                print("a")
        cantidadDeModulosTotalM = i.get("cantidadDeModulosTotal")
        cantidadMaximaDeModulosPorDiaM = i.get("cantidadMaximaDeModulosPorDia")
        a = Materia(nombreM, cursoM, posiblesProfesoresM, aulas, cantidadDeModulosTotalM, cantidadMaximaDeModulosPorDiaM, "red")
        materias.append(a)

    try:
        horarios, materiasProfesores, horariosAulas = algoritmo(aulas, profesores, dias, cursos, turnos, materias)
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
    
    hora = str(datetime.now())
    
    diccionario2 = {"horarios":horariosDiccionario, "materiasProfesores":materiasProfesores, "horariosAulas":horariosAulasDiccionario}
    escribir(diccionario2, hora)
    return hora

def idGenerator():

    doc_ref = db.collection(u'school').document()
    return doc_ref.id

def escribir(my_data, hora):
    data = {hora:my_data}
    doc_ref = db.collection(u'horariosHechos').document()
    doc_ref.set(data)
    print(data)
    try:
        id = idGenerator()
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

def enviarEscuelaAlAlgoritmo(id):

    #doc_ref = db.collection(u'school').document(u'lhrtFyMTfLFawLGOtp3J')

    #doc = doc_ref.get()
    #schoolR = School.from_dict()   #hay que hacer una funcion para poder traducir lo que llega de doc a School
    doc_ref = db.collection(u'schools').document(id)

    #docDiccionario es un diccionario de la escuela
    doc = doc_ref.get()
    docDiccionario = doc.to_dict()
    profesores = []
    cursos = []
    materias = []
    turnos = []
    cantModulosPorDia = docDiccionario["cantModulosPorDia"]
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]
    for i in docDiccionario["profesores"].keys():
        profesores.append(docDiccionario['profesores'].get(i))
    for i in docDiccionario["cursos"].keys():
        cursos.append(docDiccionario['cursos'].get(i))
    for i in docDiccionario["turnos"].key():
        nombreT = str(docDiccionario["turnos"].get(i).get("turno"))
        cantidadModulosT = int(docDiccionario["materias"].get(i).get("cantModulos"))
        t = Turno(nombreT, cantidadModulosT)
        print(t)
        turnos.append(t)
    for i in docDiccionario["materias"].keys():
        nombreM = str(docDiccionario["materias"].get(i).get("nombre"))
        cursoM = str(docDiccionario["materias"].get(i).get("curso"))
        cantidadModulosTotalM = docDiccionario["materias"].get(i).get("cantidadDeModulosTotal")
        cantModulosPorDiaM = docDiccionario["materias"].get(i).get("cantidadMaximaDeModulosPorDia")
        profesoresM = []
        for j in docDiccionario["materias"].get(i).get("profesoresCapacitados"):
            profesoresM.append(docDiccionario["materias"].get(i).get("profesoresCapacitados").get(j))
        a = Materia(nombreM,cursoM, profesoresM,cantidadModulosTotalM, cantModulosPorDiaM)
        materias.append(a)  
        #main(cursos,turnos,materias,dias,profesores)
    try:
        id = request.json['id']
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 3304))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)

#fijarse cuando se sube algo
#importar algoritmo

