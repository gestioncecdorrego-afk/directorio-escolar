import flet as ft
import os

def main(page: ft.Page):
    # --- Configuración de la Página ---
    page.title = "Directorio Escolar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # --- Lógica de Navegación Simple ---
    def entrar(e):
        print("Botón presionado")
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("¡Bienvenido al sistema!", size=25, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Volver", on_click=lambda _: main(page))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding.only(top=50)
            )
        )

    # --- Interfaz de Bienvenida ---
    
    titulo = ft.Text(
        "Consejo Escolar", 
        size=30, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800
    )

    # Usamos ElevatedButton que es el que acepta 'text' sin problemas
    btn_entrar = ft.ElevatedButton(
        text="Entrar al Buscador", 
        on_click=entrar, 
        width=250
    )

    contenedor_inicio = ft.Container(
        content=ft.Column(
            controls=[
                titulo,
                ft.Text("Sistema de búsqueda de instituciones", size=16),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                btn_entrar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.only(top=50), 
        alignment=ft.Alignment.TOP_CENTER 
    )

    page.add(contenedor_inicio)

# --- Ejecución de la App ---
if __name__ == "__main__":
    puerto = int(os.getenv("PORT", 8080))
    # Usamos ft.app para asegurar compatibilidad total en Render por ahora
    ft.app(target=main, port=puerto, view=ft.AppView.WEB_BROWSER)
