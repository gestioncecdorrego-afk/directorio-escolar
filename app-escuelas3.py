import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    # Quitamos alineaciones centradas que causan el error gris
    page.vertical_alignment = "start"
    page.horizontal_alignment = "start"
    page.padding = 20
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.ListView(expand=True, spacing=15)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda_original = txt_busqueda.value.lower().strip()
        busqueda_limpia = normalizar(busqueda_original)
        
        if busqueda_original:
            for linea in datos_escuelas:
                if busqueda_original in linea.lower() or busqueda_limpia in normalizar(linea):
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        inst, loc, dir, tel = [p.strip() for p in partes[:4]]
                        tel_limpio = "".join(filter(str.isdigit, tel))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15, bgcolor="#F0F4F8", border_radius=10,
                                content=ft.Column([
                                    ft.Text(inst, size=18, weight="bold", color="blue"),
                                    ft.Text(f"📍 {loc} | 👤 {dir}", size=14),
                                    ft.Row([
                                        ft.ElevatedButton("Llamar", icon="phone", bgcolor="green", color="white", url=f"tel:{tel_limpio}"),
                                        ft.ElevatedButton("Mapa", icon="map", bgcolor="red", color="white", url=f"http://google.com/maps/search/{inst.replace(' ', '+')}+{loc.replace(' ', '+')}"),
                                    ], alignment="end")
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar...", on_change=actualizar_lista, border_radius=10, prefix_icon="search")

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(
                ft.Text("Directorio Escolar", size=24, weight="bold", color="blue"),
                ft.Text("Consejo Escolar Dorrego", size=12),
                ft.Divider(),
                txt_busqueda,
                lista_resultados
            )
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            page.update()

    # Login simple al principio de la página para que se vea en el celu
    txt_clave = ft.TextField(label="Clave de Acceso", password=True, on_submit=entrar, width=300)
    
    page.add(
        ft.Column([
            ft.Icon("lock", size=40, color="blue"),
            ft.Text("Ingresar Clave", size=18, weight="bold"),
            txt_clave,
            ft.ElevatedButton("Entrar", on_click=entrar, width=200)
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
