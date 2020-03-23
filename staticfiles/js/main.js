main_menu = document.querySelectorAll('#main_menu .nav-item');

function changeActiveTab(tab){
    console.log(tab);
}

main_menu.forEach(m => {
    m.addEventListener('click',e=>changeActiveTab(m));
});