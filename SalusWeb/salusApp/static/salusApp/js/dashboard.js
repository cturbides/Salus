//=======================Seleccionador============================
//const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
const url = window.location.href;
let last_part = url.split('/').pop()

if (last_part === '') {
    let select = document.getElementById('dash');
    select.parentElement.classList.add('active');
} else if (last_part === 'mi-clinica') {
    let select = document.getElementById('clinica');
    select.parentElement.classList.add('active');
} else if (last_part === 'analitica') {
    let select = document.getElementById('analitica');
    select.parentElement.classList.add('active');
} else if (last_part === 'equipo') {
    let select = document.getElementById('equipo');
    select.parentElement.classList.add('active');
} else if (last_part === 'doctores') {
    let select = document.getElementById('equipo');
    select.parentElement.classList.add('active');
} else if (last_part === 'enfermeros') {
    let select = document.getElementById('equipo');
    select.parentElement.classList.add('active');
} else if (last_part === 'pacientes') {
    let select = document.getElementById('equipo');
    select.parentElement.classList.add('active');
} else if (last_part === 'settings') {
    let select = document.getElementById('settings');
    select.parentElement.classList.add('active');
}
/*
allSideMenu.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', function() {
        allSideMenu.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});
*/
//================================================================