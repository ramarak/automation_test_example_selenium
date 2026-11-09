from pathlib import Path

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[2]
EVIDENCIAS = ROOT / "evidencias"
TIMEOUT = 10


class BasePage:
    def __init__(self, driver, timeout=TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir_url(self, url):
        self.driver.get(url)

    def esperar_elemento(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def escribir_texto(self, locator, texto):
        elemento = self.esperar_elemento(locator)
        elemento.clear()
        elemento.send_keys(texto)
        return elemento

    def hacer_clic(self, locator):
        elemento = self.wait.until(EC.element_to_be_clickable(locator))
        elemento.click()
        return elemento

    def texto_visible(self, locator):
        return self.esperar_elemento(locator).text

    def url_actual(self):
        return self.driver.current_url

    def tomar_captura(self, nombre):
        EVIDENCIAS.mkdir(parents=True, exist_ok=True)
        if not nombre.endswith(".png"):
            nombre = f"{nombre}.png"
        ruta = EVIDENCIAS / nombre
        self.driver.save_screenshot(str(ruta))
        return str(ruta)

    def valor_faltante(self, element_id):
        return self.driver.execute_script(
            "return document.getElementById(arguments[0]).validity.valueMissing;",
            element_id,
        )
