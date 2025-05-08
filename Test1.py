from playwright.sync_api import sync_playwright
import time

def test_validacion_email_espacios():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # Configuración inicial automática
            page.goto("https://www.ucp.edu.ar/ingreso2025/", timeout=15000)
            page.select_option("select", index=9)  # Carrera (Ing. Sistemas)
            page.click("text=Posadas")  # Sede
            time.sleep(1)

            # Locators
            nombre = page.locator("input[placeholder='Nombre y Apellido']")
            email = page.locator("input[placeholder='Correo electrónico']")
            telefono = page.locator("input[placeholder='Telefono']")
            continuar_btn = page.locator("input.form_button[value='CONTINUAR']")

            print("\n🔍 PROGRAMA 1: Validación de email y campos vacíos")
            print("--------------------------------------------------")

            # --- TEST 1: Espacio vacío ---
            print("\n🔍 Test 1: Validación de campos vacíos")
            continuar_btn.click()
            
            # Verificar estilos de error (cambian a fondo rojo según el JS)
            nombre_color = nombre.evaluate("el => window.getComputedStyle(el).backgroundColor")
            email_color = email.evaluate("el => window.getComputedStyle(el).backgroundColor")
            telefono_color = telefono.evaluate("el => window.getComputedStyle(el).backgroundColor")
            
            assert "rgb(255, 152, 179)" in nombre_color.lower(), "❌ Falló validación nombre vacío"
            assert "rgb(255, 152, 179)" in email_color.lower(), "❌ Falló validación email vacío"
            assert "rgb(255, 152, 179)" in telefono_color.lower(), "❌ Falló validación teléfono vacío"
            print("✅ Campos vacíos detectados correctamente")
            time.sleep(1.5)

            # --- TEST 2: Email inválido ---
            print("\n⚠️ Caso 2: Email mal formado (nombre y teléfono VÁLIDOS)")
            nombre.fill("María González")  # Nombre genérico válido
            email.fill("esto-no-es-un-email")  # Email inválido
            telefono.fill("1122334455")  # Teléfono genérico válido (10 dígitos)
            
            input("👉 PRESIONA ENTER para hacer clic MANUAL en 'CONTINUAR' y verificar validación...")
            
            # Verificación específica del email
            email_color = email.evaluate("el => window.getComputedStyle(el).backgroundColor")
            nombre_color = nombre.evaluate("el => window.getComputedStyle(el).backgroundColor")  # Para asegurar que no hay error en nombre
            telefono_color = telefono.evaluate("el => window.getComputedStyle(el).backgroundColor")  # Para asegurar que no hay error en teléfono

            if "rgb(255, 152, 179)" in email_color.lower():
                print("✅ Correcto: Solo el email inválido muestra error (fondo rojo)")
                # Verificar que los otros campos NO tienen error
                if "rgb(255, 152, 179)" not in nombre_color.lower() and "rgb(255, 152, 179)" not in telefono_color.lower():
                    print("✅ Nombre y teléfono se mantienen válidos")
                else:
                    print("⚠️ Advertencia: Campos válidos aparecen como erróneos")
            else:
                print("❌ Error: El sistema aceptó un email inválido")
            time.sleep(1.5)
            continuar_btn.click()

        except Exception as e:
            print(f"\n⚠️ Error inesperado: {str(e)}")
            page.screenshot(path="error_email.png")
        finally:
            input("\nPresiona ENTER para cerrar el navegador...")
            browser.close()

if __name__ == "__main__":
    test_validacion_email_espacios()