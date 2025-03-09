// SELECCIONAR SUPLIDOR
function seleccionarSuplidor(boton) {
    const data = {
        nombre: boton.getAttribute('data-nombre')
    }

    llenarCampoSuplidor(data);
    cerrarModal('modal_suplidores');
}

function llenarCampoSuplidor(data) {
    const input_suplidor = document.getElementById('suplidor');

    input_suplidor.value = data.nombre;
}

// SELECCIONAR ENCARGADO DE COMPRAS
function seleccionarEncargadoCompras(boton) {
    const data = {
        nombre: boton.getAttribute('data-nombre')
    }

    llenarCampoEncargadoCompras(data);
    cerrarModal('modal_encargados_compras');
}

function llenarCampoEncargadoCompras(data) {
    const input_encargado_compra = document.getElementById('encargado_compras');

    input_encargado_compra.value = data.nombre;
}

// SELECCIONAR CLIENTE
function seleccionarCliente(boton) {
    const data = {
        nombre: boton.getAttribute('data-nombre')
    }

    llenarCampoCliente(data);
    cerrarModal('modal_clientes');
}

function llenarCampoCliente(data) {
    const input_cliente = document.getElementById('cliente');

    input_cliente.value = data.nombre;
}

// SELECCIONAR ENCARGADO DE VENTAS
function seleccionarEncargadoVentas(boton) {
    const data = {
        nombre: boton.getAttribute('data-nombre')
    }

    llenarCampoEncargadoVentas(data);
    cerrarModal('modal_encargados_ventas');
}

function llenarCampoEncargadoVentas(data) {
    const input_encargado_venta = document.getElementById('encargado_ventas');

    input_encargado_venta.value = data.nombre;
}

// CERRAR MODAL
function cerrarModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.getElementById('background_modal').style.display = 'none';
}