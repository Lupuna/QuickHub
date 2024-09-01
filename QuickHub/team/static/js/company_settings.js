const openSettings = document.querySelector('.btn_company_settings')
const btnClose =  document.querySelector('.btn_close')
const btnCancel = document.querySelector('.btn_cancel')
const btnSave = document.querySelector('.btn_save')
const companySettings = document.querySelector('.company_settings')

openSettings.addEventListener('click', function(event){
    event.preventDefault()
    companySettings.classList.add('active')
})

function closeSettings(){
    companySettings.classList.remove('active')
}

btnClose.addEventListener('click', closeSettings )
btnCancel.addEventListener('click', closeSettings )