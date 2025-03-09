function seleccionarArticulo(boton, tipo) {
    const cantidadInput = boton.closest('tr').querySelector('.cantidad_articulos');

    const data = {
        codigo: boton.getAttribute('data-codigo'),
        descripcion: boton.getAttribute('data-descripcion'),
        cantidad: cantidadInput.value,
        itbis: boton.getAttribute('data-itbis'),
        costo_precio: boton.getAttribute('data-costo') || boton.getAttribute('data-precio'),
    };
    boton.setAttribute('data-cantidad', data.cantidad);

    if (tipo === 'compras') {
        llenarCamposCompra(data);
        cerrarModal('modal_articulos_compras');
    } else if (tipo === 'ventas') {
        llenarCamposVenta(data);
        cerrarModal('modal_articulos_ventas');
    }
}

function llenarCamposCompra(data) {
    llenarCampos(data, 'costo');
}

function llenarCamposVenta(data) {
    llenarCampos(data, 'precio');
}

function llenarCampos(data, costo_precio) {
    const tabla = document.getElementById('tabla_articulos').getElementsByTagName('tbody')[0];
    const filas = tabla.rows;

    for (let i = 0; i < filas.length; i++) {
        const fila = filas[i];
        const inputs = obtenerInputs(fila);

        if (inputs && !inputs.codigo.value && !inputs.descripcion.value && !inputs.cantidad.value && !inputs.costo_precio.value) {
            inputs.codigo.value = data.codigo;
            inputs.descripcion.value = data.descripcion;
            inputs.cantidad.value = data.cantidad;
            inputs.itbis.value = data.itbis;
            inputs.costo_precio.value = data.costo_precio;
            return;
        }
    }
}

function obtenerInputs(fila) {
    const inputs = {
        codigo: fila.cells[0].getElementsByTagName('input')[0],
        descripcion: fila.cells[1].getElementsByTagName('input')[0],
        cantidad: fila.cells[2].getElementsByTagName('input')[0],
        itbis: fila.cells[3].getElementsByTagName('select')[0],
        costo_precio: fila.cells[4].getElementsByTagName('input')[0]
    };

    if (inputs.codigo && inputs.descripcion && inputs.cantidad && inputs.itbis && inputs.costo_precio) {
        return inputs;
    } else {
        console.log("Uno o más elementos no existen en la fila:", fila);
        return null;
    }
}

function cerrarModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.getElementById('background_modal').style.display = 'none';
}