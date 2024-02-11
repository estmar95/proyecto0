function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/usuarios/iniciar-sesion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre_de_usuario: username, contrasena: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token_de_autenticacion) {
            // Almacenar el token de autenticación en el almacenamiento local
            localStorage.setItem('token', data.token_de_autenticacion);
            // Redireccionar al usuario a la página principal del administrador de tareas
            window.location.href = '/tasks';
        } else {
            console.error('Error al iniciar sesión:', data.mensaje);
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}

function register() {
    const newUsername = document.getElementById('new-username').value;
    const newPassword = document.getElementById('new-password').value;

    fetch('/usuarios', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nombre_de_usuario: newUsername, contrasena: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token_de_autenticacion) {
            // Almacenar el token de autenticación en el almacenamiento local
            localStorage.setItem('token', data.token_de_autenticacion);
            // Redireccionar al usuario a la página principal del administrador de tareas
            window.location.href = '/tasks';
        } else {
            console.error('Error al registrar:', data.mensaje);
        }
    })
    .catch(error => {
        console.error('Error de red:', error);
    });
}
