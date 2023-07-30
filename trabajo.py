import json
import os

usuarios = {
  "profesor": "contraseña_profesor",
  "estudiante": "contraseña_estudiante",
}

try:
  with open("base_de_datos.json", "r") as archivo:
    base_de_datos = json.load(archivo)
except FileNotFoundError:
  base_de_datos = {}


def guardar_base_de_datos():
  with open("base_de_datos.json", "w") as archivo:
    json.dump(base_de_datos, archivo)


print("Bienvenido, inicia sesion si eres estudiante o profesor. \n")


def inicio_sesion():
  intentos_maximos = 3
  intentos = 0
  while intentos < intentos_maximos:

    usuario = input("Escriba su usuario: ")
    contraseña = input("Escriba su contraseña: ")
    if usuarios.get(usuario) == contraseña:
      print("\n-------------------------")
      print("Inicio de sesión exitoso.")
      print("-------------------------")
      return usuario
    else:
      print("\nCredenciales inválidas. Intente nuevamente.\n")
      intentos += 1
  print("\nSe alcanzó el máximo de intentos de inicio de sesión.")
  return None


def mostrar_notas(estudiante):
  if estudiante not in base_de_datos:
    print(
      f"\nEl estudiante '{estudiante}' no se encuentra en la base de datos.")
    return

  materias = base_de_datos[estudiante]["materias"]
  print(f"\nTabla de Notas del estudiante {estudiante}")
  print("--------------------------")
  print("Materia              Nota")
  print("--------------------------")
  for materia, nota in materias.items():
    print(f"{materia:<20} {nota}")


def calcular_promedio(estudiante):
  if estudiante not in base_de_datos:
    print(
      f"\nEl estudiante '{estudiante}' no se encuentra en la base de datos.")
    return

  materias = base_de_datos[estudiante]["materias"]
  total_notas = sum(materias.values())
  promedio = total_notas / len(materias)
  base_de_datos[estudiante]["promedio"] = promedio
  return promedio


def mostrar_promedio(estudiante):
  if estudiante not in base_de_datos:
    print(f"\nEl estudiante {estudiante} no se encuentra en la base de datos.")
    return

  if "promedio" not in base_de_datos[estudiante]:
    promedio = calcular_promedio(estudiante)
  else:
    promedio = base_de_datos[estudiante]["promedio"]
    print("\n-----------------------")
    print(f"Promedio de '{estudiante}': {promedio}")
    print("-----------------------")


def editar_notas(profesor, estudiante, materia, nueva_nota):
  if profesor not in usuarios:
    print("\nAcceso denegado. Solo los profesores pueden editar notas.")
    return

  if estudiante not in base_de_datos:
    print(
      f"\nEl estudiante '{estudiante}' no se encuentra en la base de datos.")
    return

  base_de_datos[estudiante]["materias"][materia] = nueva_nota
  print("\n------------------------------------------------")
  print(f"Nota de '{materia}' para '{estudiante}' modificada a {nueva_nota}.")
  print("------------------------------------------------")


def mostrar_notas_por_materia(materia):
  notas = []
  for estudiante, data in base_de_datos.items():
    if materia in data["materias"]:
      notas.append((estudiante, data["materias"][materia]))

  if not notas:
    print(f"\nNo hay notas para la materia '{materia}'.")
  else:
    print(f"\nNotas para la materia '{materia}':")
    print("\nEstudiante           Nota")
    print("--------------------------")
    for estudiante, nota in notas:
      print(f"{estudiante:<20} {nota}")


def calcular_promedio_global(materia):
  total_notas = 0
  total_estudiantes = 0
  for data in base_de_datos.values():
    if materia in data["materias"]:
      total_notas += data["materias"][materia]
      total_estudiantes += 1
  if total_estudiantes > 0:
    return total_notas / total_estudiantes
  else:
    return None


def mostrar_promedio_global(materia):
  promedio = calcular_promedio_global(materia)
  if promedio is not None:
    print("\n-------------------------------------------")
    print(f"Promedio global de '{materia}': {promedio}")
    print("-------------------------------------------")
  else:
    print(f"\nNo hay notas para la materia '{materia}'.")


