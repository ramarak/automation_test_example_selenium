from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class RegistroPage(BasePage):
    NOMBRE = (By.ID, "nombre")
    EMAIL = (By.ID, "email")
    CONTRASENA = (By.ID, "contrasena")
    CONFIRMAR = (By.ID, "confirmar")
    BTN_REGISTRAR = (By.ID, "btn-registrar")
    MENSAJE_ERROR = (By.ID, "mensaje-error")
    MENSAJE_EXITO = (By.ID, "mensaje-exito")

    def abrir(self, base_url):
        self.abrir_url(f"{base_url}/registro.html")
        self.esperar_elemento(self.NOMBRE)

    def registrar(self, nombre, email, contrasena, confirmar=None):
        if confirmar is None:
            confirmar = contrasena
        self.escribir_texto(self.NOMBRE, nombre)
        self.escribir_texto(self.EMAIL, email)
        self.escribir_texto(self.CONTRASENA, contrasena)
        self.escribir_texto(self.CONFIRMAR, confirmar)
        self.hacer_clic(self.BTN_REGISTRAR)

    def enviar_formulario_vacio(self):
        self.hacer_clic(self.BTN_REGISTRAR)

    def mensaje_error(self):
        return self.texto_visible(self.MENSAJE_ERROR)

    def mensaje_exito(self):
        return self.texto_visible(self.MENSAJE_EXITO)

    def nombre_requerido_vacio(self):
        return self.valor_faltante("nombre")
