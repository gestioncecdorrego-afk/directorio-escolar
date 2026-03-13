import flet as ft
import os
import re

def main(page: ft.Page):
    page.title = "Directorio Escolar - C. Dorrego"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    
    # --- CONFIGURACIÓN ---
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(texto):
        if not texto: return ""
        return "".join(re.findall(r'[a-zA-Z0-9]+', texto)).lower()

    lista_resultados = ft.ListView(expand=True, spacing=15)

    def filtrar_por_categoria(e):
        txt_busqueda.value = e.control.label
        actualizar_lista(None)
        page.update()

    def actualizar_lista(e):
        lista_resultados.controls.clear()
        val_original = txt_busqueda.value.strip().lower()
        val_limpio = normalizar(val_original)
        
        if val_original:
            encontrado = False
            for linea in datos_escuelas:
                partes = linea.split("-", 3)
                if len(partes) >= 4:
                    n, l, d, t = [p.strip() for p in partes]
                    
                    if (val_original in n.lower() or 
                        val_original in d.lower() or 
                        val_original in l.lower() or
                        val_limpio in normalizar(n)):
                        
                        encontrado = True
                        tel_f = "".join(filter(str.isdigit, t))
                        url_mapa = f"https://www.google.com/maps/search/{n.replace(' ', '+')}+{l.replace(' ', '+')}+Coronel+Dorrego"
                        texto_ws = f"*{n}*\nLocalidad: {l}\nDirector: {d}\nTel: {t}"
                        url_ws = f"https://wa.me/?text={texto_ws.replace(' ', '%20')}"

                        lista_resultados.controls.append(
                            ft.Container(
                                padding=20, 
                                border_radius=15, 
                                bgcolor="grey100",
                                border=ft.border.all(1, "grey400"),
                                content=ft.Column([
                                    ft.Text(n, size=18, weight="bold", color="blue700"),
                                    ft.Text(f"📍 {l}", size=15, color="black"),
                                    ft.Text(f"👤 Dir: {d}", size=14, italic=True, color="black"),
                                    ft.Row([
                                        ft.IconButton(icon="share", icon_color="blue", url=url_ws),
                                        ft.FilledButton("Llamar", icon="phone", url=f"tel:{tel_f}", bgcolor="green700"),
                                        ft.FilledButton("Mapa", icon="map", url=url_mapa, bgcolor="red700"),
                                    ], alignment=ft.MainAxisAlignment.END)
                                ])
                            )
                        )
            if not encontrado:
                lista_resultados.controls.append(ft.Text("No se encontraron escuelas.", color="red"))
        page.update()

    txt_busqueda = ft.TextField(
        label="Buscar escuela o director...", 
        on_change=actualizar_lista, 
        prefix_icon="search", # Cambiado a texto simple
        border_radius=15,
        filled=True
    )

    chips_categorias = ft.Row([
        ft.Chip(label="EP", on_click=filtrar_por_categoria, bgcolor="blue50"),
        ft.Chip(label="JI", on_click=filtrar_por_categoria, bgcolor="green50"),
        ft.Chip(label="EES", on_click=filtrar_por_categoria, bgcolor="orange50"),
        ft.Chip(label="CEC", on_click=filtrar_por_categoria, bgcolor="purple50"),
    ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

    vista_busqueda = ft.Column([
        ft.Text("Directorio Escolar", size=26, weight="bold", color="blue"),
        ft.Text("Consejo Escolar - Coronel Dorrego", size=13),
        ft.Divider(height=10),
        txt_busqueda,
        chips_categorias,
        lista_resultados
    ], scroll=ft.ScrollMode.AUTO)

    def verificar_clave(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(ft.SafeArea(ft.Container(content=vista_busqueda, padding=10)))
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            txt_clave.update()

    txt_clave = ft.TextField(label="Clave de Acceso", password=True, width=280, text_align="center", on_submit=verificar_clave)
    
    page.add(
        ft.Container(
            expand=True,
            content=ft.Column([
                ft.Icon(name="lock_person", size=80, color="blue"), # Cambiado a texto simple
                ft.Text("Acceso Restringido", size=22, weight="bold"),
                txt_clave,
                ft.FilledButton("Entrar", on_click=verificar_clave, width=200)
            ], horizontal_alignment="center", alignment="center")
        )
    )

if __name__ == "__main__":
    ft.app(target=main, port=int(os.getenv("PORT", 8080)))
