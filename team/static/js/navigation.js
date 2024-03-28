document.addEventListener('DOMContentLoaded', () => {

    const contentDiv = document.querySelector('.content')
    const navLinks = document.querySelectorAll('.nav_link')
    const loadingOverlay = document.querySelector('.loading_overlay')

    const showLoadingOverlay = () => {
        loadingOverlay.style.opacity = '1'
    }

    const hideLoadingOverlay = () => {
        loadingOverlay.style.opacity = '0'
    }

    const loadPage = (url) => {
        showLoadingOverlay()
        fetch(url)
            .then(response => response.text())

            .then(html => {
                const parser = new DOMParser()
                const doc = parser.parseFromString(html, 'text/html')
                const newContent = doc.querySelector('.content').innerHTML

                contentDiv.classList.add('fade_out');
                

                contentDiv.innerHTML = newContent;
                document.title = doc.title

                setTimeout(() => {
                    contentDiv.classList.remove('fade_out')
                    history.pushState({}, '', url)
                    hideLoadingOverlay()
                }, 500)

            })
    }

    navLinks.forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault()

            const url = e.currentTarget.getAttribute('href')
            showLoadingOverlay()
            loadPage(url)
        })
    })


    loadPage(window.location.pathname)

    window.addEventListener('popstate', () => {
        loadPage(window.location.pathname)
    })

})

