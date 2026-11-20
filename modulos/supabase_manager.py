
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


class SupabaseManager:

    def __init__(self):

        # Cargar variables de entorno
        BASE_DIR = Path(__file__).resolve().parent.parent
        load_dotenv(BASE_DIR / ".env")

        print("Ruta del .env:", BASE_DIR / ".env")
        print("¿Existe el archivo?:", (BASE_DIR / ".env").is_file())
        print("URL encontrada:", bool(os.getenv("SUPABASE_URL")))

        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.bucket_name = os.getenv("SUPABASE_BUCKET")
        
        if not self.supabase_url:
            raise ValueError("Falta SUPABASE_URL")

        if not self.supabase_key:
            raise ValueError("Falta SUPABASE_KEY")

        if not self.bucket_name:
            raise ValueError("Falta SUPABASE_BUCKET")

        print("URL:", self.supabase_url)
        print("Longitud URL:", len(self.supabase_url))

        # Crear cliente Supabase
        self.supabase = create_client(
            self.supabase_url,
            self.supabase_key
        )

    def probar_conexion(self):

        try:

            buckets = self.supabase.storage.list_buckets()

            print("Conexión con Supabase exitosa.")

            for bucket in buckets:
                print(f"Bucket encontrado: {bucket.name}")

            return True

        except Exception as error:

            print(f"Error de conexión: {error}")

            return False

    def subir_apk(self, apk_path):

        apk_path = Path(apk_path)

        if not apk_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el APK: {apk_path}"
            )

        # Nombre directo del archivo en el bucket
        remote_path = apk_path.name

        try:

            with apk_path.open("rb") as apk_file:

                response = self.supabase.storage \
                    .from_(self.bucket_name) \
                    .upload(
                        path=remote_path,
                        file=apk_file,
                        file_options={
                            "content-type": "application/vnd.android.package-archive",
                            "upsert": "false"
                        }
                    )

            print("\nAPK subido correctamente.")
            print(f"Bucket: {self.bucket_name}")
            print(f"Archivo remoto: {remote_path}")

            return response

        except Exception as error:

            print(f"Error al subir APK: {error}")
            raise
