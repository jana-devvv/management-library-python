// Navbar
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

// Profile
const profile = document.getElementById('profile')
const dropdownMenu = document.getElementById('dropdownMenu')

profile.addEventListener('click', (e) => {
    e.preventDefault()
    const isDropdownVisible = dropdownMenu.style.display === 'block'
    dropdownMenu.style.display = isDropdownVisible ? 'none' : 'block'
})

document.addEventListener('click', (e) => {
    if(!profile.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.style.display = 'none'
    }
})