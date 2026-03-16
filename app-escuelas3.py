import flet as ft
import os
import csv

# Función para cargar datos desde un CSV
def cargar_escuelas():
    escuelas = []
    try:
        with open("escuelas.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                escuelas.append(row)
    except FileNotFoundError:
        print("Archivo 'escuelas.csv' no encontrado.")
    return escuelas

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    escuelas = cargar_escuelas()

    def entrar(e):
        page.clean()

        buscador = ft.TextField(label="Buscar escuela", width=300)

        lista = ft.Column()

        def buscar(e):
            query = buscador.value.lower()
            resultados = [
                esc for esc in escuelas
                if query in esc["nombre"].lower()
                or query in esc["director"].lower()
            ]
            lista.controls = [
                ft.Text(f"{esc['nombre']} - {esc['director']} - {esc['direccion']} - {esc['telefono']}")
                for esc in resultados
            ]
            page.update()

        page.add(
            ft.Text("Panel de Búsqueda", size=25, weight=ft.FontWeight.BOLD),
            buscador,
            ft.ElevatedButton(content=ft.Text("Buscar"), on_click=buscar),
            lista,
            ft.ElevatedButton(content=ft.Text("Volver al Inicio"), on_click=lambda _: main(page))
        )

    titulo = ft.Text(
        "Consejo Escolar",
        size=30,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800
    )

    btn_entrar = ft.ElevatedButton(
        content=ft.Text("Entrar al Buscador"),
        on_click=entrar,
        width=250
    )

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
    puerto = int(os.getenv("PORT", 8080))
    ft.app(target=main, port=puerto, host="0.0.0.0")
