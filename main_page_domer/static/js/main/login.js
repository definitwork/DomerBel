const modalBlock = document.querySelector('.modals');
const modalLogin = document.querySelector('.modals__login');
const loginBtn = document.querySelector('.header__up-user');

modalBlock.addEventListener('click', (event) => {
    if(event.target === modalBlock){
        modalBlock.classList.remove('modal__active');
        modalLogin.classList.remove('modal__active');
        document.body.style.overflow = 'auto';
    } 
})

loginBtn.addEventListener('click', () => {
    document.body.style.overflow = 'hidden';
    modalBlock.classList.add('modal__active');
    modalLogin.classList.add('modal__active');
})
