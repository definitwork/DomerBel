const modalBlock = document.querySelector('.modals')
const login = document.querySelector('.modals__login')
const loginBtn = document.querySelector('.header__up-user')

modalBlock.addEventListener('click', (event) => {
    if(event.target === modalBlock){
        modalBlock.classList.remove('modal__active')
        document.body.style.overflow = 'auto'
    } 
})

loginBtn.addEventListener('click', () => {
    document.body.style.overflow = 'hidden'
    modalBlock.classList.add('modal__active')
})
