# Taller de automatización funcional (AA2)

Suite de pruebas funcionales con **Selenium WebDriver**, **pytest** y **pytest-html** sobre una aplicación web estática de login, registro y dashboard.

## Requisitos previos

- Python 3.10 o superior y `pip`
- Al menos uno de estos navegadores: **Brave** (predeterminado), **Firefox** o **Microsoft Edge**
- Conexión a internet la primera vez (webdriver-manager descarga el driver)

Compruebe Python:

```powershell
python --version
pip --version
```

## Instalación de dependencias

En la carpeta del proyecto (`a2/`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```



## Cómo se sirve la aplicación

Las pruebas **levantan solas** un servidor HTTP sobre la carpeta `app/` (módulo `http.server` de Python). No hace falta abrirlo a mano para ejecutar pytest.

Si desea ver la app en el navegador:

```powershell
cd app
python -m http.server 8000
```

Luego abra `http://127.0.0.1:8000/index.html`.

Credenciales de demostración:

- Usuario: `admin`
- Contraseña: `123456`
- Email ya registrado (para el caso de duplicado): `admin@demo.com`



## Cómo ejecutar las pruebas

Desde la raíz del proyecto, con el entorno virtual activado. Por defecto se usa **Brave**:

```powershell
pytest tests/ --html=reportes/reporte.html --self-contained-html
```

El mismo comando en Firefox o Edge:

```powershell
pytest tests/ --browser=firefox --html=reportes/reporte.html --self-contained-html
pytest tests/ --browser=edge --html=reportes/reporte.html --self-contained-html
```

Deben pasar los siete casos obligatorios (CT01 a CT07). El caso de demostración de fallo queda fuera por un marcador de pytest.

Para generar a propósito un fallo y su captura de error:

```powershell
pytest tests/test_demostracion_fallo.py -m demo_fallo --html=reportes/reporte_fallo.html --self-contained-html
```

Si un ejecutable no está en la ruta habitual, defina `BRAVE_BIN`, `FIREFOX_BIN` o `EDGE_BIN` con la ruta completa al `.exe`.

## Cómo interpretar el reporte HTML

1. Abra `reportes/reporte.html` en Brave, Firefox o Edge.
2. La tabla resume cada prueba: **Passed** o **Failed**, duración y nombre (`test_CT01_...`).
3. `--self-contained-html` embebe estilos e imágenes: el archivo se puede copiar solo al PDF o enviar por correo.
4. Si una prueba falla, el hook de pytest adjunta la captura `*_ERROR.png` al reporte.


## Estructura del proyecto

- `app/`: aplicación bajo prueba (HTML, CSS, JS)
- `tests/pages/`: Page Object Model
- `tests/test_funcionales.py`: CT01–CT07
- `tests/test_demostracion_fallo.py`: fallo intencional
- `evidencias/`: capturas PNG
- `reportes/`: reporte HTML de pytest-html

