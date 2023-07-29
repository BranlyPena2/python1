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