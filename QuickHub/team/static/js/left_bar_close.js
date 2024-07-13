const burger = document.querySelector('.btn_burger')
const menu = document.getElementById('left_bar')
const container = document.querySelector('.container')

function burgerClick() {
    if (menu.classList.contains ('close') == false){
        container.style.cssText = 'grid-template-columns: 64px auto;'
        menu.classList.add('close')
    } 
    else if (menu.classList.contains ('close') == true){
        container.style.cssText = 'grid-template-columns: 225px auto;'
        menu.classList.remove('close')
    }
}

burger.addEventListener('click', burgerClick)

