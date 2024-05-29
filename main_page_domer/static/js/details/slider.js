$(document).ready(function () {
  $(".details__advertisement-view-list-img").slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: true,
    vertical: true,
    touchMove:false,
    varibaleWidth: true,
  });

  $(".details__advertisement-view-img").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    infinite: true,
    asNavFor: ".details__advertisement-view-list-img",
    touchMove:false,
  });

  $(".magnifier__zoom-second").slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: true,
    vertical: true,
    touchMove:false,
    varibaleWidth: true,
  });


  $('.details__advertisement-view-list-img-item').on("click", function () {
    setMainImage($(this),'.details__advertisement-view-img');
  })

  $('.magnifier__zoom-second-item').on("click", function () {
    setMainImage($(this),".magnifier__zoom-main");
  })

  function setMainImage(thisElem, el) {
    $(el).slick('slickGoTo', +thisElem.attr('data-slick-index'))
  }
  
});


