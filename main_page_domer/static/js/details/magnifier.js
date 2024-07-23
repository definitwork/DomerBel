const btn = document.querySelector('.magnifier')
const modal = document.querySelector('.modals')
const magnifierModal = document.querySelector(".magnifier__zoom")

btn.addEventListener('click', () => {
  document.body.style.overflow = 'hidden'
    modal.classList.add('modal__active')
    magnifierModal.classList.add('modal__active')
      $(".magnifier__zoom-main").slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        infinite: true,
        asNavFor: ".magnifier__zoom-second",
        touchMove:false,
      });
})

modal.addEventListener('click', (event) => {
  if(event.target === modal) {
    document.body.style.overflow = 'auto'
    modal.classList.remove('modal__active')
  } 
})