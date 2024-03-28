const search = document.querySelector('.search')

burger.onclick = function () {
    if (search.className === 'search'){
        search.classList.add('_open')
    } else if (search.className === 'search _open'){
        search.classList.remove('_open')
    }

}