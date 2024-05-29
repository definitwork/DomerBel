const btn = document.querySelector('.magnifier')
const modal = document.querySelector('.modals')

btn.addEventListener('click', () => {
    modal.classList.add('modal__active')
    
      $(".magnifier__zoom-main").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        asNavFor: ".magnifier__zoom-second",
        touchMove:false,
      });
})

modal.addEventListener('click', (event) => {
    if(event.target === modal) modal.classList.remove('modal__active')
})