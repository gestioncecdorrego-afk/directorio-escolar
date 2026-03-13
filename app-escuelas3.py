import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    page.padding = 20
    # Quitamos alineaciones raras para que cargue por defecto
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(t):
        return "".join(re.findall(r'[a-z0-9]', t.lower()))

    lista_resultados = ft.Column(spacing=15, scroll="auto")

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda = txt_busqueda.value.lower().strip()
        if busqueda:
            busq_limp = normalizar(busqueda)
            for linea in datos_escuelas:
                if busqueda in linea.lower() or busq_limp in normalizar(linea):
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        inst, loc, dir, tel = [p.strip() for p in partes[:4]]
                        tel_f = "".join(filter(str.isdigit, tel))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=10, bgcolor="#f0f0f0", border_radius=10,
                                content=ft.Column([
                                    ft.Text(inst, size=16, weight="bold"),
                                    ft.Text(f"{loc} - {dir}"),
                                    ft.Row([
                                        ft.TextButton("📞", url=f"tel:{tel_f}"),
                                        ft.TextButton("📍", url=f"https://www.google.com/maps/search/{inst.replace(' ', '+')}")
                                    ])
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar...", on_change=actualizar_lista)

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

    txt_clave = ft.TextField(label="Clave", password=True, on_submit=entrar)
    
    # Usamos el botón nuevo que pide el sistema para evitar avisos
    page.add(
        ft.Text("Ingresar Clave"),
        txt_clave,
        ft.FilledButton("Entrar", on_click=entrar)
    )

if __name__ == "__main__":
    # Arrancamos de la forma más simple posible
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
