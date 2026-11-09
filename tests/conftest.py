import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from pytest_html import extras

from tests.navegador import NAVEGADORES_VALIDOS, crear_driver
from tests.pages.base_page import BasePage

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"
EVIDENCIAS = ROOT / "evidencias"
REPORTES = ROOT / "reportes"


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="brave",
        help="Navegador a usar: brave (predeterminado), firefox o edge",
    )


def pytest_configure(config):
    elegido = config.getoption("--browser").strip().lower()
    if elegido not in NAVEGADORES_VALIDOS:
        permitidos = ", ".join(NAVEGADORES_VALIDOS)
        raise pytest.UsageError(
            f"--browser={elegido} no es válido. Use uno de: {permitidos}"
        )


@pytest.fixture(scope="session")
def nombre_navegador(pytestconfig):
    return pytestconfig.getoption("--browser").strip().lower()


@pytest.fixture(scope="session")
def servidor():
    EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    REPORTES.mkdir(parents=True, exist_ok=True)
    handler = partial(SimpleHTTPRequestHandler, directory=str(APP_DIR))
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    hilo = threading.Thread(target=httpd.serve_forever, daemon=True)
    hilo.start()
    host, puerto = httpd.server_address
    yield f"http://{host}:{puerto}"
    httpd.shutdown()
    httpd.server_close()


@pytest.fixture
def driver(nombre_navegador):
    navegador = crear_driver(nombre_navegador)
    navegador.maximize_window()
    yield navegador
    navegador.quit()


@pytest.fixture
def captura(driver):
    pagina = BasePage(driver)

    def _captura(nombre):
        return pagina.tomar_captura(nombre)

    return _captura


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()
    setattr(item, f"reporte_{reporte.when}", reporte)

    adjuntos = getattr(reporte, "extras", [])
    if reporte.when == "call" and reporte.failed:
        navegador = item.funcargs.get("driver")
        if navegador:
            EVIDENCIAS.mkdir(parents=True, exist_ok=True)
            nombre = f"{item.name}_ERROR.png"
            ruta = EVIDENCIAS / nombre
            png = navegador.get_screenshot_as_png()
            ruta.write_bytes(png)
            adjuntos.append(extras.image(png, mime_type="image/png"))
    reporte.extras = adjuntos
