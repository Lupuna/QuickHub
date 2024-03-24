document.addEventListener("DOMContentLoaded", (event) => {

    const burger = document.querySelector('.btn_burger')
    const menu = document.getElementById('left_bar')
    const container = document.querySelector('.container')

    burger.onclick = function () {
        if (menu.className === 'left_bar'){
            container.style.cssText = 'grid-template-columns: 64px auto;'
            menu.classList.add('_close')
        } else if (menu.className === 'left_bar _close'){
            container.style.cssText = 'grid-template-columns: 225px auto;'
            menu.classList.remove('_close')
        }
    }
    
})
