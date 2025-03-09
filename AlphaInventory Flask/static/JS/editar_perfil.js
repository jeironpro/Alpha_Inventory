document.addEventListener('DOMContentLoaded', function() {
    const boton = document.getElementById('boton_editar_perfil');
    const boton_editar = document.querySelector('.botones .boton_editar');

    const input_perfil = document.querySelectorAll('.campo .input_perfil');

    boton.addEventListener('click', function() {
        boton_editar.style.display = 'block';
        boton.style.display = 'none';

        input_perfil.forEach(input => {
            input.removeAttribute('readonly');
        });
    });
});