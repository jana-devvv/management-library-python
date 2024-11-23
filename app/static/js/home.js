// Modal
const modal = document.getElementById('modal')
const closeModal = document.getElementById('closeModal')
const textModal = document.getElementById('textModal')
const confirmYes = document.getElementById('confirmYes')
const confirmNo = document.getElementById('confirmNo')
const modalForm = document.getElementById('modalForm')

document.querySelectorAll('.open-modal').forEach(button => {
    const id = button.getAttribute('id')
    button.addEventListener('click', function() {
        const bookId = this.getAttribute('data-id')
        modal.style.display = 'flex'
        document.body.classList.add('no-scroll')

        if(id === 'borrowBook') {
            textModal.innerText = 'Are you sure want to borrow this book?'
            modalForm.setAttribute('action', `loan/${bookId}`)
        }
        
        if(id === 'deleteBook') {
            textModal.innerText = 'Are you sure want to delete this book?'
            modalForm.setAttribute('action', `delete/${bookId}`)
        }
    })
})

closeModal.addEventListener('click', () => {
    modal.style.display = 'none'
    document.body.classList.remove('no-scroll')
})

confirmYes.addEventListener('click', () => {
    modal.style.display = 'none'
    document.body.classList.remove('no-scroll')
})

confirmNo.addEventListener('click', () => {
    modal.style.display = 'none'
    document.body.classList.remove('no-scroll')
})