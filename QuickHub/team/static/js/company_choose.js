const menuCompany = document.querySelector('.menu_company')
const chooseCompany = document.querySelector('.company_choose')
const companyName = document.querySelector('.company_name')
const body = document.body

function closeMenuCompany(){
    menuCompany.classList.remove('active')
    companyName.style.borderRadius = '10px'
}

function openMenuCompany(){
    menuCompany.classList.add('active')
    companyName.style.borderRadius = '10px 10px 0 0'
}

chooseCompany.addEventListener('click', function(event){
    event.isClicked = true
    if (menuCompany.classList.contains('active') == false){
        openMenuCompany()
    }
    else if(menuCompany.classList.contains('active') == true){
        closeMenuCompany()
    }
})

window.addEventListener('click', function (event){
    if (event.isClicked == true) return
        closeMenuCompany()
})