def guardar_estudiante_nuevo(profesor):
  if profesor not in usuarios:
    print("\nAcceso denegado. Solo los profesores pueden guardar estudiantes.")
    return

  nombre_estudiante = input("\nIngrese el nombre del nuevo estudiante: ")
  if nombre_estudiante in base_de_datos:
    print(
      f"\nEl estudiante '{nombre_estudiante}' ya existe en la base de datos.")
    return

  base_de_datos[nombre_estudiante] = {"materias": {}}
  print(f"\nDatos del estudiante '{nombre_estudiante}' agregados.")

  materias = [
    "ciencias",
    "tecnologia",
    "medio ambiente",
    "artes",
    "matematicas",
    "fisica",
    "quimica",
    "lengua",
    "historia",
  ]

  for materia in materias:
    while True:
      try:
        nota = float(input(f"\nIngrese la nota para la materia '{materia}': "))
        base_de_datos[nombre_estudiante]["materias"][materia] = nota
        break
      except ValueError:
        print("\nValor inválido. La nota debe ser un número.")

  print(
    "\n--------------------------------------------------------------------")
  print(
    f"Las calificaciones del estudiante '{nombre_estudiante}' se han puesto correctamente."
  )
  print("--------------------------------------------------------------------")


def main():
  usuario = inicio_sesion()
  if usuario is None:
    return

  bienvenida_profesor = False
  bienvenida_estudiante = False

  # Se declaran diferentes entradas en caso de que sea "estudiante" o "profesor"
  while True:
    if usuario == "profesor" and not bienvenida_profesor:
      print("\nBienvenido, profesor.\n")
      bienvenida_profesor = True
    elif usuario == "estudiante" and not bienvenida_estudiante:
      print("\nBienvenido, estudiante.\n")
      bienvenida_estudiante = True

    if usuario == "profesor":
      print("\n¿Qué desea hacer?\n")
      print("1. Guardar estudiante nuevo y publicar notas")
      print("2. Editar notas de un estudiante")
      print("3. Mostrar notas de todos los estudiantes por materia")
      print("4. Calcular Promedio de notas del estudiante")
      print("5. Calcular Promedio Global de notas de una materia\n")
      opcion = input("Ingrese el número de la opción deseada: ")

      # Cada opcion lleva consigo su funcion pa que esta se ejecute
      if opcion == "1":
        guardar_estudiante_nuevo(usuario)
      elif opcion == "2":
        estudiante = input("\nNombre del estudiante: ")
        materia = input("\nMateria: ")
        nueva_nota = float(input("\nNueva nota: "))
        editar_notas(usuario, estudiante, materia, nueva_nota)
      elif opcion == "3":
        materia = input("\nMateria: ")
        mostrar_notas_por_materia(materia)
      elif opcion == "4":
        estudiante = input("\nIngrese el nombre del estudiante: ")
        mostrar_promedio(estudiante)
      elif opcion == "5":
        materia = input("\nIngrese Materia: ")
        mostrar_promedio_global(materia)
      else:
        print("Opción inválida.")

    elif usuario == "estudiante":
      print("\n¿Qué desea hacer?\n")
      print("1. Mostrar notas")
      print("2. Mostrar promedio\n")
      opcion = input("Ingrese el número de la opción deseada: ")

      if opcion == "1":
        estudiante = input("\nNombre del estudiante: ")
        mostrar_notas(estudiante)
      elif opcion == "2":
        estudiante = input("\nNombre del estudiante: ")
        mostrar_promedio(estudiante)
    else:
      print("\nPerfil no reconocido. Saliendo del programa.")

    guardar_base_de_datos()

    # Opciones de salida, cuando acabe todo el programa
    opcion_salir = input("\n¿Desea salir? (s/n): ").lower()
    if opcion_salir == "s":
      os.system('clear')
      print("Saliendo del programa...")
      break


if __name__ == "__main__":
  main()
