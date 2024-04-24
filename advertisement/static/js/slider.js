$(document).ready(function () {
  $(".details__advertisement-view-list-img").slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: true,
    vertical: true,
    touchMove:false,
    varibaleWidth: true,
    lazyLoad: "ondemand",
  });


  $('.details__advertisement-view-list-img-item').on("click", function () {
    setMainImage($(this));
  })
  function setMainImage(el) {
    const mainImage = $(".details__advertisement-view-img img");
    mainImage.attr("src", el[0].children[0].src);
  }
});
