const hamburger = document.querySelector('.hamburger')
const sidebar = document.querySelector('.sidebar')
const overlay = document.querySelector('.overlay')

hamburger.addEventListener('click', () => {
    sidebar.classList.add('active')
    overlay.classList.add('active')
})

overlay.addEventListener('click', () => {
    sidebar.classList.remove('active')
    overlay.classList.remove('active')
})