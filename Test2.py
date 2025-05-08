from playwright.sync_api import sync_playwright
import time

def test_validacion_telefono_corto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # Configuración inicial automática
            page.goto("https://www.ucp.edu.ar/ingreso2025/", timeout=15000)
            page.select_option("select", index=9)  # Carrera (Ing. Sistemas)
            page.click("text=Posadas")  # Sede
            continuar_btn = page.locator("input.form_button[value='CONTINUAR']")
            time.sleep(1)

            # Locators
            nombre = page.locator("input[placeholder='Nombre y Apellido']")
            email = page.locator("input[placeholder='Correo electrónico']")
            telefono = page.locator("input[placeholder='Telefono']")

            print("\n🔍 PROGRAMA 2: Validación de teléfono corto")
            print("--------------------------------------------------")

            # --- TEST: Teléfono con menos de 10 dígitos ---
            print("\n⚠️ Caso: Teléfono corto (nombre y email válidos)")
            nombre.fill("Carlos Méndez")
            email.fill("carlos@example.com")
            telefono.fill("123")  # Menos de 10 dígitos
            
            telefono_color = telefono.evaluate("el => window.getComputedStyle(el).backgroundColor")
            if "rgb(255, 152, 179)" in telefono_color.lower():
                print("✅ Correcto: Sistema detectó teléfono inválido")
            else:
                print("❌ Error: Teléfono corto fue aceptado")
            time.sleep(1.5)
            continuar_btn.click()

            # --- Caso de éxito para comparación ---
            print("\n⚠️ Caso de control: Datos completamente válidos")
            telefono.fill("1234567890")
            continuar_btn.click()
            input("👉 PRESIONA ENTER para hacer clic MANUAL en 'CONTINUAR'...")
            
            if page.locator(".contenedorEnvio").is_visible(timeout=3000):
                print("✅ Correcto: Formulario avanzó con datos válidos")
            else:
                print("❌ Error: No avanzó con datos correctos")
            time.sleep(1.5)

        except Exception as e:
            print(f"\n⚠️ Error inesperado: {str(e)}")
            page.screenshot(path="error_telefono.png")
        finally:
            input("\nPresiona ENTER para cerrar el navegador...")
            browser.close()

if __name__ == "__main__":
    test_validacion_telefono_corto()