document.addEventListener('DOMContentLoaded', function() {
    const contenedor_notificacion = document.getElementById('contenedor_notificacion');
    const boton_cerrar_mensaje = document.getElementById('boton_notificacion');

    boton_cerrar_mensaje.addEventListener('click', function() {
        contenedor_notificacion.style.display = 'none';
    })
})