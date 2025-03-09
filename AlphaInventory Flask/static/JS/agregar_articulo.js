document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.querySelector('.tabla tbody');
    let filas = Array.from(tbody.querySelectorAll('tr'));
    const filas_paginas = 8;
    let pagina_actual = 1;

    function mostrarPagina(pagina) {
        filas.forEach(fila => {
            fila.style.display = 'none';
        });

        const inicio = (pagina - 1) * filas_paginas;
        const fin = inicio + filas_paginas;

        for (let i = inicio; i < fin && i < filas.length; i++) {
            filas[i].style.display = 'table-row';
        }

        actualizarPagina();
    }

    function actualizarPagina() {
        const paginas_totales = Math.ceil(filas.length / filas_paginas);
        const pagina_actual_elemento = document.querySelector('.pagina_actual');
        const paginas_totales_elemento = document.querySelector('.paginas_totales');

        pagina_actual_elemento.textContent = pagina_actual;
        paginas_totales_elemento.textContent = paginas_totales;

        const boton_anterior = document.getElementById('anterior');
        const boton_siguiente = document.getElementById('siguiente');

        boton_anterior.disabled = pagina_actual === 1;
        boton_siguiente.disabled = pagina_actual === paginas_totales;
    }

    const boton_anterior = document.getElementById('anterior');
    const boton_siguiente = document.getElementById('siguiente');

    boton_anterior.addEventListener('click', function() {
        if (pagina_actual > 1) {
            pagina_actual--;
            mostrarPagina(pagina_actual);
        }
    });

    boton_siguiente.addEventListener('click', function() {
        const paginas_totales = Math.ceil(filas.length / filas_paginas);
        if (pagina_actual < paginas_totales) {
            pagina_actual++;
            mostrarPagina(pagina_actual);
        }
    });

    function generarFilaArticulo(tipo, numero_articulos) {
        let placeholderPrecioCosto = tipo === 'venta' ? 'precio' : 'costo';

        return `
        <tr>
            <td><input type="text" id="codigo_${numero_articulos}" name="codigo_${numero_articulos}" placeholder="0000000" class="nth" autocomplete="off" required></td>
            <td><input type="text" id="descripcion_${numero_articulos}" name="descripcion_${numero_articulos}" placeholder="descripci&oacute;n" class="nth" autocomplete="off" required></td>
            <td><input type="number" id="cantidad_${numero_articulos}" name="cantidad_${numero_articulos}" placeholder="000" class="nth" autocomplete="off" required></td>
            <td>
                <select name="itbis_${numero_articulos}" id="itbis_${numero_articulos}" size="1" autocomplete="off" required>
                    <option selected>Sel. impuesto</option>
                    <option>18</option>
                    <option>16</option>
                    <option>0</option>
                </select>
            </td>
            <td><input type="number" id="${placeholderPrecioCosto}_${numero_articulos}" name="${placeholderPrecioCosto}_${numero_articulos}" placeholder="00.00" class="nth" autocomplete="off" required></td>
        </tr>
        `;
    }

    function agregarFila(tipo) {
        let contenedor;
        let input_numero_articulos;

        if (tipo === 'venta') {
            contenedor = document.querySelector('#tabla_articulos tbody');
            input_numero_articulos = document.getElementById('numero_articulos_venta');
        } else if (tipo === 'compra') {
            contenedor = document.querySelector('#tabla_articulos tbody');
            input_numero_articulos = document.getElementById('numero_articulos_compra');
        }

        let numero_articulos = parseInt(input_numero_articulos.value) + 1;

        let nuevaFila = generarFilaArticulo(tipo, numero_articulos);
        contenedor.insertAdjacentHTML('beforeend', nuevaFila);

        input_numero_articulos.value = numero_articulos;

        filas = Array.from(tbody.querySelectorAll('tr'));
        mostrarPagina(pagina_actual);
    }

    mostrarPagina(pagina_actual);
    
    document.querySelector('.boton').addEventListener('click', function() {
        agregarFila('compra');
    });

    document.querySelector('.boton').addEventListener('click', function() {
        agregarFila('venta');
    });
});