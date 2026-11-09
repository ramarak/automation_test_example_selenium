"""Genera Taller_Automatizacion_[NombreGrupo].docx (sin portada)."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import OxmlElement

SALIDA = Path(__file__).resolve().parent / "Taller_Automatizacion_[NombreGrupo].docx"


def set_run_font(run, name="Calibri", size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def shade_cell(cell, hex_color):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc
    tc_pr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tc_pr.append(shd)


def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    return p


def add_para(doc, text, size=11, bold=False, italic=False, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_code(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.rows[0].cells[0]
    shade_cell(cell, "F1F5F9")
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text.strip("\n"))
    set_run_font(run, name="Consolas", size=8, color=RGBColor(0x1E, 0x29, 0x3B))
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def add_placeholder(doc, figura, descripcion, archivo):
    table = doc.add_table(rows=1, cols=1)
    cell = table.rows[0].cells[0]
    shade_cell(cell, "FEF3C7")
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        f"[AQUÍ VA LA CAPTURA]\n{figura}. {descripcion}\nPegar: {archivo}"
    )
    set_run_font(run, size=9, italic=True, color=RGBColor(0x92, 0x40, 0x0E))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run(f"{figura}. {descripcion}")
    set_run_font(r, size=9, italic=True)


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        shade_cell(cell, "1E293B")
        p = cell.paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=9, bold=True, color=RGBColor(255, 255, 255))
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            p = table.rows[r_i + 1].cells[c_i].paragraphs[0]
            run = p.add_run(val)
            set_run_font(run, size=9)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.5)
    section.bottom_margin = Cm(1.5)

    # Sin portada: el informe inicia en el contenido.
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = t.add_run(
        "Taller de automatización de pruebas funcionales — Actividad 2, Unidad 2"
    )
    set_run_font(r, size=14, bold=True, color=RGBColor(0x0F, 0x17, 0x2A))
    add_para(
        doc,
        "Asignatura: Pruebas y Calidad del Software. Entregable: "
        "Taller_Automatizacion_[NombreGrupo].pdf (máximo 15 páginas, sin portada). "
        "Sustituya [NombreGrupo] y complete integrantes, reflexión y las capturas indicadas.",
        size=10,
        italic=True,
    )

    add_heading(doc, "1. Presentación del grupo", 1)
    add_para(
        doc,
        "Objetivo del taller: diseñar una aplicación web mínima (login, registro y dashboard) "
        "y automatizar pruebas funcionales con Selenium WebDriver, pytest y Page Object Model, "
        "generando evidencias (capturas y reporte HTML) para demostrar que la suite pasa y que "
        "un fallo produce captura automática.",
    )
    add_para(doc, "Integrantes y roles (completar):", bold=True)
    add_table(
        doc,
        ["Nombre", "Rol en el taller", "Aporte principal"],
        [
            ["[Completar]", "App HTML/CSS/JS", "Pantallas y validaciones de negocio"],
            ["[Completar]", "Automatización / POM", "Page Objects, fixtures y casos CT01–CT07"],
            ["[Completar]", "Evidencias y redacción", "Capturas, reporte HTML y este informe"],
        ],
    )

    add_heading(doc, "2. Descripción de la aplicación bajo prueba", 1)
    add_para(
        doc,
        "La aplicación es estática (HTML, CSS y JavaScript) y se sirve en local con "
        "http.server. No hay backend: el login válido, el email duplicado y la sesión "
        "se simulan en el navegador (sessionStorage / localStorage).",
    )
    add_para(doc, "Módulos y reglas", bold=True)
    add_table(
        doc,
        ["Pantalla", "Archivo", "Comportamiento"],
        [
            [
                "Login",
                "app/index.html",
                "Usuario y contraseña; Ingresar. Válido: admin / 123456 → dashboard. "
                "Error: «Credenciales inválidas». Campos required (HTML5).",
            ],
            [
                "Registro",
                "app/registro.html",
                "Nombre, email, contraseña y confirmar. Vacío: required. "
                "Email admin@demo.com → «email ya existe». Éxito: «Registro exitoso».",
            ],
            [
                "Dashboard",
                "app/dashboard.html",
                "«Bienvenido, admin» si hay sesión. Cerrar sesión limpia sesión y vuelve al login. "
                "Sin sesión redirige a index.html.",
            ],
        ],
    )
    add_para(
        doc,
        "Extracto de la lógica de login y del email duplicado en app/app.js. Las credenciales "
        "y el email semilla están fijos para que los casos de prueba sean reproducibles.",
    )
    add_code(
        doc,
        """
