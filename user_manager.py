#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

import json
from pathlib import Path

class UserManager:
    def __init__(self, filepath="usuarios.json"):
        self.filepath = Path(filepath)
        self.usuarios = self.cargar_usuarios()
     # Asegurarse de que 'root' exista
        if "root" not in self.usuarios:
            self.usuarios["root"] = {
                "password": "rootpass",
                "permisos": [
                    "crear_tabla", "ver_usuarios", "insertar", "usar_base",
                    "crear_base", "eliminar_usuario", "otorgar", "ver_bases",
                    "ver_tablas", "actualizar", "contar", "eliminar", "eliminar_tablas",
                    "crear_usuario"  # ← necesario
                ]
            }
            self.guardar_usuarios()

    def cargar_usuarios(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def guardar_usuarios(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.usuarios, f, indent=2, ensure_ascii=False)

    def agregar_usuario(self, nombre, password):
        if nombre in self.usuarios:
            raise ValueError(f"El usuario '{nombre}' ya existe.")
        self.usuarios[nombre] = {"password": password, "permisos": []}
        self.guardar_usuarios()
        self.usuarios = self.cargar_usuarios()  # 🔄 recarga en memoria


    def otorgar_permiso(self, nombre, permiso):
        if nombre not in self.usuarios:
            raise ValueError("Usuario no encontrado.")
        if permiso not in self.usuarios[nombre]["permisos"]:
            self.usuarios[nombre]["permisos"].append(permiso)
            self.guardar_usuarios()

    def revocar_permiso(self, usuario, permiso):
        if usuario not in self.usuarios:
            raise ValueError(f"El usuario '{usuario}' no existe.")
        if permiso in self.usuarios[usuario]["permisos"]:
            self.usuarios[usuario]["permisos"].remove(permiso)
            self.guardar_usuarios()
            return True
        return False

    def verificar_credenciales(self, nombre, password):
        return (
            nombre in self.usuarios and
            self.usuarios[nombre]["password"] == password
        )
    
    def eliminar_usuario(self, nombre):
        if nombre not in self.usuarios:
            raise ValueError(f"El usuario '{nombre}' no existe.")
        del self.usuarios[nombre]
        self.guardar_usuarios()

    def obtener_permisos(self, nombre):
        return self.usuarios.get(nombre, {}).get("permisos", [])
