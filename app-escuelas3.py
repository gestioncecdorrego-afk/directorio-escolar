import flet as ft
import os

def cargar_escuelas():
    escuelas = []
    with open("lista.txt", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split("-")
            if len(partes) >= 4:
                telefono = partes[3].strip().rstrip("-")
                # quitar el "15" si aparece después del código de área
                telefono = telefono.replace("-15-", "-")
                escuelas.append({
                    "nombre": partes[0].strip(),
                    "localidad": partes[1].strip(),
                    "director": partes[2].strip(),
                    "telefono": telefono
                })
    return escuelas

PASSWORD = "consejo2026"

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

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
            ft.Text("Acceso al Directorio Escolar", size=25, weight=ft.FontWeight.BOLD),
            clave,
            ft.ElevatedButton(content=ft.Text("Ingresar"), on_click=validar)
        )

    def entrar():
        page.clean()
        buscador = ft.TextField(label="Buscar escuela / director / localidad / teléfono", width=400)
        lista = ft.Column()

        def buscar(e):
            query = buscador.value.lower()
            resultados = [
                esc for esc in escuelas
                if query in esc["nombre"].lower()
                or query in esc["localidad"].lower()
                or query in esc["director"].lower()
                or query in esc["telefono"].lower()
            ]
            lista.controls = []
            for esc in resultados:
                fila = ft.Row([
                    ft.Text(f"{esc['nombre']} - {esc['localidad']} - {esc['director']} - {esc['telefono']}"),
                    ft.ElevatedButton(
                        content=ft.Text("Llamar"),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                        url=f"tel:{esc['telefono']}"
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("Mapa"),
                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                        url=f"https://www.google.com/maps/search/{esc['localidad']}"
                    )
                ])
                lista.controls.append(fila)
            page.update()

        buscador.on_change = buscar

        page.add(
            ft.Text("Panel de Búsqueda", size=25, weight=ft.FontWeight.BOLD),
            buscador,
            lista,
            ft.ElevatedButton(content=ft.Text("Cerrar sesión"), on_click=lambda _: login_screen())
        )

    login_screen()

if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 8080))
    ft.run(main, port=puerto, host="0.0.0.0")
