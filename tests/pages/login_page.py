from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USUARIO = (By.ID, "usuario")
    CONTRASENA = (By.ID, "contrasena")
    BTN_INGRESAR = (By.ID, "btn-ingresar")
    MENSAJE_ERROR = (By.ID, "mensaje-error")

    def abrir(self, base_url):
        self.abrir_url(f"{base_url}/index.html")
        self.esperar_elemento(self.USUARIO)

    def iniciar_sesion(self, usuario, contrasena):
        self.escribir_texto(self.USUARIO, usuario)
        self.escribir_texto(self.CONTRASENA, contrasena)
        self.hacer_clic(self.BTN_INGRESAR)

    def enviar_formulario_vacio(self):
        self.hacer_clic(self.BTN_INGRESAR)

    def mensaje_error(self):
        return self.texto_visible(self.MENSAJE_ERROR)

    def usuario_requerido_vacio(self):
        return self.valor_faltante("usuario")

    def contrasena_requerida_vacia(self):
        return self.valor_faltante("contrasena")