const EMAIL_DUPLICADO = "admin@demo.com";
const USUARIO_VALIDO = "admin";
const CLAVE_VALIDA = "123456";

if (usuario === USUARIO_VALIDO && clave === CLAVE_VALIDA) {
  sessionStorage.setItem(STORAGE_SESION, JSON.stringify({ nombre: USUARIO_VALIDO }));
  window.location.href = "dashboard.html";
  return;
}
error.textContent = "Credenciales inválidas";

if (emailExiste(email.value.trim())) {
  error.textContent = "email ya existe";
  return;
}
exito.textContent = "Registro exitoso";
""",
    )
    add_placeholder(
        doc,
        "Figura 1",
        "Pantalla de login (index.html) con campos usuario, contraseña y botón Ingresar",
        "captura manual de la app o evidencias/test_CT01_login_credenciales_validas_paso1.png",
    )
    add_placeholder(
        doc,
        "Figura 2",
        "Pantalla de registro (registro.html)",
        "evidencias/test_CT04_registro_usuario_nuevo_paso1.png",
    )
    add_placeholder(
        doc,
        "Figura 3",
        "Dashboard con mensaje de bienvenida y botón Cerrar sesión",
        "evidencias/test_CT01_login_credenciales_validas_paso2.png",
    )

    add_heading(doc, "3. Guía paso a paso del trabajo grupal", 1)
    add_para(
        doc,
        "El trabajo se organizó en tres frentes paralelos: (1) aplicación web de demostración, "
        "(2) suite Selenium con POM y (3) evidencias + informe. El servidor HTTP lo arranca "
        "pytest, de modo que un compañero puede clonar, instalar y ejecutar en un solo comando.",
    )
    add_para(doc, "3.1 Requisitos e instalación", bold=True)
    add_para(
        doc,
        "Python 3.10+, pip y un navegador: Brave (predeterminado), Firefox o Edge. "
        "webdriver-manager descarga el driver en la primera ejecución.",
    )
    add_code(
        doc,
        """
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
""",
    )
    add_para(doc, "3.2 Ejecución de la app (opcional, para inspección manual)", bold=True)
    add_code(
        doc,
        """
cd app
python -m http.server 8000
# Abrir http://127.0.0.1:8000/index.html
""",
    )
    add_para(doc, "3.3 Ejecución de la suite (CT01–CT07 en verde)", bold=True)
    add_code(
        doc,
        """
pytest tests/ --html=reportes/reporte.html --self-contained-html
pytest tests/ --browser=firefox --html=reportes/reporte.html --self-contained-html
pytest tests/ --browser=edge --html=reportes/reporte.html --self-contained-html
""",
    )
    add_para(doc, "3.4 Demostración de fallo y captura automática", bold=True)
    add_code(
        doc,
        """
