const burger = document.querySelector('.btn_burger')
const menu = document.querySelector('.left_bar a')
const container = document.querySelector('.container')

let closed = true

burger.onclick = function () {
    console.log('Hello')
    if (closed == true){
        container.style.cssText = 'grid-template-columns: 100px auto;'
        closed = false
    } else if (closed == false){
        container.style.cssText = 'grid-template-columns: 225px auto;'
        closed = true
    }

}
