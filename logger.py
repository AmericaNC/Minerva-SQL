#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

import logging
from datetime import datetime
from config_manager import ConfigManager

class SQLLogger:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.config = config_manager.get_modo_depuracion()
        self.setup_logger()
        
    def setup_logger(self):
        logging.basicConfig(
            filename=self.config['log_archivo'],
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def log(self, mensaje, nivel="INFO"):
        config = self.config_manager.get_modo_depuracion()
        
        if nivel not in config['niveles']:
            return
            
        # Log a archivo
        logging.log(getattr(logging, nivel.upper(), logging.INFO), mensaje)
        
        # Mostrar en pantalla si está activado
        if config['mostrar_pantalla']:
            self.mostrar_pantalla(mensaje, nivel)
    
    def mostrar_pantalla(self, mensaje, nivel):
        colores = {
            "LEX": Fore.CYAN,
            "PARSER": Fore.MAGENTA,
            "SEMANTICO": Fore.YELLOW,
            "EXEC": Fore.GREEN,
            "ERROR": Fore.RED
        }
        
        color = colores.get(nivel, Fore.WHITE) if self.config['color'] else ''
        reset = Style.RESET_ALL if self.config['color'] else ''
        
        print(f"{color}[{nivel}] {mensaje}{reset}")