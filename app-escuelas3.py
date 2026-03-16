import flet as ft
import os

def main(page: ft.Page):
    # Configuración de página estable
    page.title = "Directorio Escolar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    def entrar(e):
        page.clean()
        page.add(
            ft.Text("Panel de Búsqueda", size=25, weight=ft.FontWeight.BOLD),
            ft.Text("Aquí irá la lista de escuelas...", size=16),
            ft.ElevatedButton("Volver al Inicio", on_click=lambda _: main(page))
        )

    # Título principal
    titulo = ft.Text(
        "Consejo Escolar", 
        size=30, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800
    )

    # BOTÓN ESTABLE: ElevatedButton siempre acepta 'text'
    btn_entrar = ft.ElevatedButton(
        text="Entrar al Buscador",
        on_click=entrar,
        width=250
    )

    # Contenedor usando Clases (Mayúsculas) para evitar errores de atributo
    inicio = ft.Container(
        content=ft.Column(
            [
                titulo,
                ft.Text("Sistema de búsqueda de instituciones", size=16),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                btn_entrar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(top=50),
        alignment=ft.Alignment.TOP_CENTER
    )

    page.add(inicio)

if __name__ == "__main__":
    # Render configuración de puerto
    puerto = int(os.getenv("PORT", 8080))
    
    # Usamos host="0.0.0.0" para que Render detecte la app correctamente
    ft.app(target=main, port=puerto, host="0.0.0.0")
