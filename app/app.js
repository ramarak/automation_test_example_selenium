const EMAIL_DUPLICADO = "admin@demo.com";
const USUARIO_VALIDO = "admin";
const CLAVE_VALIDA = "123456";
const STORAGE_USUARIOS = "aa2_usuarios";
const STORAGE_SESION = "aa2_sesion";

function usuariosRegistrados() {
  const raw = localStorage.getItem(STORAGE_USUARIOS);
  const extra = raw ? JSON.parse(raw) : [];
  const base = [{ nombre: "admin", email: EMAIL_DUPLICADO }];
  const emails = new Set(base.map((u) => u.email));
  extra.forEach((u) => {
    if (!emails.has(u.email)) {
      base.push(u);
    }
  });
  return base;
}

function guardarUsuario(usuario) {
  const actuales = usuariosRegistrados();
  actuales.push(usuario);
  localStorage.setItem(STORAGE_USUARIOS, JSON.stringify(actuales));
}

function emailExiste(email) {
  return usuariosRegistrados().some(
    (u) => u.email.toLowerCase() === email.toLowerCase()
  );
}

function campoVacio(valor) {
  return !valor || !valor.trim();
}

function iniciarLogin() {
  const form = document.getElementById("form-login");
  const error = document.getElementById("mensaje-error");
  if (!form) {
    return;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const usuarioInput = document.getElementById("usuario");
    const claveInput = document.getElementById("contrasena");
    const usuario = usuarioInput.value;
    const clave = claveInput.value;
    error.textContent = "";

    if (campoVacio(usuario) || campoVacio(clave)) {
      usuarioInput.reportValidity();
      claveInput.reportValidity();
      return;
    }

    if (usuario === USUARIO_VALIDO && clave === CLAVE_VALIDA) {
      sessionStorage.setItem(
        STORAGE_SESION,
        JSON.stringify({ nombre: USUARIO_VALIDO })
      );
      window.location.href = "dashboard.html";
      return;
    }

    error.textContent = "Credenciales inválidas";
  });
}

function iniciarRegistro() {
  const form = document.getElementById("form-registro");
  const error = document.getElementById("mensaje-error");
  const exito = document.getElementById("mensaje-exito");
  if (!form) {
    return;
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    error.textContent = "";
    exito.textContent = "";

    const nombre = document.getElementById("nombre");
    const email = document.getElementById("email");
    const clave = document.getElementById("contrasena");
    const confirmar = document.getElementById("confirmar");

    const vacios = [nombre, email, clave, confirmar].filter((el) =>
      campoVacio(el.value)
    );
    if (vacios.length > 0) {
      vacios[0].reportValidity();
      return;
    }

    if (clave.value !== confirmar.value) {
      error.textContent = "Las contraseñas no coinciden";
      return;
    }

    if (emailExiste(email.value.trim())) {
      error.textContent = "email ya existe";
      return;
    }

    guardarUsuario({
      nombre: nombre.value.trim(),
      email: email.value.trim(),
    });
    exito.textContent = "Registro exitoso";
  });
}

function iniciarDashboard() {
  const bienvenida = document.getElementById("bienvenida");
  const botonSalir = document.getElementById("btn-cerrar-sesion");
  if (!bienvenida || !botonSalir) {
    return;
  }

  const sesionRaw = sessionStorage.getItem(STORAGE_SESION);
  if (!sesionRaw) {
    window.location.href = "index.html";
    return;
  }

  const sesion = JSON.parse(sesionRaw);
  bienvenida.textContent = `Bienvenido, ${sesion.nombre}`;

  botonSalir.addEventListener("click", () => {
    sessionStorage.removeItem(STORAGE_SESION);
    window.location.href = "index.html";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  iniciarLogin();
  iniciarRegistro();
  iniciarDashboard();
});
