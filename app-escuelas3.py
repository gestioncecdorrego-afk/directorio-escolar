import flet as ft
import os
import re

def cargar_escuelas():
    escuelas = []
    with open("lista.txt", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split("-")
            if len(partes) >= 4:
                telefono = partes[3].strip()
                telefono = telefono.rstrip("-")
                telefono = telefono.replace("-15-", "-")
                telefono = telefono.replace("-", "")
                escuelas.append({
                    "nombre": partes[0].strip(),
                    "localidad": partes[1].strip(),
                    "director": partes[2].strip(),
                    "telefono": telefono
                })
    return escuelas

def normalizar(texto):
    texto = texto.lower()
    texto = re.sub(r"[.\º]", "", texto)
    texto = texto.replace("nº", "").replace("no", "")
    texto = texto.replace(" ", "")
    return texto

PASSWORD = "consejo2026"

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    escuelas = cargar_escuelas()

    def login_screen():
        page.clean()
        clave = ft.TextField(label="Ingrese contraseña", password=True, can_reveal_password=True, width=300)

        def validar(e):
            if clave.value == PASSWORD:
                entrar()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Contraseña incorrecta"), open=True)
                page.update()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Acceso al Directorio Escolar", size=25, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                    clave,
                    ft.Button(content=ft.Text("Ingresar"), on_click=validar,
                              style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
                padding=30,
                bgcolor=ft.Colors.LIGHT_BLUE_50,
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY)
            )
        )

    def entrar():
        page.clean()
        buscador = ft.TextField(label="Buscar escuela / director / localidad / teléfono", width=400,
                                bgcolor=ft.Colors.LIGHT_BLUE_100, border_radius=8)
        lista = ft.Column()

        def buscar(e):
            query = normalizar(buscador.value)
            resultados = [
                esc for esc in escuelas
                if query in normalizar(esc["nombre"])
                or query in normalizar(esc["localidad"])
                or query in normalizar(esc["director"])
                or query in normalizar(esc["telefono"])
            ]
            lista.controls = []
            for esc in resultados:
                tarjeta = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(esc["nombre"], size=20),
                            ft.Text(f"Localidad: {esc['localidad']}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Director/a: {esc['director']}", weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Column([
                                    ft.IconButton(
                                        icon=ft.Icons.PHONE,
                                        icon_color=ft.Colors.WHITE,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.GREEN,
                                            shape=ft.RoundedRectangleBorder(radius=8)
                                        ),
                                        url=f"tel:{esc['telefono']}"
                                    ),
                                    ft.Text("Llamar", size=12)
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Column([
                                    ft.IconButton(
                                        icon=ft.Icons.LOCATION_ON,
                                        icon_color=ft.Colors.WHITE,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.Colors.RED,
                                            shape=ft.RoundedRectangleBorder(radius=8)
                                        ),
                                        url=f"https://www.google.com/maps/search/{esc['nombre']} {esc['localidad']}"
                                    ),
                                    ft.Text("Mapa", size=12)
                                ], alignment=ft.MainAxisAlignment.CENTER)
                            ], spacing=40)
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.LIGHT_BLUE_50,
                        border_radius=12,
                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY)
                    )
                )
                lista.controls.append(tarjeta)
            page.update()

        buscador.on_change = buscar

        page.add(
            ft.Text("Panel de Búsqueda", size=25, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
            buscador,
            lista,
            ft.Button(content=ft.Text("Cerrar sesión"), on_click=lambda _: login_screen(),
                      style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE))
        )

    login_screen()

if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 8080))
    ft.run(main, port=puerto, host="0.0.0.0")
