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
        if not t: return ""
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
                        tel_f = "".join(filter(str.isdigit, tel))
                        
                        lista_resultados.controls.append(
                            ft.Container(
                                padding=15, 
                                bgcolor="white", 
                                border_radius=12,
                                border=ft.border.all(1, "#E1E1E1"),
                                shadow=ft.BoxShadow(blur_radius=4, color="grey300"),
                                content=ft.Column([
                                    ft.Text(inst, size=18, weight="bold", color="blue700"),
                                    ft.Text(f"📍 {loc}", size=14, color="black"),
                                    ft.Text(f"👤 Dir: {dir}", size=13, italic=True, color="grey700"),
                                    ft.Row([
                                        ft.ElevatedButton("WhatsApp", icon="share", bgcolor="blue", color="white", url=f"https://wa.me/?text=Escuela:%20{inst}%0ADir:%20{dir}%0ATel:%20{tel}"),
                                        ft.ElevatedButton("Llamar", icon="phone", bgcolor="green700", color="white", url=f"tel:{tel_f}"),
                                        ft.ElevatedButton("Mapa", icon="map", bgcolor="red700", color="white", url=f"https://www.google.com/maps/search/{inst.replace(' ', '+')}+{loc.replace(' ', '+')}"),
                                    ], alignment="end", wrap=True)
                                ])
                            )
                        )
        page.update()

    txt_busqueda = ft.TextField(
        label="Buscar...", 
        on_change=actualizar_lista, 
        border_radius=15, 
        prefix_icon="search",
        filled=True
    )

    def entrar(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(
                ft.Text("Directorio Escolar", size=26, weight="bold", color="blue800"),
                ft.Text("Consejo Escolar Coronel Dorrego", size=13),
                ft.Divider(height=20),
                txt_busqueda,
                lista_resultados
            )
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            page.update()

    txt_clave = ft.TextField(label="Clave de Acceso", password=True, on_submit=entrar, width=280, text_align="center")
    
    page.add(
        ft.Container(
            padding=50,
            content=ft.Column([
                ft.Icon("lock_outline", size=60, color="blue800"),
                ft.Text("Acceso Restringido", size=22, weight="bold"),
                txt_clave,
                ft.ElevatedButton("Entrar", on_click=entrar, width=200)
            ], horizontal_alignment="center")
        )
    )

if __name__ == "__main__":
    # Usamos ft.app directamente sin parámetros extra para que no tire error en Python 3.14
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
