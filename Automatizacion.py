from playwright.sync_api import sync_playwright
import time

def test_formulario_contacto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        try:
            # 1. Ir a la página 
            page.goto("https://www.ucp.edu.ar/ingreso2025/", timeout=15000)

            # 2. Seleccionar carrera 
            page.wait_for_selector("select", timeout=10000)
            page.select_option("select", index=9)  # Ingeniería en Sistemas de Información

            # 3. Seleccionar sede 
            page.wait_for_selector("text=Posadas", timeout=10000)
            page.click("text=Posadas")

            # 4. Completar formulario 
            time.sleep(1) 
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.fill("input[placeholder='Nombre y Apellido']", "Juan Pérez")
            page.fill("input[placeholder='Correo electrónico']", "juanperez@example.com")
            page.fill("input[placeholder='Telefono']", "123456789")
            time.sleep(2)
            
            # 5. Hacer clic en el botón CONTINUAR 
            continue_button = page.locator("input.form_button[value='CONTINUAR']")
            continue_button.scroll_into_view_if_needed()
            continue_button.click()
            
            # 6. Esperar que aparezca la sección de método de contacto
            page.wait_for_selector(".contenedorEnvio", state="visible", timeout=5000)
            time.sleep(2)

            # 7. Seleccionar método de contacto 
            page.click("#selectCorreo")
            time.sleep(0.5)
            time.sleep(1)

            # 8. Hacer clic en el botón CONFIRMAR 
            confirm_button = page.locator("#submit")
            confirm_button.scroll_into_view_if_needed()
            confirm_button.click()
            
            # 9. Esperar confirmación final
            page.wait_for_selector("div.form_message b", timeout=5000)
            print("✅ Formulario completado y enviado correctamente!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            page.screenshot(path="error.png")
            print("📸 Se guardó captura de error como 'error.png'")
            
        finally:
            time.sleep(3) 
            browser.close()

if __name__ == "__main__":
    test_formulario_contacto()