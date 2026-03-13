import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    page.scroll = "auto"
    # Esto ayuda a que no aparezca el espacio gris al inicio
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.ListView(expand=True, spacing=15, padding=10)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda_original = txt_busqueda.value.lower().strip()
        busqueda_limpia = normalizar(busqueda_original)
        
        if busqueda_original:
            for linea in datos_escuelas:
                # Buscamos tanto en el texto normal como en el "limpio" (sin guiones)
                if busqueda_original in linea.lower() or busqueda_limpia in normalizar(linea):
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        n, l, d, t = [p.strip() for p in partes[:4]]
                        tel_limpio = "".join(filter(str.isdigit, t))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15, bgcolor="#F0F4F8", border_radius=10,
                                content=ft.Column([
                                    ft.Text(n, size=18, weight="bold", color="blue"),
                                    ft.Text(f"📍 {l} | 👤 {d}", size=14),
                                    ft.Row([
                                        ft.ElevatedButton("Llamar", icon="phone", bgcolor="green", color="white", url=f"tel:{tel_limpio}"),
                                        ft.ElevatedButton("Mapa", icon="map", bgcolor="red", color="white", url=f"https://www.google.com/maps/search/{n.replace(' ', '+')}"),
                                    ], alignment="end")
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar...", on_change=actualizar_lista, border_radius=10, prefix_icon="search")

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.vertical_alignment = ft.MainAxisAlignment.START # Cambiamos al entrar
            page.controls.clear()
            page.add(
                ft.Text("Directorio Escolar", size=25, weight="bold", color="blue"),
                txt_busqueda,
                lista_resultados
            )
            page.update()
        else:
            txt_clave.error_text = "Incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave de Acceso", password=True, on_submit=entrar, width=280, text_align="center")
    
    page.add(
        ft.Icon("lock", size=50, color="blue"),
        ft.Text("Acceso Restringido", size=20, weight="bold"),
        txt_clave,
        ft.ElevatedButton("Entrar", on_click=entrar, width=200)
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
