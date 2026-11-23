
import asyncio
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

        if not (
            self.flutter_project_path / "pubspec.yaml"
        ).is_file():
            raise FileNotFoundError(
                f"No se encontró un proyecto Flutter válido: "
                f"{self.flutter_project_path}"
            )

    async def build_apk(self, on_output=None):

        command = [
            str(self.flutter_path),
            "build",
            "apk",
            "--release",
            "--target-platform",
            "android-arm64",
        ]

        print("Iniciando compilación Flutter...\n")

        process = await asyncio.create_subprocess_exec(
            "cmd",
            "/c",
            *command,
            cwd=str(self.flutter_project_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        try:
            while True:
                line = await process.stdout.readline()

                if not line:
                    break

                output = line.decode(
                    "utf-8",
                    errors="replace"
                ).rstrip()

                if output:
                    print(output)

                    if on_output:
                        on_output(output)

            return_code = await process.wait()

            if return_code != 0:
                raise RuntimeError(
                    f"Flutter terminó con código de error: {return_code}"
                )

            apk_path = (
                self.flutter_project_path
                / "build"
                / "app"
                / "outputs"
                / "flutter-apk"
                / "app-release.apk"
            )

            if not apk_path.is_file():
                raise FileNotFoundError(
                    "Flutter terminó, pero no se encontró el APK."
                )

            size_mb = apk_path.stat().st_size / (1024 * 1024)

            print("\nAPK generado correctamente.")
            print(f"Ubicación: {apk_path}")
            print(f"Tamaño: {size_mb:.2f} MB")

            return apk_path

        except asyncio.CancelledError:
            if process.returncode is None:
                process.kill()
                await process.wait()
            raise

