document.addEventListener('DOMContentLoaded', function() {
    const tbody = document.querySelector('table tbody');
    const filas = Array.from(tbody.querySelectorAll('tr'));
    const filas_paginas = 10;

    let pagina_actual = 1;

    function mostarPagina(pagina) {
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
            mostarPagina(pagina_actual);
        }
    });

    boton_siguiente.addEventListener('click', function() {
        const paginas_totales = Math.ceil(filas.length / filas_paginas);
        if (pagina_actual < paginas_totales) {
            pagina_actual++;
            mostarPagina(pagina_actual);
        }
    });
    mostarPagina(pagina_actual);
});