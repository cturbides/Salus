//=======================Seleccionador============================
//const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
const switchMode = document.getElementById('switch-mode');
const dark = () => document.body.classList.add('dark');
const light = () => document.body.classList.remove('dark');

switchMode.addEventListener('change', function() {
    if (this.checked) {
        dark();
        localStorage.setItem("mode", "dark");
    } else {
        light();
        localStorage.setItem("mode", "light");
    }
})

window.onload = () => {
    if (localStorage.getItem("mode") == "dark") {
        dark();
        switchMode.click();
    } else
        light();
}
 
const url = window.location.href;
const lastPart = url.split('/').pop();
let urlTag = url.split('/')[5];
let select;

if (!lastPart) {
    select = document.getElementById('dash');
    select.parentElement.classList.add('active');
} else {
    switch (urlTag) {
        case 'mi-clinica':
            select = document.getElementById('clinica');
            select.parentElement.classList.add('active');
            break;
        
        case 'equipo':
            select = document.getElementById('equipo');
            select.parentElement.classList.add('active');

        default:
            select = document.getElementById('settings');
            select.parentElement.classList.add('active');
            break;
    }
}
//================================================================