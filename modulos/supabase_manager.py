
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


class SupabaseManager:

    def __init__(self):

        # Localizar y cargar el archivo .env
        base_dir = Path(__file__).resolve().parent.parent
        env_path = base_dir / ".env"

        load_dotenv(env_path)

        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.bucket_name = os.getenv("SUPABASE_BUCKET")

        # Validar variables de entorno
        if not self.supabase_url:
            raise ValueError("Falta SUPABASE_URL en el archivo .env")

        if not self.supabase_key:
            raise ValueError("Falta SUPABASE_KEY en el archivo .env")

        if not self.bucket_name:
            raise ValueError("Falta SUPABASE_BUCKET en el archivo .env")

        # Crear cliente Supabase
        self.supabase = create_client(
            self.supabase_url,
            self.supabase_key
        )

    def probar_conexion(self):

        try:
            buckets = self.supabase.storage.list_buckets()

            print("Conexión con Supabase exitosa.")

            bucket_encontrado = False

            for bucket in buckets:
                print(f"Bucket encontrado: {bucket.name}")

                if bucket.name == self.bucket_name:
                    bucket_encontrado = True

            if not bucket_encontrado:
                print(
                    f"No se encontró el bucket: {self.bucket_name}"
                )
                return False

            print(f"Bucket configurado correctamente: {self.bucket_name}")

            return True

        except Exception as error:
            print(f"Error de conexión con Supabase: {error}")
            return False

    def subir_apk(self, apk_path):

        apk_path = Path(apk_path)

        # Validar existencia del archivo
        if not apk_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el APK: {apk_path}"
            )

        # Validar extensión
        if apk_path.suffix.lower() != ".apk":
            raise ValueError(
                f"El archivo no tiene extensión APK: {apk_path}"
            )

        # Nombre del archivo en Supabase Storage
        remote_path = apk_path.name

        try:
            with apk_path.open("rb") as apk_file:

                response = (
                    self.supabase.storage
                    .from_(self.bucket_name)
                    .upload(
                        path=remote_path,
                        file=apk_file,
                        file_options={
                            "content-type": "application/vnd.android.package-archive",
                            "upsert": "false"
                        }
                    )
                )

            print("\nAPK subido correctamente.")
            print(f"Bucket: {self.bucket_name}")
            print(f"Archivo remoto: {remote_path}")

            return response

        except Exception as error:
            print(f"Error al subir APK: {error}")
            raise
