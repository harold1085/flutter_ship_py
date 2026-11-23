
from pathlib import Path
from datetime import datetime
import re


class VersionManager:

    def __init__(self):
        self.carpeta_versiones = Path(
            r"C:\MisCredencialesFlutter\versiones"
        )

    def Obtener_mas_reciente(self):

        if not self.carpeta_versiones.exists():
            raise FileNotFoundError(
                "La carpeta de versiones no existe."
            )

        archivos_apk = [
            archivo
            for archivo in self.carpeta_versiones.iterdir()
            if archivo.is_file()
            and archivo.suffix.lower() == ".apk"
        ]

        if not archivos_apk:
            print("No hay archivos APK en la carpeta.")
            return None

        apk_reciente = max(
            archivos_apk,
            key=lambda archivo: archivo.stat().st_mtime
        )

        fecha = datetime.fromtimestamp(
            apk_reciente.stat().st_mtime
        )

        # Buscar y extraer la versión del nombre del APK
        patron = r"_v(\d+)\.(\d+)\.(\d+)$"

        resultado = re.search(
            patron,
            apk_reciente.stem,
            re.IGNORECASE
        )

        if not resultado:
            raise ValueError(
                f"No se encontró una versión válida en: "
                f"{apk_reciente.name}"
            )

        version = {
            "mayor": resultado.group(1),
            "menor": resultado.group(2),
            "parche": resultado.group(3)
        }

        return {
            "version": version,
            "archivo": apk_reciente.name,
            "fecha": fecha
        }

    # Evitar versiones duplicadas
    def existe_version(self, mayor, menor, parche):

        if not self.carpeta_versiones.exists():
            raise FileNotFoundError(
                "La carpeta de versiones no existe."
            )

        version_buscada = (
            f"_v{mayor}.{menor}.{parche}"
        )

        for archivo in self.carpeta_versiones.iterdir():

            if (
                archivo.is_file()
                and archivo.suffix.lower() == ".apk"
            ):
                if archivo.stem.lower().endswith(
                    version_buscada.lower()
                ):
                    return True

        return False
