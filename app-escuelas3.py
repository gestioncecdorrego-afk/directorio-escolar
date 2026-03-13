import flet as ft
import os

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    page.scroll = "auto"
    page.padding = 20
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    lista_resultados = ft.ListView(expand=True, spacing=15)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda = txt_busqueda.value.lower().strip()
        if busqueda:
            for linea in datos_escuelas:
                if busqueda in linea.lower():
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        n, l, d, t = partes[0].strip(), partes[1].strip(), partes[2].strip(), partes[3].strip()
                        
                        # Limpiamos el teléfono para la función de llamar
                        tel_limpio = "".join(filter(str.isdigit, t))
                        # Link de Google Maps
                        url_mapa = f"https://www.google.com/maps/search/{n.replace(' ', '+')}+{l.replace(' ', '+')}"

                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15,
                                bgcolor="white",
                                border_radius=10,
                                border=ft.border.all(1, "#E1E1E1"),
                                content=ft.Column([
                                    ft.Text(n, size=18, weight="bold", color="blue"),
                                    ft.Text(f"📍 {l}", size=14),
                                    ft.Text(f"👤 Dir: {d}", size=13, italic=True),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Llamar", 
                                            icon="phone", 
                                            bgcolor="green", 
                                            color="white",
                                            url=f"tel:{tel_limpio}"
                                        ),
                                        ft.ElevatedButton(
                                            "Mapa", 
                                            icon="map", 
                                            bgcolor="red", 
                                            color="white",
                                            url=url_mapa
                                        ),
                                    ], alignment="end")
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(
        label="Buscar escuela o director...", 
        on_change=actualizar_lista,
        border_radius=10,
        prefix_icon="search"
    )

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(
                ft.Text("Directorio Escolar", size=28, weight="bold", color="blue"),
                ft.Text("Consejo Escolar Coronel Dorrego", size=14),
                ft.Divider(height=20),
                txt_busqueda,
                lista_resultados
            )
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            page.update()

    # Pantalla de Login mejorada
    txt_clave = ft.TextField(label="Clave de Acceso", password=True, on_submit=entrar, width=300)
    page.add(
        ft.Container(
            expand=True,
            content=ft.Column([
                ft.Icon("lock", size=50, color="blue"),
                ft.Text("Acceso Restringido", size=20, weight="bold"),
                txt_clave,
                ft.ElevatedButton("Entrar", on_click=entrar, width=200)
            ], horizontal_alignment="center", alignment="center")
        )
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
