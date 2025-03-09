document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.mostrar').forEach(icono => {
        icono.addEventListener('click', () => {
            const target = icono.getAttribute('data-target');
            const input = document.getElementById(target);

            icono.classList.toggle('fa-eye-slash');
            icono.classList.toggle('fa-eye');

            input.type = input.type === 'password' ? 'text': 'password';
        });
    })
})