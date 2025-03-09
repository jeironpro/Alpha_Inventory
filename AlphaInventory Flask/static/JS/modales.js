// MOSTRAR MODALES
function cargarModal(id_modal) {
    var pagina_modales = 'modales.html';

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var div_temporal = document.createElement('div');
                div_temporal.innerHTML = xhr.responseText;
                var contenido_modal = div_temporal.querySelector('#' + id_modal);

                if (contenido_modal) {
                    var contenedor_modal = document.getElementById('contenedor_modal');
                    contenedor_modal.innerHTML = '';
                    var clonarModal = contenido_modal.cloneNode(true);
                    clonarModal.style.display = 'block';
                    contenedor_modal.appendChild(clonarModal);
                    document.getElementById('background_modal').style.display = 'block';

                    var boton_cerrar = clonarModal.querySelector('.cerrar_modal');
                    boton_cerrar.addEventListener('click', function() {
                        cerrarModal(id_modal);
                    });

                    if (id_modal === 'modal_mostrar_marcas') {
                        var boton_editar = clonarModal.querySelector('button[onclick="cargarModal(\'modal_editar_marca\')"]');

                        if (boton_editar) {
                            boton_editar.addEventListener('click', function() {
                                cargarModal('modal_editar_marca');
                            });
                        }
                    } else if (id_modal === 'modal_mostrar_encargados_compras') {
                        var boton_editar = clonarModal.querySelector('button[onclick="cargarModal(\'modal_editar_encargado_compras\')"]');

                        if (boton_editar) {
                            boton_editar.addEventListener('click', function() {
                                cargarModal('modal_editar_encargado_compras');
                            })
                        }
                    } else if (id_modal === 'modal_mostrar_encargados_ventas') {
                        var boton_editar = clonarModal.querySelector('button[onclick="cargarModal(\'modal_editar_encargado_ventas\')"]');

                        if (boton_editar) {
                            boton_editar.addEventListener('click', function() {
                                cargarModal('modal_editar_encargado_ventas');
                            })
                        }
                    }
                }
            } else {
                console.log("Error al cargar la modal:" + xhr.status);
            }
        }
    };
    xhr.open('GET', pagina_modales, true);
    xhr.send();
}

function mostrarModal(id_modal) {
    cargarModal(id_modal);
}

function cerrarModal(id_modal) {
    document.getElementById(id_modal).style.display = 'none';
    document.getElementById('background_modal').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function() {

    window.editarMarca = function(id, codigo, nombre) {
        cargarModal('modal_editar_marca');
        console.log(id, codigo, nombre)
        
        setTimeout(function() {
            var codigo_input = document.getElementById('codigo_marca_editar');
            var nombre_input = document.getElementById('nombre_marca_editar');
    
            if (codigo_input && nombre_input) {
                codigo_input.value = codigo;
                nombre_input.value = nombre;
                document.getElementById('formulario_editar_marca_modal').action = '/editarmarca/' + id;
                console.log('/editarmarca/' + id)
            }
        }, 100)
    }

    window.editarEncargadoCompras = function(id, codigo, nombre) {
        cargarModal('modal_editar_encargado_compras');

        setTimeout(function() {
            var codigo_input = document.getElementById('codigo_encargado_compras_editar');
            var nombre_input = document.getElementById('nombre_encargado_compras_editar');

            if (codigo_input && nombre_input) {
                codigo_input.value = codigo;
                nombre_input.value = nombre;
                document.getElementById('formulario_editar_encargado_compras_modal').action = '/editarencargadocompras/' + id;
            }
        }, 100)
    }

    window.editarEncargadoVentas = function(id, codigo, nombre) {
        cargarModal('modal_editar_encargado_ventas');

        setTimeout(function() {
            var codigo_input = document.getElementById('codigo_encargado_ventas_editar');
            var nombre_input = document.getElementById('nombre_encargado_ventas_editar');

            if (codigo_input && nombre_input) {
                codigo_input.value = codigo;
                nombre_input.value = nombre;
                document.getElementById('formulario_editar_encargado_ventas_modal').action = '/editarencargadoventas/' + id;
            }
        }, 100)
    }
})
    