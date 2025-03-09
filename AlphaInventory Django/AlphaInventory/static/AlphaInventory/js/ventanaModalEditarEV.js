// MODAL EDITAR ENCARGADO DE VENTAS
let modalEdiEV = document.getElementById('miModalEdiEV');
let flexEdiEV = document.getElementById('flexEdiEV');
let abrirEdiEV = document.getElementById('abrirEdiEV');
let cerrarEdiEV = document.getElementById('closeEdiEV');
let modalENV = document.getElementById('miModalENV');
let cerrarENV = document.getElementById('closeENV');


abrirEdiEV.addEventListener('click', function(){
    modalEdiEV.style.display = 'block';
});

cerrarEdiEV.addEventListener('click', function(){
    modalEdiEV.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexEdiEV){
        modalEdiEV.style.display = 'block';
    }
});