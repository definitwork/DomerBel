const modalBlock = document.querySelector('.modals');
const modalLogin = document.querySelector('.modals__login');
const loginBtn = document.querySelector('.header__up-user');

modalBlock.addEventListener('click', (event) => {
    if(event.target === modalBlock){
        modalBlock.classList.remove('modal__active');
        for(let i of modalBlock.children) {
            i.classList.remove('modal__active');
            const fieldErorr = document.querySelectorAll('.modals__signIn-error')
            fieldErorr.forEach(item => item.remove())
        }
        document.body.style.overflow = 'auto';
    } 
})

loginBtn?.addEventListener('click', () => {
    document.body.style.overflow = 'hidden';
    modalBlock.classList.add('modal__active');
    modalLogin.classList.add('modal__active');
})
