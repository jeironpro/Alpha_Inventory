// MODAL EDITAR MARCAS
let modalEdiMar = document.getElementById('miModalEdiMar');
let flexEdiMar = document.getElementById('flexEdiMar');
let abrirEdiMar = document.getElementById('abrirEdiMar');
let cerrarEdiMar = document.getElementById('closeEdiMar');

abrirEdiMar.addEventListener('click', function(){
    modalEdiMar.style.display = 'block';
});

cerrarEdiMar.addEventListener('click', function(){
    modalEdiMar.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexEdiMar){
        modalEdiMar.style.display = 'block';
    }
});
