
import subprocess
from pathlib import Path


class FlutterBuilder:

    def __init__(self):

        # Ruta del ejecutable Flutter
        self.flutter_path = Path(
            r"C:\flutter_windows_3.47.3-stable\flutter\bin\flutter.bat"
        )

        # Ruta del proyecto Flutter
        self.flutter_project_path = Path(
            r"C:\Proyectos\mi_app_flutter"
        )

        if not self.flutter_path.is_file():
            raise FileNotFoundError(
                f"No se encontró Flutter: {self.flutter_path}"
            )

        if not (self.flutter_project_path / "pubspec.yaml").is_file():
            raise FileNotFoundError(
                f"No se encontró un proyecto Flutter válido: "
                f"{self.flutter_project_path}"
            )

    def build_apk(self):

        command = [
            str(self.flutter_path),
            "build",
            "apk",
            "--release",
            "--target-platform", "android-arm64"            
        ]     

        print("Iniciando compilación Flutter...\n")

        try:
            subprocess.run(
                ["cmd", "/c"] + command,
                cwd=self.flutter_project_path,
                check=True
            )

            apk_path = (
                self.flutter_project_path /
                "build" /
                "app" /
                "outputs" /
                "flutter-apk" /
                "app-release.apk"
            )

            if not apk_path.is_file():
                raise FileNotFoundError(
                    "Flutter terminó, pero no se encontró el APK."
                )

            # Obtener tamaño del APK
            size_mb = apk_path.stat().st_size / (1024 * 1024)

            print("\nAPK generado correctamente.")
            print(f"Ubicación: {apk_path}")
            print(f"Tamaño: {size_mb:.2f} MB")

            return apk_path

        except subprocess.CalledProcessError:
            print("\nError durante la compilación Flutter.")
            raise
