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
    
    # Carga de datos
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    def normalizar(texto):
        """Limpia el texto para búsquedas (ej: J.I. N2 -> jin2)"""
        if not texto: return ""
        return "".join(re.findall(r'[a-zA-Z0-9]+', texto)).lower()

    # --- ELEMENTOS DE LA INTERFAZ ---
    lista_resultados = ft.ListView(expand=True, spacing=15)

    def cambiar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        btn_tema.icon = ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        page.update()

    def filtrar_por_categoria(e):
        """Al tocar un Chip, se escribe en el buscador y se filtra"""
        txt_busqueda.value = e.control.label.value
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
                        texto_ws = f"📍 *{n}*\nLocalidad: {l}\nDirector: {d}\nTel: {t}"
                        url_ws = f"https://wa.me/?text={texto_ws.replace(' ', '%20')}"

                        lista_resultados.controls.append(
                            ft.Container(
                                padding=20, border_radius=15, 
                                bgcolor=ft.Colors.SURFACE_VARIANT,
                                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                                content=ft.Column([
                                    ft.Text(n, size=18, weight="bold", color=ft.Colors.PRIMARY),
                                    ft.Text(f"📍 {l}", size=15),
                                    ft.Text(f"👤 Dir: {d}", size=14, italic=True),
                                    ft.Row([
                                        ft.IconButton(ft.Icons.SHARE, icon_color=ft.Colors.BLUE_400, url=url_ws, tooltip="Compartir"),
                                        ft.FilledButton("Llamar", icon=ft.Icons.PHONE, url=f"tel:{tel_f}", bgcolor=ft.Colors.GREEN_700),
                                        ft.FilledButton("Mapa", icon=ft.Icons.MAP, url=url_mapa, bgcolor=ft.Colors.RED_700),
                                    ], alignment=ft.MainAxisAlignment.END, spacing=5)
                                ])
                            )
                        )
            if not encontrado:
                lista_resultados.controls.append(ft.Text("No se encontraron escuelas.", color="red", italic=True))
        page.update()

    btn_tema = ft.IconButton(ft.Icons.DARK_MODE, on_click=cambiar_tema)
    
    txt_busqueda = ft.TextField(
        label="Buscar escuela o director...", 
        on_change=actualizar_lista, 
        prefix_icon=ft.Icons.SEARCH,
        border_radius=15,
        filled=True,
        hint_text="Ej: ep1, jin2, ees1..."
    )

    chips_categorias = ft.Row([
        ft.ActionChip(label=ft.Text("EP"), on_click=filtrar_por_categoria),
        ft.ActionChip(label=ft.Text("JI"), on_click=filtrar_por_categoria),
        ft.ActionChip(label=ft.Text("EES"), on_click=filtrar_por_categoria),
        ft.ActionChip(label=ft.Text("CEC"), on_click=filtrar_por_categoria),
    ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

    vista_busqueda = ft.Column([
        ft.Row([
            ft.Column([
                ft.Text("Directorio Escolar", size=26, weight="bold", color=ft.Colors.PRIMARY),
                ft.Text("Consejo Escolar - Coronel Dorrego", size=13),
            ], expand=True),
            btn_tema
        ]),
        ft.Divider(height=10, color="transparent"),
        txt_busqueda,
        chips_categorias,
        lista_resultados
    ], scroll=ft.ScrollMode.AUTO)

    def verificar_clave(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(ft.SafeArea(ft.Container(content=vista_busqueda, padding=15)))
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            txt_clave.value = ""
            page.update()

    txt_clave = ft.TextField(
        label="Clave de Acceso", 
        password=True, 
        can_reveal_password=True, 
        on_submit=verificar_clave, 
        width=280,
        text_align=ft.TextAlign.CENTER
    )
    
    vista_login = ft.Container(
        expand=True,
        content=ft.Column([
            ft.Icon(ft.Icons.LOCK_PERSON, size=80, color=ft.Colors.PRIMARY),
            ft.Text("Acceso Restringido", size=22, weight="bold"),
            txt_clave,
            ft.FilledButton("Entrar", on_click=verificar_clave, width=200, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
    )

    page.add(vista_login)

# --- ESTO ES LO QUE CAMBIAMOS PARA RENDER ---
if __name__ == "__main__":
    # Usamos ft.app en lugar de ft.run para la web
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=int(os.getenv("PORT", 8080))
    )
