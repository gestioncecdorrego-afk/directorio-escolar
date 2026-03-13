import flet as ft
import os

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = "light"
    page.scroll = "auto"
    
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    lista_resultados = ft.ListView(expand=True, spacing=10)

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        busqueda = txt_busqueda.value.lower().strip()
        if busqueda:
            for linea in datos_escuelas:
                if busqueda in linea.lower():
                    partes = linea.split("-")
                    if len(partes) >= 4:
                        n, l, d, t = partes[0], partes[1], partes[2], partes[3]
                        lista_resultados.controls.append(
                            ft.ListTile(
                                title=ft.Text(n, weight="bold"),
                                subtitle=ft.Text(f"{l} - Dir: {d}"),
                                trailing=ft.Text(t),
                                on_click=lambda _: None
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(label="Buscar escuela...", on_change=actualizar_lista)

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(ft.Text("Directorio Escolar", size=25, weight="bold"), txt_busqueda, lista_resultados)
            page.update()
        else:
            txt_clave.error_text = "Incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave", password=True, on_submit=entrar)
    page.add(ft.Text("Ingresar Clave"), txt_clave, ft.ElevatedButton("Entrar", on_click=entrar))

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
