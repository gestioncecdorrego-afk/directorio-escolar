import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    page.scroll = "auto"
    page.padding = 15
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.Column(spacing=15)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda = txt_busqueda.value.lower().strip()
        if busqueda:
            busq_limp = normalizar(busqueda)
            for linea in datos_escuelas:
                if busqueda in linea.lower() or busq_limp in normalizar(linea):
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        inst, loc, dir_esc, tel = [p.strip() for p in partes[:4]]
                        tel_link = "".join(filter(str.isdigit, tel))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15, bgcolor="white", border_radius=10,
                                border=ft.border.all(1, "#E1E1E1"),
                                content=ft.Column([
                                    ft.Text(inst, size=18, weight="bold", color="blue700"),
                                    ft.Text(f"📍 {loc} | 👤 {dir_esc}", size=14),
                                    ft.Text(f"📞 {tel}", size=16, weight="bold"),
                                    ft.Row([
                                        ft.ElevatedButton("Llamar", icon="phone", bgcolor="green", color="white", url=f"tel:{tel_link}"),
                                        ft.ElevatedButton("Mapa", icon="map", bgcolor="red", color="white", url=f"https://www.google.com/maps/search/{inst.replace(' ', '+')}"),
                                    ], alignment="end")
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar...", on_change=actualizar_lista, border_radius=10)

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(ft.Text("Directorio Escolar", size=24, weight="bold"), txt_busqueda, lista_resultados)
            page.update()
        else:
            txt_clave.error_text = "Incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave", password=True, on_submit=entrar, width=280)
    page.add(ft.Column([ft.Icon("lock", size=50), txt_clave, ft.ElevatedButton("Entrar", on_click=entrar)], horizontal_alignment="center"))

if __name__ == "__main__":
    # Usamos "simple-http" que es el salvavidas para Python 3.14
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))

