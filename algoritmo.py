import copy
import app
class Materia():
	def __init__(self, nombre, curso, posibleProfesores, posiblesAulas, cantModulos, modulosContinuos):
		self.nombre = nombre + "-" + curso
		self.curso = curso
		self.posibleProfesores = posibleProfesores
		self.posiblesAulas = posiblesAulas
		self.cantModulos = cantModulos
		self.modulosContinuos = modulosContinuos
		self.modulosMinimos = 1


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


def algoritmo(aulas, profesores, dias, cursos, turnos, materias, disponibilidadProfesores, hora, nombreColegio):
	app.decirA()
	cargaAlgoritmo = []
	# ordenar materias por modulosContinuos
	for curso in range(len(cursos)):
		materias[curso] = sorted(
			materias[curso], key=lambda materia: materia.modulosContinuos)


	cargaAlgoritmo.append(0) #5

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
				if profesor:
					for profe in profesor.split(";"):
						if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and "Hueco" not in horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre and profe in materiasProfesores[horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre].split(";"):
							return False
		if profesor:
			for profe in profesor.split(";"):
				if not profe in disponibilidadProfesores[dia][turno][modulo]:
					return False
		return True

	def buscarEspaciosVacios(horarios, curso):
		posiblesPosiciones = []

		for dia in range(len(dias)):
			for turno in range(len(turnos)):
				for modulo in range(turnos[turno].cantModulos):
					if horarios[curso][dia][turno][modulo].nombre.split('-')[0] == "Hueco":
						posiblesPosiciones.append([curso, dia, turno, modulo])

		return posiblesPosiciones

	# Busca donde se puede poner un aula para que este adayacente a otras
	def checkearPosicionValidaMinimosAulas(horarios, aula):
		posiblesPosiciones = []
		for curso in range(len(cursos)):
			for dia in range(len(dias)):
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
							# Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
							cantidadModulos = cantidadModulos - 1
							if modulo == 0:
								if (horariosAulas[curso][dia][turno][modulo + 1] != aula):
									posiblesPosiciones.append(
										[curso, dia, turno, modulo + 1])
							elif modulo + 1 == turnos[turno].cantModulos:
								if (horariosAulas[curso][dia][turno][modulo - 1] != aula):
									posiblesPosiciones.append(
										[curso, dia, turno, modulo - 1])
							elif (horariosAulas[curso][dia][turno][modulo + 1] != aula or horariosAulas[curso][dia][turno][modulo - 1] != aula):
								if horariosAulas[curso][dia][turno][modulo + 1] != aula:
									posiblesPosiciones.append(
										[curso, dia, turno, modulo + 1])
								if horariosAulas[curso][dia][turno][modulo - 1] != aula:
									posiblesPosiciones.append(
										[curso, dia, turno, modulo - 1])
		return posiblesPosiciones

	# devuelve las posibles posiciones donde se puede poner una materia para que este cerca de otra
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
							# Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
							cantidadModulos = cantidadModulos - 1
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

	def buscarTurnosVacios(horarios, curso):
		posiblesPosiciones = []
		noVacio = True
		for dia in range(len(dias)):
			for turno in range(len(turnos)):
				noVacio = True
				for modulo in range(turnos[turno].cantModulos):
					if horarios[curso][dia][turno][modulo].nombre.split('-')[0] != "Hueco":
						noVacio = False
						break
				if noVacio:
					posiblesPosiciones.append([curso, dia, turno])

		return posiblesPosiciones

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
							# Pasa que siempre me sobra 1 y no tenia ganas de reestructurar la logica
							cantidadModulos = cantidadModulos - 1
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

	def conjuntoDeBloques(bloques, bloqueInicial, tamanoRequerido, curso):
		posicionEnBloques = bloques[curso].index(bloqueInicial)
		tamanoActual = len(bloqueInicial)
		conjuntoBloques = [bloqueInicial]
		for posBloque in range(posicionEnBloques+1, len(bloques[curso])):
			if bloques[curso][posBloque][0][1] != bloqueInicial[0][1] or bloques[curso][posBloque][0][0] != bloqueInicial[0][0]:
				return False, []
			conjuntoBloques.append(bloques[curso][posBloque])
			tamanoActual += len(bloques[curso][posBloque])
			if tamanoActual == tamanoRequerido:
				return True, conjuntoBloques
			elif tamanoActual > tamanoRequerido:
				return False, []

		return False, []

	def bloqueValido(horarios, bloque, curso, horariosAulas):
		for posicion in bloque:
			if not profesorDisponible(materiasProfesores[horarios[curso][posicion[0]][posicion[1]][posicion[2]].nombre], horarios, posicion[0], posicion[1], posicion[2], cursos[curso]):
				return False, "profesor"
			if not aulaDisponible(horariosAulas[curso][posicion[0]][posicion[1]][posicion[2]], horarios, posicion[0], posicion[1], posicion[2], cursos[curso]):
				return False, "aula"
			if not validarModulosContinuos(horarios, curso, posicion[0], posicion[1], posicion[2]):
				return False, "Modulos Continuos"
		return True, None

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
			posiblesPosiciones.append([])
			for dia in range(len(dias)):
				for turno in range(len(turnos)):
					for modulo in range(turnos[turno].cantModulos):
						if modulo != 0 and horarios[curso][dia][turno][modulo].nombre == horarios[curso][dia][turno][modulo - 1].nombre and "Hueco" not in horarios[curso][dia][turno][modulo].nombre:
							posiblesPosiciones[-1][-1].append(
								[dia, turno, modulo])
						else:
							posiblesPosiciones[-1].append([[dia, turno, modulo]])

		return posiblesPosiciones

	# Encuentra, dentro de un curso, el turno con mas huecos
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
					mayor = cuentaHuecos

		return turnoDefinitivo

	def swapValido(horariosAValidar, posMateria1, posMateria2, posibleProfesor, aula):

		materia1 = horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
		materia2 = horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo]

		materia2Valida = False

		if posMateria1 != posMateria2:
			materia2Valida = swapValido(horariosAValidar, posMateria2, posMateria2,
										materiasProfesores[materia2.nombre], horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo])

		# disponibilidad profesores
		if materia2Valida and not profesorDisponible(materiasProfesores[materia2.nombre], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
			return False

		if not profesorDisponible(posibleProfesor, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
			return False

		# disponibilidad aulas
		if materia2Valida and not aulaDisponible(horariosAulas[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar, posMateria1.dia, posMateria1.turno, posMateria1.modulo, cursos[posMateria1.curso]):
			return False

		if not aulaDisponible(aula, horariosAValidar, posMateria2.dia, posMateria2.turno, posMateria2.modulo, cursos[posMateria2.curso]):
			return False

		# continiudad modulos
			# swap temporal para probar si qda bien
		horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[
			posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]

		if materia2Valida and not validarModulosContinuos(horariosAValidar, posMateria1.curso, posMateria1.dia, posMateria1.turno, posMateria1.modulo):
			# saco el swap temporal
			horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[
				posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
			return False

		if not validarModulosContinuos(horariosAValidar, posMateria2.curso, posMateria2.dia, posMateria2.turno, posMateria2.modulo):
			# saco el swap temporal
			horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[
				posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]
			return False

			# saco el swap temporal
		horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo], horariosAValidar[posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo] = horariosAValidar[
			posMateria2.curso][posMateria2.dia][posMateria2.turno][posMateria2.modulo], horariosAValidar[posMateria1.curso][posMateria1.dia][posMateria1.turno][posMateria1.modulo]

		# Resticciones extras ACA
		return True

	def inconsistenciasHuecos(horarios, curso, dia, turno):
		inconsistenciasEncontradas = []
		for modulo in len(turnos[turno].cantModulos):
			if (modulo != 0 and modulo != turnos[turno].cantModulos - 1) and "Hueco" in horarios[curso][dia][turno][modulo].nombre and "Hueco" not in horarios[curso][dia][turno][modulo - 1].nombre and "Hueco" not in horarios[curso][dia][turno][modulo + 1].nombre:
				inconsistenciasEncontradas.append(
					[curso, dia, turno, modulo, "Hueco Inconsistente"])
			if (modulo == 0 and turno != 0) and "Hueco" not in horarios[curso][dia][turno][modulo].nombre:
				for modulo2 in len(turnos[turno - 1].cantModulos):
					if "Hueco" not in horarios[curso][dia][turno - 1][modulo2].nombre:
						inconsistenciasEncontradas.append(
							[curso, dia, turno, modulo, "Turno Anterior Inconsistente"])
			if (modulo == turnos[turno].cantModulos - 1 and turno != len(turnos) - 1) and "Hueco" not in horarios[curso][dia][turno][modulo].nombre:
				for modulo2 in len(turnos[turno - 1].cantModulos):
					if "Hueco" not in horarios[curso][dia][turno + 1][modulo2].nombre:
						inconsistenciasEncontradas.append(
							[curso, dia, turno, modulo, "Turno Siguiente Inconsistente"])

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
					bloquesASumar.append(bloque)
				for i in posiblesSwapsRecursivo(horarios, bloque, cantidadARellenar - largoPosible):
					if i not in bloquesASumar:
						bloquesASumar.append(i)
			elif cantidadARellenar == largoPosible:
				bloquesASumar.append(bloque)
				return bloquesASumar
		suma = 0
		for i in bloquesASumar:
			suma += len(i)
		if suma == cantidadARellenar:
			return bloquesASumar
		else:
			return []

	# Chekea que todo este bien, que el horario actual sea valido segun todos los parametros establecidos, se puede enviar un bool para ignorar ciertos parametros

	def checkeo(boolAulas=True, boolProfesores=True, boolModulosContinuos=True):
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
						if not aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo, cursos[curso]) and boolAulas:
							print("Aula no disponible: " + materia.nombre,
								  horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
							return False
						if not profesorDisponible(materiasProfesores[horarios[curso][dia][turno][modulo].nombre], horarios, dia, turno, modulo, cursos[curso]) and boolProfesores:
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

	def checkeoSinReturn(boolAulas=True, boolProfesores=True, boolModulosContinuos=True):
		problemas = 0
		for curso in range(len(cursos)):
			for dia in range(len(dias)):
				for turno in range(len(turnos)):
					for modulo in range(turnos[turno].cantModulos):
						materia = horarios[curso][dia][turno][modulo]
						if "Hueco" in materia.nombre:
							break
						if horariosAulas[curso][dia][turno][modulo] not in materia.posiblesAulas and boolAulas:
							problemas += 1
							print("Aula no disponible: " + materia.nombre,
								horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
						if not aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, dia, turno, modulo, cursos[curso]) and boolAulas:
							problemas += 1
							print("Aula no disponible: " + materia.nombre,
								horariosAulas[curso][dia][turno][modulo], curso, dia, turno, modulo)
						if not profesorDisponible(materiasProfesores[horarios[curso][dia][turno][modulo].nombre], horarios, dia, turno, modulo, cursos[curso]) and boolProfesores:
							problemas += 1
							print("Profesor no disponible: " + materia.nombre,
								materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
						if not validarModulosContinuos(horarios, curso, dia, turno, modulo) and boolModulosContinuos:
							problemas += 1
							print("Modulos continuos: " + materia.nombre,
								materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
						if contarModulosTotal(horarios, materia) != materia.cantModulos and boolModulosContinuos:
							problemas += 1
							print("Modulos continuos: " + materia.nombre,
								materiasProfesores[horarios[curso][dia][turno][modulo].nombre], curso, dia, turno, modulo)
		print(problemas)

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
		if "Hueco" not in materiaChequear.nombre:
			if turnoChequear == 0 and moduloChequear == 0 and "Hueco" in horariosChequear[cursoChequear][diaChequear][turnoChequear][moduloChequear + 1].nombre:
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
						if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre:
							break

					else:
						continue
					break

				else:
					for modulo in range(turnos[turnoChequear].cantModulos):
						if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre:
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
						if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre:
							break

					else:
						continue
					break

				else:
					for modulo in range(turnos[turnoChequear].cantModulos):
						if "Hueco" not in horariosChequear[cursoChequear][diaChequear][turno][modulo].nombre:
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
				if horarioVerificar[cursos.index(curso)][dia][turno][modulo] is not None and "Hueco" not in horarioVerificar[cursos.index(curso)][dia][turno][modulo].nombre and horariosAulas[cursos.index(curso)][dia][turno][modulo] == aula:
					return False
		return True

	# Posibles combinaciones de modulos de c/materia p/cada turno
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

	cargaAlgoritmo[-1] = 5
	print("Aca llamo a progreso")
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	print("aca ya llame a progreso")

	# -------------------------------------------------------^Funciones^---------------------------------------------------------------------
	# Incializaciones


	cargaAlgoritmo.append(0) #5

	cargaAulas = {}
	for aula in aulas:
		cuentaAula = 0
		for curso in range(len(cursos)):
			for materia in materias[curso]:
				if aula in materia.posiblesAulas:
					cuentaAula += materia.cantModulos
		cargaAulas[aula] = cuentaAula

	def myFunc(aulaA):
		return cargaAulas[aulaA]

	cargaAlgoritmo[-1] = 1
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	for curso in range(len(cursos)):
		for materia in materias[curso]:
			materia.posiblesAulas.sort(key=myFunc)

	cargaAlgoritmo[-1] = 2
	app.progreso(hora, nombreColegio, cargaAlgoritmo)

	combinacionesTurnos = []
	for turno in turnos:
		combinacionesTurnos.append([])
		combinaciones(turno, [])

	cargaAlgoritmo[-1] = 3
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
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

	cargaAlgoritmo[-1] = 4
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	# Inicializo las posciciones de las materias
	materiasProfesores = {}
	for curso in range(len(cursos)):
			for materia in materias[curso]:
				materiasProfesores[materia.nombre] = None

	cargaAlgoritmo[-1] = 5
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
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

	cargaAlgoritmo[-1] = 6
	app.progreso(hora, nombreColegio, cargaAlgoritmo)

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

	cargaAlgoritmo[-1] = 7
	app.progreso(hora, nombreColegio, cargaAlgoritmo)

	for curso in range(len(cursos)):
		for materia in materias[curso]:
			if "Hueco" in materia.nombre:
				break
			if len(materia.posibleProfesores) == 1:
				materiasProfesores[materia.nombre] = materia.posibleProfesores[0]
	cargaAlgoritmo[-1] = 8
	app.progreso(hora, nombreColegio, cargaAlgoritmo)

	# Asigandor profesores
	for curso in range(len(cursos)):
		for materia in materias[curso]:
			if "Hueco" in materia.nombre:
				break
			if materiasProfesores[materia.nombre] == None:
				cargaProfesorPrincipal = 0
				profesorPrincipal = None
				for profesorPosible in materia.posibleProfesores:
					cargaProfesorPosible = 0
					for curso2 in range(len(cursos)):
						for materia2 in materias[curso2]:
							if materiasProfesores[materia2.nombre] != None and profesorPrincipal != None and profesorPrincipal in materiasProfesores[materia2.nombre]:
								cargaProfesorPrincipal += materia.cantModulos
							if materiasProfesores[materia2.nombre] != None and profesorPosible in materiasProfesores[materia2.nombre]:
								cargaProfesorPosible += materia.cantModulos
					if cargaProfesorPosible < cargaProfesorPrincipal or profesorPrincipal == None:
						profesorPrincipal = profesorPosible
						materiasProfesores[materia.nombre] = profesorPosible
					else:
						materiasProfesores[materia.nombre] = profesorPrincipal

	cargaAlgoritmo[-1] = 9
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	cargaAlgoritmo[-1] = 10
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	# ^^Inicializciones^^

	# for curso in range(len(cursos)):
	#	for materia in materias[curso]:
	#		if "Hueco" in materia.nombre:
	#			break
	#		if materiasProfesores[materia.nombre] == None:
	#			cuentaMinProfesor = None
	#			for profesoresI in materia.posibleProfesores:
	#				cuentaProfesor = 0
	#				for profesor in profesoresI.split(";"):
	#					for cursoAux in range(len(cursos)):
	#						for materiaAux in materias[cursoAux]:
	#							if  materiasProfesores[materiaAux.nombre] != None and profesor in materiasProfesores[materiaAux.nombre].split(";"):
	#								cuentaProfesor += materiaAux.cantModulos
	#				if cuentaMinProfesor == None or cuentaProfesor < cuentaMinProfesor:
	#					cuentaMaxProfesor = cuentaProfesor
	#					materiasProfesores[materia.nombre] = profesor


	cargaAlgoritmo.append(0) #25

	# Greedy principal
	iteraciones = 0
	while not todosPuestos(horarios) and iteraciones < 10:
		cargaAlgoritmo[-1] = iteraciones * 2
		app.progreso(hora, nombreColegio, cargaAlgoritmo)
		iteraciones += 1
		for curso in range(len(cursos)):
			for dia in range(len(dias)):
				for turno in range(len(turnos)):
					for combinacionAux in combinacionesTurnos[turno]:
						for cursoHueco in range(len(cursos)):
							for diaHueco in range(len(dias)):
								for turnoHueco in range(len(turnos)):
									for moduloHueco in range(turnos[turno].cantModulos):
										if "Hueco" in horarios[cursoHueco][diaHueco][turnoHueco][moduloHueco].nombre:
											horariosAulas[cursoHueco][diaHueco][turnoHueco][moduloHueco] = "Hueco"
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
							# if materiaAPoner.nombre == "Programacion - 6C":
							#	 print("a")

							if materiaAPoner.modulosMinimos <= 1 and iteraciones < 2:
								continue
							if "Hueco" in materiaAPoner.nombre or not validarModulosTurno(horarios, dia, materiaAPoner):
								continue

							modulosRestantes = materiaAPoner.cantModulos - contarModulosTotal(horarios, materiaAPoner)
							cantHuecos = 0
							for modulo in range(turnos[turno].cantModulos):
								if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
									cantHuecos += 1

							if modulosRestantes == 0 or cantHuecos == 0 or (materiaAPoner.modulosMinimos > cantHuecos):
								continue

							if modulosRestantes < materiaAPoner.modulosContinuos:
								modulosAPoner = modulosRestantes
							else:
								modulosAPoner = materiaAPoner.modulosContinuos

							if modulosAPoner not in combinacion:
								continue

							if cantHuecos < modulosAPoner:
								continue


							huecosUsables = 0
							for modulo in range(turnos[turno].cantModulos):
								if turno == 0:
									a = modulo
									modulo = turnos[turno].cantModulos-modulo-1
								if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
									if not profesorDisponible(materiasProfesores[materiaAPoner.nombre], horarios, dia, turno, modulo, curso):
										huecosUsables = 0
										break
									for aulaPosible in materiaAPoner.posiblesAulas:
										if aulaDisponible(aulaPosible, horarios, dia, turno, modulo, cursos[curso]):
											break
									else:
										huecosUsables = 0
										break
									for profesor in materiasProfesores[materiaAPoner.nombre].split(";"):
										if profesor not in disponibilidadProfesores[dia][turno][modulo]:
											huecosUsables = 0
											break
									else:
										huecosUsables += 1
							if huecosUsables < modulosAPoner:
								continue

							combinacion.remove(modulosAPoner) #
							for _ in range(modulosAPoner):
								for modulo in range(turnos[turno].cantModulos):


									if turno == 0:
										a = modulo
										modulo = turnos[turno].cantModulos-modulo-1

									if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
										if not profesorDisponible(materiasProfesores[materiaAPoner.nombre], horarios, dia, turno, modulo, curso):
											break
										for aulaPosible in materiaAPoner.posiblesAulas:
											if aulaDisponible(aulaPosible, horarios, dia, turno, modulo, cursos[curso]):
												break
										else:
											break
										for profesor in materiasProfesores[materiaAPoner.nombre].split(";"):
											if profesor not in disponibilidadProfesores[dia][turno][modulo]:
												break
										else:
											horarios[curso][dia][turno][modulo] = materiaAPoner
											# if materiaAPoner.nombre == "Programacion - 6C":
											#	 print(modulo)
											#	 print(modulosAPoner)
											#	 print(horarios[curso][dia][turno][modulo - 1].nombre)
											#	 print(horarios[curso][dia][turno][modulo - 2].nombre)
											#	 print(horarios[curso][dia][turno][modulo - 3].nombre)
											#	 print(horarios[curso][dia][turno][modulo - 4].nombre)
											#	 print(horarios[curso][dia][turno][modulo - 5].nombre)
											#	 input()
											pusido = False
											if _ == modulosAPoner - 1:
												for aulaPosible in horarios[curso][dia][turno][modulo].posiblesAulas:
													for moduloParaAula in range(turnos[turno].cantModulos):
														if aulaDisponible(aulaPosible, horarios, dia, turno, moduloParaAula, cursos[curso]) and horarios[curso][dia][turno][moduloParaAula].nombre == materiaAPoner.nombre:
															horariosAulas[curso][dia][turno][moduloParaAula] = aulaPosible
															if moduloParaAula == modulo:
																pusido = True
														elif horarios[curso][dia][turno][moduloParaAula].nombre == materiaAPoner.nombre:
															break
													else:
														break
											if not pusido:
												for aulaPosible in horarios[curso][dia][turno][modulo].posiblesAulas:
													if aulaDisponible(aulaPosible, horarios, dia, turno, modulo, cursos[curso]):
														horariosAulas[curso][dia][turno][modulo] = aulaPosible
														break
											break

	
	cargaAlgoritmo[-1] = 25
	
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	# Greedy secundario (No mas de 10 iteraciones usualmente)
	cargaAlgoritmo.append(0) #10
	while not todosPuestos(horarios):
		cargaAlgoritmo[-1] += 1
		app.progreso(hora, nombreColegio, cargaAlgoritmo)
		for curso in range(len(cursos)):
			for materia in materias[curso]:
				if "Hueco" in materia.nombre:
					continue
				if contarModulosTotal(horarios, materia) < materia.cantModulos:
					curso = cursos.index(materia.curso)
					dia = encontrarTurnoConMasEspacios(horarios, curso)[0]
					turno = encontrarTurnoConMasEspacios(horarios, curso)[1]
					print(curso, dia, turno)
					modulosRestantes = materia.cantModulos - contarModulosTotal(horarios, materia)
					cantHuecos = 0
					for modulo in range(turnos[turno].cantModulos):
						if "Hueco" in horarios[curso][dia][turno][modulo].nombre:
							cantHuecos += 1
					for _ in range(cantHuecos):
						if modulosRestantes == 0:
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
	cargaAlgoritmo[-1] = 10
	app.progreso(hora, nombreColegio, cargaAlgoritmo)


	cargaAlgoritmo.append(0) # 5
	# Poner Aulas faltantes
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
	cargaAlgoritmo[-1] = 5
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	# ---------------------------------------------^Greedy^--------------------------------------------------------------------



	def swap2(horarios, horariosAulas):
		# La idea seria swappear por turnos, si no va ir probando con cada vez menos bloques hasta quedar solo con el problematico
		bloques = encontrarBloquesMaterias(horarios)
		for curso in range(len(cursos)):
			for iBloque in range(len(bloques[curso])):
				bloqueA = bloques[curso][iBloque]
				dia = bloqueA[0][0]
				turno = bloqueA[0][1]

				materia = horarios[curso][dia][turno][bloqueA[0][2]]

				if "Hueco" in materia.nombre:
					continue
				a, b = bloqueValido(horarios, bloqueA, curso, horariosAulas)
				if a:
					continue
				bloqueTurno = []
				for bloqueParaTurno in bloques[curso]:
					if bloqueParaTurno[0][0] == dia and bloqueParaTurno[0][1] == turno:
						bloqueTurno.append(bloqueParaTurno)
				for repeticion in range(len(bloqueTurno)):

					if bloqueA not in bloqueTurno:
						break
					bloque = []
					for bloqueAUnir in bloqueTurno:
						bloque += bloqueAUnir
					for bloque2 in bloques[curso]:

						if bloque2 == bloque:
							continue
						bloquesAux = [bloque2]

						if len(bloque) < len(bloque2):
							continue

						elif len(bloque) > len(bloque2):
							posibleConjunto, bloquesAux = conjuntoDeBloques(bloques, bloque2, len(bloque), curso)

							if not posibleConjunto:
								continue

						horariosAux = copy.deepcopy(horarios)
						horariosAulasAux = copy.deepcopy(horariosAulas)

						bloqueSwappeado = []
						for bloqueAux in bloquesAux:
							bloqueSwappeado += bloqueAux

						for moduloBloque in bloque:
							for bloqueAux in bloquesAux:
								for moduloBloqueAux in bloqueAux:
									if bloque.index(moduloBloque) != bloqueSwappeado.index(moduloBloqueAux):
										continue
									horariosAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]],horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]], horariosAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]]
									horariosAulasAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]],horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]], horariosAulasAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]]

						# if turno = 0
						# if turno2 = 0
						# if turno = len(turnos) - 1
						# if turno2 = len(turnos) - 1


						a, b = bloqueValido(horariosAux, bloqueSwappeado, curso, horariosAulasAux)
						if not a:

							if b == "aula":
								for moduloBloqueAux in bloqueSwappeado:
									for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
										if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
											horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
											break
								a, b = bloqueValido(horariosAux, bloqueSwappeado, curso, horariosAulasAux)

							# print(horarios[curso][bloque[0][0]][bloque[0][1]][bloque[0][2]].nombre)
							# print(horarios[curso][bloque2[0][0]][bloque2[0][1]][bloque2[0][2]].nombre)
							# for curso in range(len(cursos)):
							#	 imprimir(curso)
							# input()
							if not a:
								continue

						swapInvalido = False

						for bloqueAux in bloquesAux:
							# if "Hueco" in horariosAux[curso][bloqueAux[0][0]][bloqueAux[0][1]][bloqueAux[0][2]].nombre:
							#	 continue

							a, b = bloqueValido(horarios, bloqueAux, curso, horariosAulas)
							if a:

								valido, errorSwap = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
								if not valido:
									if errorSwap == "aula":
										for moduloBloqueAux in bloqueAux:
											for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
												if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
													horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
													break
										valido, b = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
									if not valido:
										swapInvalido = True
							if not a:
								valido, errorSwap = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
								if not valido:
									if errorSwap == "aula":
										for moduloBloqueAux in bloqueAux:
											for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
												if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
													horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
													break
						if swapInvalido:
							continue

						horarios = horariosAux
						horariosAulas = horariosAulasAux




						break
					else:
						bloqueTurno.pop(len(bloqueTurno) - 1)
						continue

					break
		return horarios, horariosAulas



	def swap(horarios, horariosAulas):
		bloques = encontrarBloquesMaterias(horarios)
		for curso in range(len(cursos)):
			for iBloque in range(len(bloques[curso])):
				bloque = bloques[curso][iBloque]
				dia = bloque[0][0]
				turno = bloque[0][1]

				materia = horarios[curso][dia][turno][bloque[0][2]]

				if "Hueco" in materia.nombre:
					continue
				a, b = bloqueValido(horarios, bloque, curso, horariosAulas)
				if a:
					continue

				for bloque2 in bloques[curso]:

					if bloque2 == bloque:
						continue
					bloquesAux = [bloque2]

					if len(bloque) < len(bloque2):
						continue

					elif len(bloque) > len(bloque2):
						posibleConjunto, bloquesAux = conjuntoDeBloques(bloques, bloque2, len(bloque), curso)

						if not posibleConjunto:
							continue

					horariosAux = copy.deepcopy(horarios)
					horariosAulasAux = copy.deepcopy(horariosAulas)

					bloqueSwappeado = []
					for bloqueAux in bloquesAux:
						bloqueSwappeado += bloqueAux

					for moduloBloque in bloque:
						for bloqueAux in bloquesAux:
							for moduloBloqueAux in bloqueAux:
								if bloque.index(moduloBloque) != bloqueSwappeado.index(moduloBloqueAux):
									continue
								horariosAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]],horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]], horariosAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]]
								horariosAulasAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]],horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]], horariosAulasAux[curso][moduloBloque[0]][moduloBloque[1]][moduloBloque[2]]

					# if turno = 0
					# if turno2 = 0
					# if turno = len(turnos) - 1
					# if turno2 = len(turnos) - 1


					a, b = bloqueValido(horariosAux, bloqueSwappeado, curso, horariosAulasAux)
					if not a:

						if b == "aula":
							for moduloBloqueAux in bloqueSwappeado:
								for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
									if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
										horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
										break
							a, b = bloqueValido(horariosAux, bloqueSwappeado, curso, horariosAulasAux)

						# print(horarios[curso][bloque[0][0]][bloque[0][1]][bloque[0][2]].nombre)
						# print(horarios[curso][bloque2[0][0]][bloque2[0][1]][bloque2[0][2]].nombre)
						# for curso in range(len(cursos)):
						#	 imprimir(curso)
						# input()
						if not a:
							continue

					swapInvalido = False

					for bloqueAux in bloquesAux:
						# if "Hueco" in horariosAux[curso][bloqueAux[0][0]][bloqueAux[0][1]][bloqueAux[0][2]].nombre:
						#	 continue

						a, b = bloqueValido(horarios, bloqueAux, curso, horariosAulas)
						if a:

							valido, errorSwap = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
							if not valido:
								if errorSwap == "aula":
									for moduloBloqueAux in bloqueAux:
										for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
											if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
												horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
												break
									valido, b = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
								if not valido:
									swapInvalido = True
						if not a:
							valido, errorSwap = bloqueValido(horariosAux, bloque[bloqueSwappeado.index(bloqueAux[0]) : bloqueSwappeado.index(bloqueAux[-1]) + 1], curso, horariosAulasAux)
							if not valido:
								if errorSwap == "aula":
									for moduloBloqueAux in bloqueAux:
										for aula in horariosAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]].posiblesAulas:
											if aulaDisponible(aula, horarios, moduloBloqueAux[0], moduloBloqueAux[1], moduloBloqueAux[2], cursos[curso]):
												horariosAulasAux[curso][moduloBloqueAux[0]][moduloBloqueAux[1]][moduloBloqueAux[2]] = aula
												break
					if swapInvalido:
						continue

					horarios = horariosAux
					horariosAulas = horariosAulasAux




					break
				else:
					continue
				break
			else:
				continue
			break

		return horarios, horariosAulas

	
	cargaAlgoritmo.append(0) #30
	iteracion = 0
	while not checkeo() and iteracion != 30:
		print(iteracion)
		cargaAlgoritmo[-1] = iteracion
		app.progreso(hora, nombreColegio, cargaAlgoritmo)
		horarios, horariosAulas = swap(horarios, horariosAulas)
		horarios, horariosAulas = swap2(horarios, horariosAulas)
		iteracion += 1

	cargaAlgoritmo[-1] = 30
	app.progreso(hora, nombreColegio, cargaAlgoritmo)
	# for materiaAPoner in materias:
	#	 if "Hueco" not in materiaAPoner.nombre:
	#		 cuentaTotal = 0

	#		 for dia in range(len(dias)):
	#			 cuentaDia = 0
	#			 for turno in range(len(turnos)):
	#				 for modulo in range(turnos[turno].cantModulos):

	#					 if cuentaTotal < materiaAPoner.cantModulos and cuentaDia < materiaAPoner.modulosContinuos and "Hueco" in horarios[cursos.index(materiaAPoner.curso)][dia][turno][modulo].nombre:
	#						 horarios[cursos.index(materiaAPoner.curso)][dia][turno][modulo] = materiaAPoner
	#						 cuentaTotal += 1
	#						 cuentaDia += 1


	# ------------------------------------Reagrupador------------------------------------------



	# Agrupador de aulas principal, utiliza el mismo metodo que el agrupador de materias
	def agrupadorPrincipalAulas(horariosAulas, horarios):
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
							for posiblePosicion in posibles:
								if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horarios, dia, turno, modulo, cursos[curso]) and aulaDisponible(horariosAulas[curso][dia][turno][modulo], horarios, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], cursos[posiblePosicion[0]])):
									if horariosAulas[curso][dia][turno][modulo] in horarios[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]].posiblesAulas and horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] in horarios[curso][dia][turno][modulo].posiblesAulas:
										horariosAulas[curso][dia][turno][modulo], horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horariosAulas[curso][dia][turno][modulo]
										break




	# Agrupador secundario de aulas, este intenta poner aulas adyacentes a las que ya hay
	def agrupadorSecundarioAulas(horariosAulas, horarios):
		for aula in aulas:
			posibles = checkearPosicionValidaMinimosAulas(horariosAulas, aula)
			for posiblePosicion in posibles:
				if (aulaDisponible(horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]], horarios, dia, turno, modulo, cursos[curso]) and aulaDisponible(aula, horarios, posiblePosicion[1], posiblePosicion[2], posiblePosicion[3], cursos[posiblePosicion[0]])):
					if aula in horarios[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]].posiblesAulas:
						horariosAulas[posiblePosicion[0]][posiblePosicion[1]][posiblePosicion[2]][posiblePosicion[3]] = aula
						break

	# Tercer agrupador, este intenta hacer que en un bloque tengan todos la misma aula
	def agrupadorTerciarioAulas(horariosAulas, horarios):
		bloquesMaterias = encontrarBloquesMaterias(horarios)
		horariosCopia = copy.deepcopy(horariosAulas)
		for curso in range(len(cursos)):
			for bloque in bloquesMaterias[curso]:
				materia = horarios[  curso  ][  bloque[0][0]  ][  bloque[0][1]  ][  bloque[0][2]  ]
				aulasUsadas = {}
				horarioValido = True
				for modulo in bloque:
					try:
						aulasUsadas[horariosAulas[curso][modulo[0]][modulo[1]][modulo[2]]] = aulasUsadas[horariosAulas[curso][modulo[0]][modulo[1]][modulo[2]]] + 1
					except:
						aulasUsadas[horariosAulas[curso][modulo[0]][modulo[1]][modulo[2]]] = 1
				if not len(aulasUsadas.keys()) == 1:
					for aula in aulasUsadas:
						for modulo in bloque:
							if aulaDisponible(aula, horarios, modulo[0], modulo[1], modulo[2], curso) and aula in horarios[curso][modulo[0]][modulo[1]][modulo[2]].posiblesAulas:
								horariosCopia[curso][modulo[0]][modulo[1]][modulo[2]] = aula
							else:
								horarioValido = False



				if not horarioValido:
					for aula in aulas:
						for modulo in bloque:
							if aulaDisponible(aula, horarios, modulo[0], modulo[1], modulo[2], curso) and aula in horarios[curso][modulo[0]][modulo[1]][modulo[2]].posiblesAulas:
								horariosCopia[curso][modulo[0]][modulo[1]][modulo[2]] = aula
							else:
								horarioValido = False




				if horarioValido:
					horariosAulas = horariosCopia
				else:
					horariosCopia = horariosAulas


	cargaAlgoritmo.append(0) #20

	for i in range(10):
		cargaAlgoritmo[-1] = i * 2
		app.progreso(hora, nombreColegio, cargaAlgoritmo)
		agrupadorPrincipalAulas(horariosAulas, horarios)
		agrupadorSecundarioAulas(horariosAulas, horarios)
		agrupadorTerciarioAulas(horariosAulas, horarios)


	# ------------------------------------^Reagrupador^-----------------------------------------------------

	# -----------------------------------------------------------^Swap^------------------------------------------------------------

	checkeoSinReturn(True, True, True)
	return horarios, materiasProfesores, horariosAulas, cargaAlgoritmo