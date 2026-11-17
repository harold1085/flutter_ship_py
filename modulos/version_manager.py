from pathlib import Path
from datetime import datetime
import re


class versionManager:
    def __init__(self):
        self.carpeta_versiones = Path(r"C:\MisCredencialesFlutter\versiones")

    def Obtener_mas_reciente(self):

        if not self.carpeta_versiones.exists():
            raise FileNotFoundError("La carpeta de versiones no existe.")
            
        archivos_apk= [
            archivo 
            for archivo in self.carpeta_versiones.iterdir()
            if archivo.is_file() and archivo.suflix.lower() == ".apk"
        ]

        if not archivos_apk:
            print("No hay archivos en la carpeta")
            return None

        apk_reciente = max(archivos_apk,key=lambda archivo: archivo.stat().st_mtime)

        fecha=datetime.fromtimestamp(apk_reciente.stat().st_mtime)

        #regex : busqueda y extraccion version mas reciente
        patron = r"_v(\d+)\.(\d+)\.(\d+)(?=\.apk)"

        resultado = re.search(patron,apk_reciente.name,re.IGNORECASE)

        if not resultado:
            raise ValueError(f"NO se encontro version valida en : " f"{apk_reciente.name}")

        version = {
            "mayor": resultado.group(1),
            "menor": resultado.group(2),
            "parche": resultado.group(3)
        }

        return {"version": version}

