
import asyncio
import logging
import re
import sys

import flet as ft

from modulos.apk_manager import APKManager
from modulos.flutter_builder import FlutterBuilder
from modulos.supabase_manager import SupabaseManager
from modulos.version_manager import VersionManager


log = logging.getLogger(f"app.{__name__}")


def build_release_screen(page: ft.Page):

    # Inicializar administradores
    version_manager = VersionManager()
    builder = FlutterBuilder()
    storage = SupabaseManager()

    apk_manager = APKManager(
        version_manager.carpeta_versiones
    )

    # Obtener última versión local
    initial_release = None
    initial_notice = ""

    try:
        initial_release = version_manager.Obtener_mas_reciente()

        if initial_release is None:
            initial_notice = (
                "Aún no hay APKs versionadas en la carpeta local."
            )

    except (FileNotFoundError, ValueError) as exc:
        initial_notice = str(exc)

    current_version = (initial_release or {}).get("version", {})

    current_major = current_version.get("mayor", "0")
    current_minor = current_version.get("menor", "0")
    current_patch = current_version.get("parche", "0")

    latest_file = (initial_release or {}).get("archivo")

    # Campos de versión
    major_field = ft.TextField(
        label="Mayor",
        value=current_major,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLUE_GREY_900,
        label_style=ft.TextStyle(
            color=ft.Colors.BLUE_GREY_600
        ),
        expand=True,
    )

    minor_field = ft.TextField(
        label="Menor",
        value=current_minor,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLUE_GREY_900,
        label_style=ft.TextStyle(
            color=ft.Colors.BLUE_GREY_600
        ),
        expand=True,
    )

    patch_field = ft.TextField(
        label="Patch",
        value=current_patch,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLUE_GREY_900,
        label_style=ft.TextStyle(
            color=ft.Colors.BLUE_GREY_600
        ),
        expand=True,
    )    
    
    tipo_actualizacion_field = ft.Dropdown(
        label="Tipo de actualización",
        value="opcional",
        options=[
            ft.dropdown.Option(
                key="obligatoria",
                text="Obligatoria",
            ),
            ft.dropdown.Option(
                key="opcional",
                text="Opcional",
            ),
        ],
        border_color=ft.Colors.BLUE_GREY_300,
        focused_border_color=ft.Colors.BLUE_GREY_600,
        color=ft.Colors.BLUE_GREY_900,
        expand=True,
    )


    latest_text = ft.Text(
        f"APK local: {latest_file}"
        if latest_file
        else "APK local: sin publicaciones",
        size=13,
        color=ft.Colors.BLUE_GREY_600,
    )

    notice_text = ft.Text(
        initial_notice,
        size=12,
        color=ft.Colors.BLUE_GREY_600,
        visible=bool(initial_notice),
    )

    status_text = ft.Text(
        "Listo para crear una versión nueva.",
        size=14,
        color=ft.Colors.BLUE_GREY_900,
    )

    output_text = ft.Text(
        "",
        size=12,
        color=ft.Colors.BLUE_GREY_600,
        max_lines=2,
        overflow=ft.TextOverflow.ELLIPSIS,
    )

    progress_bar = ft.ProgressBar(
        value=0,
        visible=False,
    )

    create_button = ft.Button(
        content="Crear y subir APK",
        bgcolor=ft.Colors.BLUE_GREY_800,
        color=ft.Colors.WHITE,
    )

    # Proceso de compilación y publicación
    async def create_and_upload():

        if sys.platform != "win32":
            status_text.value = (
                "La compilación necesita la aplicación de escritorio "
                "en Windows; no funciona desde el preview web."
            )
            status_text.color = ft.Colors.RED_700
            page.update()
            return

        # Validar versión
        parts = [
            major_field.value or "",
            minor_field.value or "",
            patch_field.value or "",
        ]

        if any(
            not re.fullmatch(r"\d+", part.strip())
            for part in parts
        ):
            status_text.value = (
                "Ingresa números enteros en los tres campos de versión."
            )
            status_text.color = ft.Colors.RED_700
            page.update()
            return

        major, minor, patch = (
            part.strip() for part in parts
        )

        version = f"{major}.{minor}.{patch}"

        # Comprobar versiones duplicadas
        try:
            version_manager.carpeta_versiones.mkdir(
                parents=True,
                exist_ok=True,
            )

            if version_manager.existe_version(
                major,
                minor,
                patch,
            ):
                status_text.value = (
                    f"La versión {version} ya existe en el archivo local."
                )
                status_text.color = ft.Colors.RED_700
                page.update()
                return

        except Exception as exc:
            status_text.value = str(exc)
            status_text.color = ft.Colors.RED_700
            page.update()
            return

        # Preparar interfaz
        create_button.disabled = True

        progress_bar.visible = True
        progress_bar.value = None

        output_text.value = ""

        status_text.value = (
            "Compilando APK release para Android arm64…"
        )
        status_text.color = ft.Colors.BLUE_GREY_800

        page.update()

        prepared_path = None

        try:

            # Mostrar salida de Flutter
            def show_build_line(line):
                if line:
                    output_text.value = line
                    page.update()

            # 1. Compilar APK
            generated_apk = await builder.build_apk(
                on_output=show_build_line
            )

            status_text.value = (
                "Compilación terminada. Preparando APK versionada…"
            )
            page.update()

            # 2. Preparar APK versionada
            prepared_path = await asyncio.to_thread(
                apk_manager.prepare_apk,
                generated_apk,
                builder.flutter_project_path.name,
                version,
            )

            status_text.value = (
                f"Subiendo {prepared_path.name} a Supabase…"
            )

            output_text.value = ""
            page.update()

            # 3. Subir APK a Supabase
            await asyncio.to_thread(
                storage.subir_apk,
                prepared_path,
            )

            # 4. Actualizar interfaz
            status_text.value = (
                f"¡Versión {version} creada y subida correctamente!"
            )

            status_text.color = ft.Colors.GREEN_800

            latest_text.value = (
                f"APK local: {prepared_path.name}"
            )

            notice_text.visible = False

            major_field.value = major
            minor_field.value = minor
            patch_field.value = patch

            log.info(
                "APK publicada: %s",
                prepared_path.name,
            )

        except Exception as exc:

            # Eliminar APK local si la publicación falla
            if (
                prepared_path is not None
                and prepared_path.exists()
            ):
                try:
                    prepared_path.unlink()

                except OSError:
                    log.exception(
                        "No se pudo borrar el archivo no publicado %s",
                        prepared_path,
                    )

            status_text.value = (
                f"No se pudo completar la publicación: {exc}"
            )

            status_text.color = ft.Colors.RED_700

            log.exception(
                "Falló la creación o subida de la APK"
            )

        finally:

            progress_bar.value = 1
            progress_bar.visible = False

            create_button.disabled = False

            page.update()

    # Evento del botón
    async def handle_create(_):
        await create_and_upload()

    create_button.on_click = handle_create

    # Tarjeta principal
    card = ft.Container(
        max_width=660,
        padding=28,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(
            1,
            ft.Colors.BLUE_GREY_100,
        ),
        border_radius=20,
        content=ft.Column(
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[

                # Encabezado
                ft.Column(
                    spacing=6,
                    controls=[
                    ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Image(
                                src="icon.svg",
                                width=48,
                                height=48,
                            ),
                            ft.Text(
                                "FLUTTER SHIP",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_900,
                                    ),
                            ],
                        ),
                        ft.Text(
                            "Compila, versiona y publica tu release de Flutter.",
                            size=14,
                            color=ft.Colors.BLUE_GREY_600,
                        ),
                    ],
                ),

                # Última versión local
                ft.Container(
                    padding=16,
                    bgcolor=ft.Colors.BLUE_GREY_50,
                    border_radius=14,
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text(
                                "ÚLTIMA VERSIÓN LOCAL",
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_600,
                            ),

                            ft.Text(
                                f"{current_major}.{current_minor}.{current_patch}",
                                size=26,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_GREY_900,
                            ),

                            latest_text,
                        ],
                    ),
                ),


                # Nueva versión
                ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text(
                            "Nueva versión",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.BLUE_GREY_900,
                        ),

                        ft.Row(
                            spacing=12,
                            controls=[
                                major_field,
                                minor_field,
                                patch_field,
                            ],
                        ),

                        tipo_actualizacion_field,
                    ],
                ),


                create_button,
                progress_bar,
                status_text,
                output_text,
                notice_text,

                ft.Text(
                    "Supabase: .env con SUPABASE_URL y SUPABASE_KEY · "
                    "bucket: SUPABASE_BUCKET (predeterminado: apks)",
                    size=11,
                    color=ft.Colors.BLUE_GREY_500,
                ),
            ],
        ),
    )

    return ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            padding=24,
            alignment=ft.Alignment.CENTER,
            content=card,
        ),
    )
