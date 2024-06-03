const modal = document.querySelector('.modals')
const login = document.querySelector('.modals__login')
const loginBtn = document.querySelector('.header__up-user')

modal.addEventListener('click', (event) => {
    if(event.target === modal){
        modal.classList.remove('modal__active')
        document.body.style.overflow = 'auto'
    } 
})

loginBtn.addEventListener('click', () => {
    document.body.style.overflow = 'hidden'
    modal.classList.add('modal__active')
})
