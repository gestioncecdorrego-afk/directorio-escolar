import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    # Alineación al inicio (arriba) para evitar el espacio gris
    page.vertical_alignment = "start" 
    page.padding = 20
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        if not t: return ""
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.ListView(expand=True, spacing=15)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busq_orig = txt_busqueda.value.lower().strip()
        busq_limp = normalizar(busq_orig)
        
        if busq_orig:
            for linea in datos_escuelas:
                if busq_orig in linea.lower() or busq_limp in normalizar(linea):
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        inst, loc, dir, tel = [p.strip() for p in partes[:4]]
                        tel_f = "".join(filter(str.isdigit, tel))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15, bgcolor="white", border_radius=10,
                                border=ft.border.all(1, "#E1E1E1"),
                                content=ft.Column([
                                    ft.Text(inst, size=16, weight="bold", color="blue700"),
                                    ft.Text(f"📍 {loc} | Dir: {dir}", size=13),
                                    ft.Row([
                                        ft.ElevatedButton("📞", bgcolor="green", color="white", url=f"tel:{tel_f}", width=60),
                                        ft.ElevatedButton("🗺️", bgcolor="red", color="white", url=f"https://www.google.com/maps/search/{inst.replace(' ', '+')}", width=60),
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
                ft.Text("Directorio Escolar", size=22, weight="bold"),
                txt_busqueda,
                lista_resultados
            )
            page.update()
        else:
            txt_clave.error_text = "Incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave", password=True, on_submit=entrar, width=250)
    
    # Usamos una forma de alineación que Flet 0.82+ siempre acepta
    page.add(
        ft.Column([
            ft.Icon("lock", size=40, color="blue"),
            ft.Text("Ingresar Clave", weight="bold"),
            txt_clave,
            ft.ElevatedButton("Entrar", on_click=entrar)
        ], horizontal_alignment="center")
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
