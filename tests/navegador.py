import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

NAVEGADORES_VALIDOS = ("brave", "firefox", "edge")


def _primera_ruta_existente(rutas):
    for ruta in rutas:
        if ruta and Path(ruta).is_file():
            return str(Path(ruta))
    return None


def _desde_path(comandos):
    for comando in comandos:
        encontrado = shutil.which(comando)
        if encontrado:
            return encontrado
    return None


def _ruta_brave():
    return _primera_ruta_existente(
        [
            os.environ.get("BRAVE_BIN"),
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expandvars(
                r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            "/usr/bin/brave-browser",
            "/usr/bin/brave",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            _desde_path(["brave", "brave-browser", "brave-browser-stable"]),
        ]
    )


def _ruta_firefox():
    return _primera_ruta_existente(
        [
            os.environ.get("FIREFOX_BIN"),
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            "/usr/bin/firefox",
            "/Applications/Firefox.app/Contents/MacOS/firefox",
            _desde_path(["firefox"]),
        ]
    )


def _ruta_edge():
    return _primera_ruta_existente(
        [
            os.environ.get("EDGE_BIN"),
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
            "/usr/bin/microsoft-edge",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            _desde_path(["msedge", "microsoft-edge"]),
        ]
    )


def _opciones_chromium(opciones, binario):
    opciones.binary_location = binario
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--no-first-run")
    opciones.add_argument("--no-default-browser-check")
    opciones.add_argument("--disable-extensions")
    opciones.add_argument("--start-maximized")
    return opciones


def crear_driver(nombre="brave"):
    nombre = (nombre or "brave").strip().lower()
    if nombre not in NAVEGADORES_VALIDOS:
        permitidos = ", ".join(NAVEGADORES_VALIDOS)
        raise ValueError(f"Navegador no soportado: {nombre}. Use: {permitidos}")

    if nombre == "brave":
        binario = _ruta_brave()
        if not binario:
            raise FileNotFoundError(
                "No se encontró Brave. Instálelo o defina BRAVE_BIN con la ruta a brave.exe."
            )
        opciones = _opciones_chromium(ChromeOptions(), binario)
        servicio = ChromeService(
            ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
        )
        return webdriver.Chrome(service=servicio, options=opciones)

    if nombre == "firefox":
        binario = _ruta_firefox()
        if not binario:
            raise FileNotFoundError(
                "No se encontró Firefox. Instálelo o defina FIREFOX_BIN con la ruta a firefox.exe."
            )
        opciones = FirefoxOptions()
        opciones.binary_location = binario
        servicio = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=servicio, options=opciones)

    binario = _ruta_edge()
    if not binario:
        raise FileNotFoundError(
            "No se encontró Microsoft Edge. Instálelo o defina EDGE_BIN con la ruta a msedge.exe."
        )
    opciones = _opciones_chromium(EdgeOptions(), binario)
    servicio = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=servicio, options=opciones)
