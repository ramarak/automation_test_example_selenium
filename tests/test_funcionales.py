from time import time

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage
from tests.pages.registro_page import RegistroPage


def test_CT01_login_credenciales_validas(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    captura("test_CT01_login_credenciales_validas_paso1")

    login.iniciar_sesion("admin", "123456")
    dashboard = DashboardPage(driver).esperar_carga()
    captura("test_CT01_login_credenciales_validas_paso2")

    assert "dashboard.html" in dashboard.url_actual()
    assert "Bienvenido, admin" in dashboard.bienvenida()


def test_CT02_login_contrasena_incorrecta(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    captura("test_CT02_login_contrasena_incorrecta_paso1")

    login.iniciar_sesion("admin", "clave_errada")
    captura("test_CT02_login_contrasena_incorrecta_paso2")

    assert "Credenciales inválidas" in login.mensaje_error()
    assert "dashboard.html" not in login.url_actual()


def test_CT03_login_campos_vacios(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    captura("test_CT03_login_campos_vacios_paso1")

    login.enviar_formulario_vacio()
    captura("test_CT03_login_campos_vacios_paso2")

    assert "dashboard.html" not in login.url_actual()
    assert login.usuario_requerido_vacio() or login.contrasena_requerida_vacia()


def test_CT04_registro_usuario_nuevo(driver, servidor, captura):
    registro = RegistroPage(driver)
    registro.abrir(servidor)
    captura("test_CT04_registro_usuario_nuevo_paso1")

    email = f"nuevo.usuario.{int(time())}@demo.com"
    registro.registrar("Ana Perez", email, "clave123")
    captura("test_CT04_registro_usuario_nuevo_paso2")

    assert "Registro exitoso" in registro.mensaje_exito()


def test_CT05_registro_email_duplicado(driver, servidor, captura):
    registro = RegistroPage(driver)
    registro.abrir(servidor)
    captura("test_CT05_registro_email_duplicado_paso1")

    registro.registrar("Admin Clone", "admin@demo.com", "clave123")
    captura("test_CT05_registro_email_duplicado_paso2")

    assert "email ya existe" in registro.mensaje_error()


def test_CT06_registro_campos_vacios(driver, servidor, captura):
    registro = RegistroPage(driver)
    registro.abrir(servidor)
    captura("test_CT06_registro_campos_vacios_paso1")

    registro.enviar_formulario_vacio()
    captura("test_CT06_registro_campos_vacios_paso2")

    assert registro.mensaje_exito() == ""
    assert registro.nombre_requerido_vacio()


def test_CT07_cerrar_sesion(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    login.iniciar_sesion("admin", "123456")

    dashboard = DashboardPage(driver).esperar_carga()
    captura("test_CT07_cerrar_sesion_paso1")

    dashboard.cerrar_sesion()
    captura("test_CT07_cerrar_sesion_paso2")

    assert "index.html" in login.url_actual()
    LoginPage(driver).esperar_elemento(LoginPage.USUARIO)
