import flet as ft
import os
import re  # <--- IMPORTANTE: Agregamos esto para la limpieza profunda

def main(page: ft.Page):
    page.title = "Directorio Escolar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    
    page.meta_data = {
        "viewport": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
    }

    # --- CONFIGURACIÓN ---
    CLAVE_ACCESO = "dorrego2026"
    archivo = "lista.txt"
    datos_escuelas = []
    
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
            datos_escuelas = [linea.strip() for linea in f if linea.strip()]

    # --- FUNCIÓN DE LIMPIEZA TOTAL ---
    def normalizar(texto):
        """Deja solo letras y números. Convierte 'J.I. Nº2' en 'jin2'"""
        if not texto:
            return ""
        # Busca solo caracteres alfanuméricos y los une en minúsculas
        return "".join(re.findall(r'[a-zA-Z0-9]+', texto)).lower()

    # --- ELEMENTOS DE LA INTERFAZ ---
    lista_resultados = ft.ListView(expand=True, spacing=15)
    
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
                    
                    # COMPARACIÓN
                    # 1. ¿Está el texto en el nombre, director o localidad?
                    # 2. ¿Coincide la versión limpia (sin puntos, espacios ni º)?
                    if (val_original in n.lower() or 
                        val_original in d.lower() or 
                        val_original in l.lower() or
                        val_limpio in normalizar(n)):
                        
                        encontrado = True
                        tel_f = "".join(filter(str.isdigit, t)).replace("15", "", 1)
                        
                        # URL de Mapa con búsqueda directa
                        url_mapa = f"https://www.google.com/maps/search/{n.replace(' ', '+')}+{l.replace(' ', '+')}+Coronel+Dorrego"

                        lista_resultados.controls.append(
                            ft.Container(
                                padding=20, border_radius=15, bgcolor="white",
                                border=ft.Border.all(1, ft.Colors.BLUE_100),
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
                                content=ft.Column([
                                    ft.Text(n, size=20, weight="bold", color="blue900"),
                                    ft.Text(f"📍 {l}", size=16),
                                    ft.Text(f"👤 Dir: {d}", size=14, italic=True),
                                    ft.Row([
                                        ft.FilledButton(
                                            "Llamar", icon=ft.Icons.PHONE, url=f"tel:{tel_f}", 
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700, color="white")
                                        ),
                                        ft.FilledButton(
                                            "Mapa", icon=ft.Icons.MAP, url=url_mapa, 
                                            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color="white")
                                        ),
                                    ], alignment=ft.MainAxisAlignment.END, spacing=10)
                                ])
                            )
                        )
            if not encontrado:
                lista_resultados.controls.append(ft.Text("Sin resultados", color="red", italic=True))
        page.update()

    txt_busqueda = ft.TextField(
        label="¿Qué escuela buscás?", 
        on_change=actualizar_lista, 
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        hint_text="Ej: epn1, jin2, eesn1..."
    )

    vista_busqueda = ft.Container(
        content=ft.Column([
            ft.Text("Directorio Escolar", size=28, weight="bold", color="blue900"),
            ft.Text("Consejo Escolar - Coronel Dorrego", size=14),
            ft.Divider(height=10, color="transparent"),
            txt_busqueda,
            lista_resultados
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15
    )

    def verificar_clave(e):
        if txt_clave.value == CLAVE_ACCESO:
            page.controls.clear()
            page.add(vista_busqueda)
            page.update()
        else:
            txt_clave.error_text = "Clave incorrecta"
            page.update()

    txt_clave = ft.TextField(
        label="Clave de Acceso", password=True, can_reveal_password=True, 
        on_submit=verificar_clave, width=300
    )
    
    vista_login = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.LOCK_PERSON, size=80, color="blue900"),
            ft.Text("Acceso Restringido", size=24, weight="bold"),
            txt_clave,
            ft.FilledButton(
                "Entrar", on_click=verificar_clave, 
                style=ft.ButtonStyle(bgcolor="blue900", color="white"), width=200
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=50,
        alignment=ft.Alignment(0, 0)
    )

    page.add(vista_login)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.run(main, host="0.0.0.0", port=port, view=ft.AppView.WEB_BROWSER)
