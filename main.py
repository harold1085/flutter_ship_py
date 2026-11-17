from modulos.flutter_builder import FlutterBuilder
from modulos.version_manager import VersionManager

def main():
    version_manager = VersionManager()
    resultado = version_manager.Obtener_mas_reciente()

    if resultado is not None:
        version = resultado["version"]

