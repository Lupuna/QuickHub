const search = document.querySelector('.placeholder')

function searchOpen() {
    console.log('Clicked')
    if (search.classList.contains ('open') == false){
        search.classList.add('open')
    } 
    else if (search.classList.contains ('open') == true){
        search.classList.remove('open')
    }

}

document.addEventListener("DOMContentLoaded", (event) => {
    search.onclick = searchOpen
})