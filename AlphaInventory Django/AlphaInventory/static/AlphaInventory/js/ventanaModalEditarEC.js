// MODAL EDITAR ENCARGADO DE COMPRAS
let modalEdiEC = document.getElementById('miModalEdiEC');
let flexEdiEC = document.getElementById('flexEdiEC');
let abrirEdiEC = document.getElementById('abrirEdiEC');
let cerrarEdiEC = document.getElementById('closeEdiEC');

abrirEdiEC.addEventListener('click', function(){
    modalEdiEC.style.display = 'block';
});

cerrarEdiEC.addEventListener('click', function(){
    modalEdiEC.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexEdiEC){
        modalEdiEC.style.display = 'block';
    }
});