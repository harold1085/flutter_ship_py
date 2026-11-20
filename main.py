from modulos.apk_manager import APKManager
from modulos.supabase_manager import SupabaseManager
from pathlib import Path

def main():

    apk_manager = APKManager(r"C:\MisCredencialesFlutter\versiones")
    # preparacion del apk
    apk_preparado = apk_manager.prepare_apk(
        apk_path=Path(r"C:\Proyectos\mi_app_flutter\build\app\outputs\flutter-apk\app-release.apk"),
        app_name="AnamariaGarden",
        version="1.0.0"
    )

    # conexion a supabse
    supabase_manager = SupabaseManager()

    # Comprobacion de  conexión
    if not supabase_manager.probar_conexion():
        print("No fue posible conectar con Supabase.")
        return

    # se sube a supabase storage
    supabase_manager.subir_apk(
        apk_path=apk_preparado
    )


if __name__ == "__main__":
    main()