pytest tests/test_demostracion_fallo.py -m demo_fallo --html=reportes/reporte_fallo.html --self-contained-html
""",
    )
    add_para(
        doc,
        "En esta máquina se ejecutó la suite en Brave (7 passed) y Firefox (7 passed). "
        "Edge Chromium no estaba instalado; el código ya contempla --browser=edge cuando exista msedge.exe. "
        "Las capturas de paso quedaron en evidencias/ y el reporte en reportes/reporte.html.",
    )
    add_placeholder(
        doc,
        "Figura 4",
        "Terminal con pytest: 7 passed (suite verde en Brave o Firefox)",
        "captura de PowerShell tras ejecutar pytest tests/",
    )

    add_heading(doc, "4. Documentación técnica", 1)
    add_para(doc, "4.1 Stack", bold=True)
    add_para(
        doc,
        "Python 3, Selenium WebDriver, webdriver-manager, pytest, pytest-html. "
        "Aplicación: HTML/CSS/JS. Navegadores: Brave (ChromeDriver + binary_location), "
        "Firefox (GeckoDriver) y Edge (EdgeDriver). Opción CLI: --browser.",
    )
    add_para(doc, "4.2 Arquitectura y Page Object Model", bold=True)
    add_para(
        doc,
        "Los tests no contienen selectores. LoginPage, RegistroPage y DashboardPage heredan "
        "de BasePage (abrir_url, escribir_texto, hacer_clic, esperar_elemento, tomar_captura). "
        "Las esperas son WebDriverWait + expected_conditions; no se usa time.sleep.",
    )
    add_para(
        doc,
        "Diagrama: pytest → conftest (servidor HTTP + driver) → POM → Selenium → app/ ; "
        "capturas a evidencias/; pytest-html a reportes/reporte.html.",
    )
    add_para(doc, "Extracto de BasePage (esperas explícitas y captura):", italic=True)
    add_code(
        doc,
        """
def esperar_elemento(self, locator):
    return self.wait.until(EC.visibility_of_element_located(locator))

def hacer_clic(self, locator):
    elemento = self.wait.until(EC.element_to_be_clickable(locator))
    elemento.click()
    return elemento

def tomar_captura(self, nombre):
    EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIAS / (nombre if nombre.endswith(".png") else f"{nombre}.png")
    self.driver.save_screenshot(str(ruta))
    return str(ruta)
""",
    )
    add_para(doc, "Extracto de LoginPage (selectores solo en el POM):", italic=True)
    add_code(
        doc,
        """
class LoginPage(BasePage):
    USUARIO = (By.ID, "usuario")
    CONTRASENA = (By.ID, "contrasena")
    BTN_INGRESAR = (By.ID, "btn-ingresar")
    MENSAJE_ERROR = (By.ID, "mensaje-error")

    def iniciar_sesion(self, usuario, contrasena):
        self.escribir_texto(self.USUARIO, usuario)
        self.escribir_texto(self.CONTRASENA, contrasena)
        self.hacer_clic(self.BTN_INGRESAR)
""",
    )
    add_placeholder(
        doc,
        "Figura 5",
        "Fragmento de código abierto en el editor: tests/pages/login_page.py (POM)",
        "captura del IDE mostrando LoginPage",
    )
    add_para(doc, "4.3 Fixtures: servidor, driver y capturas de fallo", bold=True)
    add_para(
        doc,
        "conftest.py levanta ThreadingHTTPServer sobre app/ en un puerto libre (fixture de sesión). "
        "El fixture driver llama a crear_driver(), maximiza y hace quit() al terminar. "
        "El hook pytest_runtest_makereport guarda *_ERROR.png y lo embebe en el HTML si el test falla.",
    )
    add_code(
        doc,
        """
@pytest.fixture
def driver(nombre_navegador):
    navegador = crear_driver(nombre_navegador)
    navegador.maximize_window()
    yield navegador
    navegador.quit()

# Hook (resumen): si reporte.failed → save *_ERROR.png y extras.image(png)
""",
    )
    add_para(doc, "Fábrica de navegadores (Brave por defecto):", italic=True)
    add_code(
        doc,
        """
if nombre == "brave":
    opciones = _opciones_chromium(ChromeOptions(), _ruta_brave())
    servicio = ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
    return webdriver.Chrome(service=servicio, options=opciones)
""",
    )

    add_heading(doc, "5. Scripts automatizados", 1)
    add_para(
        doc,
        "Los siete casos obligatorios viven en tests/test_funcionales.py. pytest.ini excluye "
        "el marcador demo_fallo para que el comando principal quede en verde.",
    )
    add_table(
        doc,
        ["ID", "Caso", "Resultado esperado"],
        [
            ["CT01", "Login credenciales válidas (admin / 123456)", "Redirección a dashboard; «Bienvenido, admin»"],
            ["CT02", "Login contraseña incorrecta", "«Credenciales inválidas»; permanece en login"],
            ["CT03", "Login campos vacíos", "No navega; validity.valueMissing"],
            ["CT04", "Registro usuario nuevo (email único)", "«Registro exitoso»"],
            ["CT05", "Registro email duplicado (admin@demo.com)", "«email ya existe»"],
            ["CT06", "Registro campos vacíos", "Sin éxito; campo required vacío"],
            ["CT07", "Cerrar sesión desde dashboard", "Vuelve a index.html"],
        ],
    )
    add_para(doc, "Fragmento CT01 (flujo POM + aserciones de URL y texto):", italic=True)
    add_code(
        doc,
        """
