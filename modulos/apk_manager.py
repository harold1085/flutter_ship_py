import shutil
from pathlib import Path


class APKManager:

    def __init__(self, destination_folder):

        self.destination_folder = Path(destination_folder)

        self.destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def prepare_apk(self, apk_path, app_name, version):

        apk_path = Path(apk_path)

        if not apk_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el APK: {apk_path}"
            )

        new_filename = f"{app_name}_v{version}.apk"

        destination_path = self.destination_folder / new_filename

        if destination_path.exists():
            raise FileExistsError(
                f"Ya existe un APK con esta versión: {destination_path}"
            )

        shutil.copy2(
            apk_path,
            destination_path
        )

        print("\nAPK preparado correctamente.")
        print(f"Archivo: {new_filename}")
        print(f"Ubicación: {destination_path}")

        return destination_path