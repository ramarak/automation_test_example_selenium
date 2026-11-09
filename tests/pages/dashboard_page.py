from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    BIENVENIDA = (By.ID, "bienvenida")
    BTN_CERRAR_SESION = (By.ID, "btn-cerrar-sesion")

    def esperar_carga(self):
        self.esperar_elemento(self.BIENVENIDA)
        return self

    def bienvenida(self):
        return self.texto_visible(self.BIENVENIDA)

    def cerrar_sesion(self):
        self.hacer_clic(self.BTN_CERRAR_SESION)
        self.wait.until(EC.url_contains("index.html"))
