// MENU
document.addEventListener('DOMContentLoaded', function() {
    fetch('/menu')
        .then(response => response.text())
        .then(data => {
            document.getElementById('contenedor_menu').innerHTML = data;
        })
        .catch(error => console.error('Error al cargar el menu', error))
})

function menuAcordeon(index) {
    var elementos = document.querySelectorAll('.si-submenu');

    elementos.forEach(function(elemento, i) {
        var icono = elemento.querySelector('.icono i');
        var submenu = elemento.querySelector('.submenu');
        if (i === index) {
            if (elemento.classList.contains('activo')) {
                elemento.classList.remove('activo');
                submenu.style.display = 'none';
                icono.classList.remove('fa-chevron-down');
                icono.classList.add('fa-chevron-right');
            } else {
                elemento.classList.add('activo');
                submenu.style.display = 'block';
                icono.classList.remove('fa-chevron-right');
                icono.classList.add('fa-chevron-down');
            }
        } else {
            elemento.classList.remove('activo');
            submenu.style.display = 'none';
            icono.classList.remove('fa-chevron-down');
            icono.classList.add('fa-chevron-right');
        }
    })
}

document.getElementById('menu-burger').addEventListener('click', function() {
    var menuNavegacion = document.getElementById('menu-navegacion');
    var menuBurger = document.getElementById('menu-burger');
    var icono = menuBurger.querySelector('.menu-burger i');
    var tituloBar = document.getElementById('titulo-bar');
    var logoBar = document.getElementById('logo-bar');
    var header = document.querySelector('header');

    if (menuNavegacion.style.display === 'none') {
        menuNavegacion.style.display = 'block';
        header.style.width = '';
        header.style.height = '';
        menuBurger.style.left = '';
        menuBurger.style.padding = '';
        menuBurger.style.position = '';
        menuBurger.style.width = '';
        icono.classList.remove('fa-bars');
        icono.classList.add('fa-x');
        logoBar.style.display = 'none';
        tituloBar.style.display = 'none';
    } else {
        menuNavegacion.style.display = 'none';
        header.style.width = '1024px';
        header.style.height = 'fit-content';
        menuBurger.style.boxSizing = 'border-box';
        menuBurger.style.left = '0';
        menuBurger.style.marginLeft = '10px';
        menuBurger.style.padding = '10px 0';
        menuBurger.style.position = 'relative';
        menuBurger.style.width = '1024px';
        icono.classList.remove('fa-x');
        icono.classList.add('fa-bars');
        logoBar.style.display = 'block';
        tituloBar.style.display = 'block';
    }
})