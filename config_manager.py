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
from colorama import Fore, Style

class ConfigManager:
    def __init__(self, archivo='config.json'):
        self.archivo = archivo
        self.config = self.cargar_config()
        
    def cargar_config(self):
        try:
            with open(self.archivo, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config_default = {
                "depuracion": {
                    "activo": False,
                    "niveles": ["LEX", "PARSER"],
                    "log_archivo": "debug.log",
                    "mostrar_pantalla": True,
                    "color": True
                },
                "configuracion": {
                    "usuario_actual": None,
                    "base_actual": None
                }
            }
            self.guardar_config(config_default)
            return config_default
    
    def guardar_config(self, config=None):
        with open(self.archivo, 'w') as f:
            json.dump(config or self.config, f, indent=4)
    
    def actualizar_config(self, nueva_config):
        self.config.update(nueva_config)
        self.guardar_config()
    
    def toggle_depuracion(self, estado=None):
        if estado is None:
            estado = not self.config['depuracion']['activo']
        self.config['depuracion']['activo'] = estado
        self.guardar_config()
        return estado
    
    def get_modo_depuracion(self):
        return self.config['depuracion']