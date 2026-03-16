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
        # Aquí es donde después pondremos la lógica de búsqueda
        print("Botón presionado")
        page.clean()
        page.add(ft.Text("¡Bienvenido al sistema!", size=25, weight=ft.FontWeight.BOLD))
        page.add(ft.Button("Volver", on_click=lambda _: main(page)))

    # --- Interfaz de Bienvenida ---
    
    # Logo o Título
    titulo = ft.Text(
        "Consejo Escolar", 
        size=30, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800
    )

    # Botón de entrada (Actualizado de ElevatedButton a Button)
    btn_entrar = ft.Button(
        text="Entrar al Buscador", 
        on_click=entrar, 
        width=250
    )

    # Contenedor Principal (Aquí corregimos el error de alignment y padding)
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
        # Corregido: Padding.only y Alignment.TOP_CENTER (con Mayúsculas)
        padding=ft.Padding.only(top=50), 
        alignment=ft.Alignment.TOP_CENTER 
    )

    # Agregar todo a la página
    page.add(contenedor_inicio)

# --- Ejecución de la App (Actualizado de app() a run()) ---
if __name__ == "__main__":
    # Render usa la variable de entorno PORT, si no existe usa 8080
    puerto = int(os.getenv("PORT", 8080))
    
    # Usamos ft.run para compatibilidad con las nuevas versiones
    ft.run(main, port=puerto)