def test_CT01_login_credenciales_validas(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    captura("test_CT01_login_credenciales_validas_paso1")
    login.iniciar_sesion("admin", "123456")
    dashboard = DashboardPage(driver).esperar_carga()
    captura("test_CT01_login_credenciales_validas_paso2")
    assert "dashboard.html" in dashboard.url_actual()
    assert "Bienvenido, admin" in dashboard.bienvenida()
""",
    )
    add_para(doc, "Fragmento CT05 (email duplicado) y CT07 (cierre de sesión):", italic=True)
    add_code(
        doc,
        """
def test_CT05_registro_email_duplicado(driver, servidor, captura):
    registro = RegistroPage(driver)
    registro.abrir(servidor)
    registro.registrar("Admin Clone", "admin@demo.com", "clave123")
    assert "email ya existe" in registro.mensaje_error()

def test_CT07_cerrar_sesion(driver, servidor, captura):
    login = LoginPage(driver)
    login.abrir(servidor)
    login.iniciar_sesion("admin", "123456")
    DashboardPage(driver).esperar_carga().cerrar_sesion()
    assert "index.html" in login.url_actual()
""",
    )
    add_para(
        doc,
        "Caso extra (no forma parte de la suite verde): test_CT99_demostracion_fallo_intencional "
        "inicia sesión correctamente y aserta un texto inexistente para forzar el hook de captura.",
    )
    add_code(
        doc,
        """
@pytest.mark.demo_fallo
def test_CT99_demostracion_fallo_intencional(driver, servidor, captura):
    ...
    assert "Bienvenido, usuario_inexistente" in dashboard.bienvenida()
""",
    )
    add_placeholder(
        doc,
        "Figura 6",
        "Editor con tests/test_funcionales.py (casos CT01–CT07)",
        "captura del IDE del archivo de tests",
    )

    add_heading(doc, "6. Evidencias", 1)
    add_para(
        doc,
        "Cada prueba toma captura en pasos clave (paso1 formulario, paso2 resultado). "
        "Si falla, el hook genera {nombre_del_test}_ERROR.png. Archivos en evidencias/.",
    )
    add_table(
        doc,
        ["Caso", "Archivo sugerido a pegar"],
        [
            ["CT01 paso 2 (éxito)", "evidencias/test_CT01_login_credenciales_validas_paso2.png"],
            ["CT02 error de clave", "evidencias/test_CT02_login_contrasena_incorrecta_paso2.png"],
            ["CT03 vacíos (login)", "evidencias/test_CT03_login_campos_vacios_paso2.png"],
            ["CT04 registro OK", "evidencias/test_CT04_registro_usuario_nuevo_paso2.png"],
            ["CT05 email duplicado", "evidencias/test_CT05_registro_email_duplicado_paso2.png"],
            ["CT06 vacíos (registro)", "evidencias/test_CT06_registro_campos_vacios_paso2.png"],
            ["CT07 logout", "evidencias/test_CT07_cerrar_sesion_paso2.png"],
            ["Fallo intencional", "evidencias/test_CT99_demostracion_fallo_intencional_ERROR.png"],
        ],
    )
    add_placeholder(
        doc,
        "Figura 7",
        "CT01 — dashboard tras login válido",
        "evidencias/test_CT01_login_credenciales_validas_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 8",
        "CT02 — mensaje Credenciales inválidas",
        "evidencias/test_CT02_login_contrasena_incorrecta_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 9",
        "CT03 — validación de campos vacíos en login",
        "evidencias/test_CT03_login_campos_vacios_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 10",
        "CT04 — mensaje Registro exitoso",
        "evidencias/test_CT04_registro_usuario_nuevo_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 11",
        "CT05 — mensaje email ya existe",
        "evidencias/test_CT05_registro_email_duplicado_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 12",
        "CT06 — validación de campos vacíos en registro",
        "evidencias/test_CT06_registro_campos_vacios_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 13",
        "CT07 — retorno a login tras cerrar sesión",
        "evidencias/test_CT07_cerrar_sesion_paso2.png",
    )
    add_placeholder(
        doc,
        "Figura 14",
        "Reporte pytest-html con los 7 casos en Passed (reportes/reporte.html)",
        "recorte de la tabla del HTML abierto en el navegador",
    )
    add_placeholder(
        doc,
        "Figura 15",
        "Fallo intencional CT99 y captura *_ERROR.png (hook de pytest)",
        "evidencias/test_CT99_demostracion_fallo_intencional_ERROR.png y recorte de reporte_fallo.html",
    )

    add_heading(doc, "7. Reflexión grupal", 1)
    add_para(
        doc,
        "Complete esta sección con el equipo (también está en REFLEXION_GRUPAL.md). "
        "Los párrafos siguientes son base editable.",
        italic=True,
    )
    add_para(doc, "Qué aprendimos en conjunto", bold=True)
    add_para(
        doc,
        "Aprendimos a separar la aplicación bajo prueba de los scripts, a encapsular "
        "selectores con Page Object Model y a generar evidencias reproducibles (PNG + HTML) "
        "sin time.sleep, usando esperas explícitas. También vimos cómo un marcador de pytest "
        "permite una suite verde y, aparte, un caso que falla a propósito para documentar el error.",
    )
    add_para(doc, "[AQUÍ el grupo puede ampliar con ejemplos concretos de la coordinación.]", italic=True)
    add_para(doc, "Dificultades de coordinación y cómo se resolvieron", bold=True)
    add_para(
        doc,
        "Dificultad: alinear el entorno (Python, drivers y navegadores distintos: Brave/Firefox). "
        "Cómo se resolvió: un requirements.txt común, webdriver-manager y la opción --browser, "
        "más un README con los comandos de PowerShell. "
        "[Completar si hubo choques de horarios o de ramas.]",
    )
    add_para(doc, "Ventajas de la automatización en grupo vs individual", bold=True)
    add_para(
        doc,
        "En grupo se puede paralelizar app, POM y redacción, y revisar que los casos cubran "
        "el enunciado (CT01–CT07). En individual es más fácil olvidar evidencias o acoplar "
        "selectores dentro de los tests. La automatización deja un comando único que cualquier "
        "integrante puede reejecutar antes de armar el PDF.",
    )
    add_para(doc, "Conclusión sobre la utilidad de las pruebas automatizadas", bold=True)
    add_para(
        doc,
        "Las pruebas automatizadas no sustituyen el diseño de casos, pero sí reducen el costo "
        "de repetir login, registro y logout, y dejan trazas (reporte y capturas) útiles para "
        "auditoría académica. El fallo intencional muestra que el harness detecta regresiones "
        "y guarda evidencia sin pasos manuales extra.",
    )

    add_heading(doc, "Referencias de archivos del proyecto", 1)
    add_para(
        doc,
        "app/ (index.html, registro.html, dashboard.html, app.js, style.css); "
        "tests/pages/ (base_page.py, login_page.py, registro_page.py, dashboard_page.py); "
        "tests/conftest.py, tests/navegador.py, tests/test_funcionales.py, "
        "tests/test_demostracion_fallo.py; evidencias/; reportes/; README.md; "
        "REFLEXION_GRUPAL.md; GUIA_ENTREGA_PDF.md.",
        size=10,
    )
    add_para(
        doc,
        "Recordatorio de entrega: exportar este Word a PDF como Taller_Automatizacion_[NombreGrupo].pdf, "
        "sin portada, máximo 15 páginas. Reemplace los recuadros amarillos por las PNG reales y "
        "rellene nombres del grupo.",
        size=10,
        italic=True,
    )

    doc.save(SALIDA)
    print(SALIDA)


if __name__ == "__main__":
    build()
