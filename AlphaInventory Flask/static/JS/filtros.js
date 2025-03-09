document.addEventListener('DOMContentLoaded', function() {
    const boton_abrir = document.getElementById('abrir_filtro');
    const boton_cerrar = document.getElementById('cerrar_filtro');
    const contenedor_filtro = document.getElementById('contenedor_filtro');
    
    boton_abrir.addEventListener('click', function() {
        boton_abrir.style.display = 'none';
        contenedor_filtro.style.display = 'flex';
    })

    boton_cerrar.addEventListener('click', function() {
        boton_abrir.style.display = 'flex';
        contenedor_filtro.style.display = 'none';
    })
})