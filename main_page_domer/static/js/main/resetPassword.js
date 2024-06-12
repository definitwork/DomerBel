const modalResetPassowrd = document.querySelector('.modals__reset-password');
const backBtn = document.querySelector('.modals__reset-password a')


resetPasswordBtn.addEventListener('click', () => {
    for(let i of modal.children) {
        i.classList.remove('modal__active')
    }
    modalResetPassowrd.classList.add('modal__active')
})


backBtn.addEventListener('click', () => {
    for(let i of modal.children) {
        i.classList.remove('modal__active')
    }
    signUp.classList.add('modal__active')
})