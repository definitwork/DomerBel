const favorite = document.querySelector(".store_ads_list")


favorite.onclick = function(event){
    let target = event.target;
    if (target.className === "favorite_img"){
        if (target.getAttribute("src") === "/static/img/favorite.png"){
            target.src = "/static/img/favorite_yes.png";
        }
        else {
            target.src = "/static/img/favorite.png";
        }
    }
}
