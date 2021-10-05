import copy

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

def algoritmo(aulas, profesores, dias, cursos, turnos, materias, disponibilidadProfesores):    
    
    #ordenar materias por modulosContinuos
    for curso in range(len(cursos)):
        materias[curso] = sorted(materias[curso], key=lambda materia: materia.modulosContinuos)

    def posiblesPosiciones(horarios, materia):
        posiblesPosiciones = []
        for curso in range(len(cursos)):
            for dia in range(5):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if horarios[curso][dia][turno][modulo].nombre == materia.nombre:
                            cantidadModulos = contarModulos(
                                horarios, dia, horarios[curso][dia][turno][modulo])
                            if cantidadModulos < horarios[curso][dia][turno][modulo].modulosContinuos:
                                if modulo == 0:
                                    if (horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre):
                                        posiblesPosiciones.append(
                                            [curso, dia, turno, modulo + 1])
                                elif modulo + 1 == turnos[turno].cantModulos:
                                    if (horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre):
                                        posiblesPosiciones.append(
                                            [curso, dia, turno, modulo - 1])
                                elif (horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre or horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre):
                                    if horarios[curso][dia][turno][modulo + 1].nombre != materia.nombre:
                                        posiblesPosiciones.append(
                                            [curso, dia, turno, modulo + 1])
                                    if horarios[curso][dia][turno][modulo - 1].nombre != materia.nombre:
                                        posiblesPosiciones.append(
                                            [curso, dia, turno, modulo - 1])
        return posiblesPosiciones

    # Funcion que revisa si en determinado modulo, el profesor esta disponible
    def profesorDisponible(profesor, horarioVerificar, dia, turno, modulo, cursoExcepcion):
        for curso in cursos:
            if curso != cursoExcepcion:
                if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre.split('-')[0] != "Hueco" and materiasProfesores[horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre] == profesor:
                    return False
        if not profesor in disponibilidadProfesores[dia][turno][modulo]:
            return False
        return True

    # Cuenta los modulos de determinada materia en determinado dia
    def contarModulos(horarios, dia, materia):
        cantidadModulos = 0
        for turno in range(len(turnos)):
            for cuentaModulo in range(turnos[turno].cantModulos):
                if materia.nombre == horarios[cursos.index(materia.curso)][dia][turno][cuentaModulo].nombre:
                    cantidadModulos = cantidadModulos + 1
        return cantidadModulos

    # Se asegura de que no haya modulos de materias en otros turnos
    def validarModulosTurno(horarios, dia, materia):
        for turno in range(len(turnos)):
            for modulo in range(turnos[turno].cantModulos):
                if materia.nombre == horarios[cursos.index(materia.curso)][dia][turno][modulo].nombre:
                    return False
        return True

    # Encuentra la division del horario segun materias
    def encontrarBloquesMaterias(horarios):
        posiblesPosiciones = []
        for curso in range(len(cursos)):
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        if modulo != 0 and horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - 1].nombre and "Hueco" not in horarios[curso][dia][turno][modulo].nombre:
                            posiblesPosiciones[len(
                                posiblesPosiciones) - 1].append([curso, dia, turno, modulo])
                        else:
                            posiblesPosiciones.append([])
                            posiblesPosiciones[len(
                                posiblesPosiciones) - 1].append([curso, dia, turno, modulo])
        return posiblesPosiciones




    def swapValido(horariosAValidar, posMateria1, posMateria2, posibleProfesor, aula):

        materia1 = horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
        materia2 = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo]
        
        materia2Valida = False

        if posMateria1 != posMateria2:
            materia2Valida = swapValido(horariosAValidar, posMateria2, posMateria2, materiasProfesores[materia2.nombre], horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo])

        #disponibilidad profesores
        if materia2Valida and not profesorDisponible(materiasProfesores[materia2.nombre], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
            return False

        if not profesorDisponible(posibleProfesor, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
            return False
        
        #disponibilidad aulas
        if materia2Valida and not aulaDisponible(horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
            return False

        if not aulaDisponible(aula, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
            return False

        #continiudad modulos
            #swap temporal para probar si qda bien
        horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]

        if materia2Valida and not validarModulosContinuos(horariosAValidar, posMateria1.curso, posMateria1.dia, posMateria1.turno, posMateria1.modulo):
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


    def posiblesSwapsRecursivo(horarios, bloqueMateria, cantidadARellenar):

        def adyacente(bloque1, bloque2):
            curso1 = bloque1[0][0]
            dia1 = bloque1[0][1]
            turno1 = bloque1[0][2]
            curso2 = bloque2[0][0]
            dia2 = bloque2[0][1]
            turno2 = bloque2[0][2]
            if curso1 == curso2 and turno1 == turno2 and dia1 == dia2 and (bloque1[len(bloque1) - 1][3] == bloque2[0][3] - 1 or bloque2[len(bloque2) - 1][3] == bloque1[0][3] - 1):
                return True
            return False


        bloquesASumar = []
        bloques = encontrarBloquesMaterias(horarios)
        for bloque in bloques:
            if bloque == bloqueMateria:
                continue
            largoPosible = len(bloque)
            if cantidadARellenar < largoPosible:
                continue
            if not adyacente(bloqueMateria, bloque):
                continue
            if cantidadARellenar > largoPosible:
                if bloque not in bloquesASumar:
                    bloquesASumar.append( bloque )
                for i in posiblesSwapsRecursivo(horarios, bloque, cantidadARellenar - largoPosible):
                    if i not in bloquesASumar:
                        bloquesASumar.append(i)
            elif cantidadARellenar == largoPosible:
                bloquesASumar.append( bloque )
                return bloquesASumar
        suma = 0
        for i in bloquesASumar:
            suma += len(i)
        if suma == cantidadARellenar:
            return bloquesASumar
        else:
            return []


        



    def posiblesSwaps(horarios, bloqueMateria):
        posibilidades = []
        curso = bloqueMateria[0][0]
        bloques = encontrarBloquesMaterias(horarios)
        largo = len(bloqueMateria)
        for bloque in bloques:
            if bloque == bloqueMateria:
                continue
            largoPosible = len(bloque)
            if largo < largoPosible:
                continue
            cursoPosible = bloque[0][0]
            if curso != cursoPosible:
                continue
            if largo > largoPosible:
                si = False
                a = False
                bloquesASumar = []
                for bloqueASumar in posiblesSwapsRecursivo(horarios,bloque,largo - largoPosible):
                    if bloqueASumar != []:
                        if bloqueASumar not in bloquesASumar :    
                            bloquesASumar.append(bloqueASumar)
                            si = True
                if si: 
                    for modulo in bloque:
                        if modulo not in bloquesASumar : 
                            a = True
                    if a:
                        bloquesASumar.append( bloque)
                        posibilidades.append([])
                        posibilidades[len(posibilidades) - 1] += bloquesASumar
            else:
                posibilidades.append([])
                posibilidades[len(posibilidades) - 1] += [bloque]
        return posibilidades

    def combinacionesSwapRecursivo(horarios, bloques, combinacionesDeSwap):
        cantBloques = len(bloques)
        cantPosibilidades = math.factorial( cantBloques)
        for i in range(cantBloques):
            opciones = copy.deepcopy(bloques)
            combinacionesDeSwap.append(combinacionesDeSwap[len(combinacionesDeSwap) - 1])
            combinacionesDeSwap[len(combinacionesDeSwap) - 1].append(bloques[i])
            opciones.remove(bloques[i])
            combinacionesSwapRecursivo(horarios, opciones, combinacionesDeSwap)
        return combinacionesDeSwap



    #Falta terminar
    def combinacionesSwap(horarios, bloques):
        return bloques


    #Encuentra, dentro de un curso, el turno con mas huecos
    def encontrarTurnoConMasEspacios(horarios, curso):
        turnoDefinitivo = []
        mayor = 0
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                cuentaHuecos = 0
                for modulo in range(turnos[turno].cantModulos):
                    if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
                        cuentaHuecos += 1
                if 0 == mayor or mayor < cuentaHuecos:
                    turnoDefinitivo = [dia, turno]

        return turnoDefinitivo

    # Chekea que todo este bien, que el horario actual sea valido segun todos los parametros establecidos, se puede enviar un bool para ignorar ciertos parametros
    def checkeo(boolAulas = True, boolProfesores = True, boolModulosContinuos = True):
        for curso in range(len(cursos)):
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        materia = horarios[curso][dia][turno][modulo]
                        if "Hueco" in materia.nombre:
                            break
                        if horariosAulas[curso][dia][turno][modulo] not in materia.posiblesAulas and boolAulas:
                            print("Aula no disponible: " + materia.nombre,
                                horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
                            return False
                        if not aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo, curso) and boolAulas:
                            print("Aula no disponible: " + materia.nombre,
                                horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
                            return False
                        if not profesorDisponible(materiasProfesores[horarios[curso][dia][turno][modulo].nombre], horarios, dia, turno, modulo, curso) and boolProfesores:
                            print("Profesor no disponible: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
                            return False
                        if not validarModulosContinuos(horarios, curso, dia, turno, modulo) and boolModulosContinuos:
                            print("Modulos continuos: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
                            return False
                        if contarModulosTotal(horarios, materia) != materia.cantModulos and boolModulosContinuos:
                            print("Modulos continuos: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
                            return False
        return True

    def checkeoSinReturn(boolAulas = True, boolProfesores = True, boolModulosContinuos = True):
        for curso in range(len(cursos)):
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for modulo in range(turnos[turno].cantModulos):
                        materia = horarios[curso][dia][turno][modulo]
                        if "Hueco" in materia.nombre:
                            break
                        if horariosAulas[curso][dia][turno][modulo] not in materia.posiblesAulas and boolAulas:
                            print("Aula no disponible: " + materia.nombre,
                                horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
                        if not aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo, curso) and boolAulas:
                            print("Aula no disponible: " + materia.nombre,
                                horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
                        if not profesorDisponible(materiasProfesores[horarios[curso][dia][turno][modulo].nombre], horarios, dia, turno, modulo, curso) and boolProfesores:
                            print("Profesor no disponible: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
                        if not validarModulosContinuos(horarios, curso, dia, turno, modulo) and boolModulosContinuos:
                            print("Modulos continuos: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
                        if contarModulosTotal(horarios, materia) != materia.cantModulos and boolModulosContinuos:
                            print("Modulos continuos: " + materia.nombre,
                                materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)

    # Revisa que todas las materias hayan alcanzado los modulos maximos y no se pasen
    def todosPuestos(horarios):
        for curso in range(len(cursos)):
            for materia in materias[curso]:
                if "Hueco" in materia.nombre:
                    continue

                if contarModulosTotal(horarios, materia) < materia.cantModulos:
                    print(materia.nombre)
                    return False
        return True

    def validarModulosContinuos(horariosChequear, cursoChequear, diaChequear, turnoChequear, moduloChequear):
        materiaChequear = horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear]

        # Chequeo q no corte una materia a la mitad
        if moduloChequear != 0 and moduloChequear != turnos[turnoChequear].cantModulos - 1 and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre == horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear + 1].nombre and horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre != horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear].nombre:
            return False

        # Chequeo q no corte un hueco
        if "Hueco" not in materiaChequear.nombre :
            if turnoChequear == 0 and moduloChequear == 0 and "Hueco" in horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear + 1].nombre :
                return False
            elif turnoChequear == len(turnos) - 1 and moduloChequear == turnos[turnoChequear].cantModulos - 1 and "Hueco" in horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear - 1].nombre:
                return False

        # Caso q quiera swappear un hueco
        else:
            # Si arranca el dia en un hueco
            if turnoChequear == 0:
                for modulo in range(moduloChequear):
                    if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turnoChequear][modulo].nombre:
                        break
                else:
                    return True

            # Si termina el dia en un hueco
            elif turnoChequear == len(turnos)-1:
                for modulo in range(moduloChequear + 1, turnos[turnoChequear].cantModulos):
                    if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turnoChequear][modulo].nombre:
                        break
                else:
                    return True

            # Si el hueco dura varios turnos hacia adelante
            for turno in range(turnoChequear, len(turnos)):
                if turno == turnoChequear:
                    for modulo in range(moduloChequear, turnos[turnoChequear].cantModulos):
                        if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre :
                            break

                    else:
                        continue
                    break

                else:
                    for modulo in range(turnos[turnoChequear].cantModulos):
                        if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre :
                            break

                    else:
                        continue
                    break

            else:
                return True

            # Si el hueco dura varios turnos hacia atras
            for turno in range(turnoChequear + 1):
                if turno == turnoChequear:
                    for modulo in range(moduloChequear + 1):
                        if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre :
                            break

                    else:
                        continue
                    break

                else:
                    for modulo in range(turnos[turnoChequear].cantModulos):
                        if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre :
                            break

                    else:
                        continue
                    break

            else:
                return True

            return False

        # Casos normales
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





    # Cuenta la cantidad total de modulos en total que hay de una materia en un horario
    def contarModulosTotal(horarios, materia):
        cantidadModulos = 0
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for cuentaModulo in range(turnos[turno].cantModulos):
                    if materia.nombre == horarios[cursos.index(materia.curso)][dia][turno][cuentaModulo].nombre:
                        cantidadModulos = cantidadModulos + 1
        return cantidadModulos

    # Funcion que revisa si en determinado modulo, el aula esta disponible
    def aulaDisponible(aula, horarioVerificar, dia, turno, modulo, cursoExcepcion):
        for curso in cursos:
            if curso != cursoExcepcion:
                if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre.split('-')[0] != "Hueco" and horariosAulas[cursos.index(curso)][dia][turno][modulo] == aula:
                    return False
        return True

    #Posibles combinaciones de modulos de c/materia p/cada turno
    def combinaciones(turno, combinacion):
        suma = 0
        for n in combinacion:
            suma += n

        if suma < turno.cantModulos:
            combinacion.append(turno.cantModulos - suma)
            for iCombinacion in combinacionesTurnos[-1]:
                if sorted(combinacion) == sorted(iCombinacion):
                    break
            else:
                combinacionesTurnos[-1].append([])
                for i in combinacion:
                    combinacionesTurnos[-1][-1].append(i)

        else:
            return

        while combinacion[-1] > 1:
            combinacion[-1] -= 1
            combinaciones(turno, copy.copy(combinacion))

    #-------------------------------------------------------^Funciones^---------------------------------------------------------------------











    combinacionesTurnos = []
    for turno in turnos:
        combinacionesTurnos.append([])
        combinaciones(turno, [])

    # Inicializo las posiciones de los horarios
    horarios = []
    for i in range(len(cursos)):
        horarios.append([])
        for j in range(len(dias)):
            horarios[i].append([])
            for k in range(len(turnos)):
                horarios[i][j].append([])
                for _ in range(turnos[k].cantModulos):
                    horarios[i][j][k].append(None)

    # Inicializo las posciciones de las materias
    materiasProfesores = {} 
    for curso in range(len(cursos)):
            for materia in materias[curso]:
                materiasProfesores[materia.nombre] = None

    # Inicializo las posiciones de las aulas
    horariosAulas = []
    for i in range(len(cursos)):
        horariosAulas.append([])
        for j in range(len(dias)):
            horariosAulas[i].append([])
            for k in range(len(turnos)):
                horariosAulas[i][j].append([])
                for _ in range(turnos[k].cantModulos):
                    horariosAulas[i][j][k].append(None)


    for curso in range(len(cursos)):
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    if horarios[curso][dia][turno][modulo] == None:
                        for materia in materias[curso]:
                            if "Hueco" in materia.nombre:
                                horarios[curso][dia][turno][modulo] = materia
                                horariosAulas[curso][dia][turno][modulo] = aulas[-1]
                                break



    for curso in range(len(cursos)):
        for materia in materias[curso]:
            if "Hueco" in materia.nombre  :
                break
            if len(materia.posibleProfesores) == 1:
                materiasProfesores[materia.nombre] = materia.posibleProfesores[0]
            # else:
            #     print(materia.nombre)

    for curso in range(len(cursos)):
        for materia in materias[curso]:
            if "Hueco" in materia.nombre:
                break
            if materiasProfesores[materia.nombre] == None:
                cuentaMinProfesor = None
                for profesoresI in materia.posibleProfesores:
                    cuentaProfesor = 0
                    for profesor in profesoresI.split(";"):
                        for cursoAux in range(len(cursos)):
                            for materiaAux in materias[cursoAux]:
                                if  materiasProfesores[materiaAux.nombre] != None and profesor in materiasProfesores[materiaAux.nombre].split(";"):
                                    cuentaProfesor += materiaAux.cantModulos
                    if cuentaMinProfesor == None or cuentaProfesor < cuentaMinProfesor:
                        cuentaMaxProfesor = cuentaProfesor
                        materiasProfesores[materia.nombre] = profesor

    iteraciones = 0
    while not todosPuestos(horarios) and iteraciones < 5:
        iteraciones += 1
        for curso in range(len(cursos)):
            for dia in range(len(dias)):
                for turno in range(len(turnos)):
                    for combinacionAux in combinacionesTurnos[turno]:
                        combinacion = copy.copy(combinacionAux)
                        # contar modulos en turnos
                        for materia in materias[curso]:
                            # remueve los modulos ya puestos de las combinaciones
                            if "Hueco" in materia.nombre:
                                continue

                            cuentaModulosMateria = 0

                            for modulo in range(turnos[turno].cantModulos):
                                if materia.nombre == horarios[curso][dia][turno][modulo].nombre:
                                    cuentaModulosMateria += 1

                            if cuentaModulosMateria == 0:
                                continue

                            if cuentaModulosMateria in combinacion:
                                combinacion.remove(cuentaModulosMateria)
                            else:
                                continue
                        if len(combinacion) == 0:
                            break

                        for materiaAPoner in materias[curso]:
                            
                            if "Hueco" in materiaAPoner.nombre or not validarModulosTurno(horarios, dia, materiaAPoner):
                                continue

                            modulosRestantes = materiaAPoner.cantModulos - contarModulosTotal(horarios, materiaAPoner)
                            cantHuecos = 0
                            for modulo in range(turnos[turno].cantModulos):
                                if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
                                    cantHuecos += 1

                            if modulosRestantes == 0 or cantHuecos == 0:
                                continue
                            
                            if modulosRestantes < materiaAPoner.modulosContinuos:
                                modulosAPoner = modulosRestantes   
                            else: 
                                modulosAPoner = materiaAPoner.modulosContinuos

                            if modulosAPoner not in combinacion:

                                continue
                                
                            if cantHuecos < modulosAPoner:
                                continue

                            combinacion.remove(modulosAPoner)
                            
                            for _ in range(modulosAPoner):
                                for modulo in range(turnos[turno].cantModulos):
                                    # Porque uso moduloi? Para que el primer turno siempre empiece desde el medio dia asi el segundo turno es utilizable por el swap
                                    # Seria mas facil usar un range()? QuiS4S
                                    if turno == 0:
                                        modulo = turnos[turno].cantModulos-modulo-1

                                    if "Hueco" in horarios[curso][dia][turno][modulo].nombre: 
                                        for profesor in materiasProfesores[materiaAPoner.nombre].split(";"):
                                            if profesor not in disponibilidadProfesores[dia][turno][modulo]:
                                                break
                                        else:
                                            horarios[curso][dia][turno][modulo] = materiaAPoner
                                            break    
                                            
    if not todosPuestos(horarios):
        for curso in range(len(cursos)):
            for materia in materias[curso]:
                if "Hueco" in materia.nombre:
                    break
                if materiasProfesores[materia.nombre] is None:
                    materiasProfesores[materia.nombre] = materia.posibleProfesores[0]
                if "Hueco" in materia.nombre:
                    continue
                if contarModulosTotal(horarios, materia) < materia.cantModulos:
                    curso = cursos.index(materia.curso)
                    dia = encontrarTurnoConMasEspacios(horarios, curso)[0]
                    turno = encontrarTurnoConMasEspacios(horarios, curso)[1]

                    modulosRestantes = materia.cantModulos - contarModulosTotal(horarios, materia)
                    cantHuecos = 0
                    for modulo in range(turnos[turno].cantModulos):
                        if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
                            cantHuecos += 1

                    for _ in range(cantHuecos):
                        if modulosRestantes <= 0:
                            break

                        for modulo in range(turnos[turno].cantModulos):
                            # Porque uso moduloi? Para que el primer turno siempre empiece desde el medio dia asi el segundo turno es utilizable por el swap
                            # Seria mas facil usar un range()? QuiS4S
                            if turno == 0:
                                moduloi = turnos[turno].cantModulos - 1 - modulo
                            else:
                                moduloi = modulo

                            if "Hueco" in horarios[curso][dia][turno][moduloi].nombre:
                                horarios[curso][dia][turno][moduloi] = materia
                                modulosRestantes -= 1
                                break

    for curso in range(len(cursos)):
        for dia in range(len(dias)):
            for turno in range(len(turnos)):
                for modulo in range(turnos[turno].cantModulos):
                    if "Hueco" not in horarios[curso][dia][turno][modulo].nombre:
                        puesto = False
                        for aula in horarios[curso][dia][turno][modulo].posiblesAulas:
                            if aulaDisponible(aula, horarios, dia, turno, modulo, cursos[curso]):
                                puesto = True
                                horariosAulas[curso][dia][turno][modulo] = aula
                                break
                        if not puesto:
                            horariosAulas[curso][dia][turno][modulo] = horarios[curso][dia][turno][modulo].posiblesAulas[0]


    #-----------------------------------------------------------^Swap^------------------------------------------------------------
    checkeo(False, False, True)

    return horarios, materiasProfesores, horariosAulas
