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
                        if modulo != 0 and horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - 1].nombre and "Hueco" not in horariosAulas[curso][dia][turno][modulo]:
                            posiblesPosiciones[len(
                                posiblesPosiciones) - 1].append([curso, dia, turno, modulo])
                        elif "Hueco" not in horariosAulas[curso][dia][turno][modulo] :
                            posiblesPosiciones.append([])
                            posiblesPosiciones[len(
                                posiblesPosiciones) - 1].append([curso, dia, turno, modulo])
        return posiblesPosiciones


    def posiblesSwaps(horarios, bloqueMateria):
        posibilidades = []
        curso = bloqueMateria[0][0]
        dia = bloqueMateria[0][1]
        turno = bloqueMateria[0][2]
        materia = horarios[curso][dia][turno][bloqueMateria[0][3]]
        bloques = encontrarBloquesMaterias(horarios)
        largo = len(bloqueMateria)
        for bloque in bloques:
            largoPosible = len(bloque)
            if largo < largoPosible:
                break
            cursoPosible = bloque[0][0]
            if curso != cursoPosible:
                break
            diaPosible = bloque[0][1]
            turnoPosible = bloque[0][2]
            materiaPosible = horarios[cursoPosible][diaPosible][turnoPosible][bloque[0][3]]
            
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
    def checkeo(boolAulas, boolProfesores, boolModulosContinuos):
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


    #ordenar materias por modulosContinuos
    for curso in range(len(cursos)):
        materias[curso] = sorted(materias[curso], key=lambda materia: materia.modulosContinuos)

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
                                        moduloi = turnos[turno].cantModulos - 1 - modulo
                                    else:
                                        moduloi = modulo

                                    if "Hueco" in horarios[curso][dia][turno][moduloi].nombre:
                                        horarios[curso][dia][turno][moduloi] = materiaAPoner
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
        for materia in materias[curso]:
            if "Hueco" in materia.nombre:
                break
            cuentaProfesores = {}
            minimo = materia.posibleProfesores[0]
            
            for posibleProfesor in materia.posibleProfesores:
                cuentaProfesores[posibleProfesor] = 0

            for curso2 in range(len(cursos)):
                for materia2 in materias[curso2]:
                    if materiasProfesores[materia2.nombre] in cuentaProfesores:
                        cuentaProfesores[materiasProfesores[materia2.nombre]] += 1
            for profesor in cuentaProfesores.keys():
                if cuentaProfesores[profesor] < cuentaProfesores[minimo]:
                    minimo = profesor

            materiasProfesores[materia.nombre] = minimo

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

    #---------------------------------------------^Greedy^--------------------------------------------------------------------

    def swap(horarios):
        for curso in range(len(cursos)):
            for materia in materias[curso]:
                if "Hueco" in materia.nombre:
                    break
                if materiasProfesores[materia.nombre] is None:
                    materiasProfesores[materia.nombre] = materia.posibleProfesores[0]
                if "Hueco" in materia.nombre:
                    break
                bloques = encontrarBloquesMaterias(horarios)
                for posiblePosicion in bloques:
                    curso = posiblePosicion[0][0]
                    dia = posiblePosicion[0][1]
                    turno = posiblePosicion[0][2]
                    cantidadModulos = len(posiblePosicion)

                    
                    if horarios[curso][dia][turno][posiblePosicion[0][3]].nombre != materia.nombre:
                        break
                    for posiblePosicion2 in bloques:
                        cursoSwap = posiblePosicion[0][0]
                        diaSwap = posiblePosicion[0][1]
                        turnoSwap = posiblePosicion[0][2]
                        cantidadModulos2 = len(posiblePosicion2)

                        if cantidadModulos < cantidadModulos2 and curso != cursoSwap:
                            break
                    #elif

    # for materiaAPoner in materias:
    #     if "Hueco" not in materiaAPoner.nombre:
    #         cuentaTotal = 0

    #         for dia in range(len(dias)):
    #             cuentaDia = 0
    #             for turno in range(len(turnos)):
    #                 for modulo in range(turnos[turno].cantModulos):

    #                     if cuentaTotal < materiaAPoner.cantModulos and cuentaDia < materiaAPoner.modulosContinuos and "Hueco" in horarios[cursos.index(materiaAPoner.curso)][dia][turno][modulo].nombre:
    #                         horarios[cursos.index(materiaAPoner.curso)][dia][turno][modulo] = materiaAPoner
    #                         cuentaTotal += 1
    #                         cuentaDia += 1



    #-----------------------------------------------------------^Swap^------------------------------------------------------------
    checkeo(False, False, True)

    return horarios, materiasProfesores, horariosAulas
