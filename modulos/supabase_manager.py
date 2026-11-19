
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

        print("URL:", repr(self.supabase_url))
        print("Longitud URL:", len(self.supabase_url))

        if not self.supabase_url:
            raise ValueError("Falta SUPABASE_URL")

        if not self.supabase_key:
            raise ValueError("Falta SUPABASE_KEY")

        if not self.bucket_name:
            raise ValueError("Falta SUPABASE_BUCKET")

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
