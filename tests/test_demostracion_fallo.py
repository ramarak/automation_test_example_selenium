import pytest

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage


@pytest.mark.demo_fallo
def test_CT99_demostracion_fallo_intencional(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    login.iniciar_sesion("admin", "123456")
    dashboard = DashboardPage(driver).esperar_carga()
    captura("test_CT99_demostracion_fallo_intencional_paso1")
    assert "Bienvenido, usuario_inexistente" in dashboard.bienvenida()
