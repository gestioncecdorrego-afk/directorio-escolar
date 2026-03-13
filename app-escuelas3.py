import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    # Forzamos a que la página no intente centrar nada verticalmente
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 10
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.Column(spacing=15, scroll=ft.ScrollMode.ADAPTIVE)

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
                                        ft.ElevatedButton("Mapa", icon="map", bgcolor="red", color="white", url=f"https://www.google.com/maps/search/{inst.replace(' ', '+')}")
                                    ], alignment="end")
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar...", on_change=actualizar_lista, border_radius=10)

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(
                ft.Column([
                    ft.Text("Directorio Escolar", size=24, weight="bold"),
                    txt_busqueda,
                    lista_resultados
                ], scroll=ft.ScrollMode.ADAPTIVE)
            )
            page.update()
        else:
            txt_clave.error_text = "Incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave", password=True, on_submit=entrar, width=280)
    
    # EL TRUCO: Un contenedor con margen superior negativo o pegado arriba
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Icon("lock", size=50, color="blue"),
                ft.Text("Ingresar Clave", weight="bold"),
                txt_clave,
                ft.ElevatedButton("Entrar", on_click=entrar, width=200)
            ], horizontal_alignment="center"),
            padding=ft.padding.only(top=20), # Lo pega arriba
            alignment=ft.alignment.top_center
        )
    )

if __name__ == "__main__":
    # Sin parámetros extras para que Render no se queje
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
