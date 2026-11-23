
import logging

import flet as ft

from views.release import build_release_screen


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


def main(page: ft.Page):

    # Configuración de la ventana
    page.title = "Flutter Ship - APK Release Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50

    page.window.width = 900
    page.window.height = 750
    page.window.min_width = 650
    page.window.min_height = 600

    # Mostrar pantalla principal
    page.add(
        build_release_screen(page)
    )


if __name__ == "__main__":
    ft.run(main)
