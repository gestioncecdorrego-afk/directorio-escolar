import flet as ft
import os

def main(page: ft.Page):
    # Configuración básica para evitar errores de visualización
    page.title = "Directorio Escolar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    def entrar(e):
        page.clean()
        page.add(
            ft.Text("¡Bienvenido al sistema!", size=25),
            ft.ElevatedButton("Volver", on_click=lambda _: main(page))
        )

    # USAMOS ELEVATEDBUTTON: Es el que NO falla con el argumento 'text'
    btn_entrar = ft.ElevatedButton(
        text="Entrar al Buscador",
        on_click=entrar,
        width=250
    )

    # Contenedor con la sintaxis de Clases (Mayúsculas) que pide la versión 0.82.2
    inicio = ft.Container(
        content=ft.Column(
            [
                ft.Text("Consejo Escolar", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Sistema de búsqueda", size=16),
                ft.Divider(height=20),
                btn_entrar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(top=50),
        alignment=ft.Alignment.TOP_CENTER
    )

    page.add(inicio)

if __name__ == "__main__":
    # Render necesita el puerto de la variable de entorno
    port_env = os.getenv("PORT", "8080")
    
    # IMPORTANTE: Usamos 0.0.0.0 para que Render pueda "ver" la app desde afuera
    ft.app(target=main, port=int(port_env), host="0.0.0.0")
