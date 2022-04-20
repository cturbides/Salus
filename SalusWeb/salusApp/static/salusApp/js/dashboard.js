//=======================Seleccionador============================
//const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function() {
    sidebar.classList.toggle('hide');
})

const switchMode = document.getElementById('switch-mode');

function dark() {
    document.body.classList.add('dark');
}

function light() {
    document.body.classList.remove('dark');
}
if (localStorage.getItem("mode") == "dark") {
    dark();
    switchMode.click();
} else {
    light();
}
window.onload = function() {

}

switchMode.addEventListener('change', function() {
    if (this.checked) {
        dark();
        localStorage.setItem("mode", "dark");
    } else {
        light();
        localStorage.setItem("mode", "light");
    }
})



const url = window.location.href;
let last_part = url.split('/').pop();
let after_dashboard = url.split('/')[5];

if (last_part === '') {
    let select = document.getElementById('dash');
    select.parentElement.classList.add('active');
} else if (after_dashboard === 'mi-clinica') {
    let select = document.getElementById('clinica');
    select.parentElement.classList.add('active');
} else if (after_dashboard === 'analitica') {
    let select = document.getElementById('analitica');
    select.parentElement.classList.add('active');
} else if (after_dashboard === 'equipo') {
    let select = document.getElementById('equipo');
    select.parentElement.classList.add('active');
} else if (after_dashboard === 'settings') {
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