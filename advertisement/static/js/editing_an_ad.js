let imageList = document.querySelectorAll(".img_preview")

for (let i of imageList){
    console.log(i.src)
}
if (window.location.href === `http://127.0.0.1:8000/advertisement/editing_an_ad/${document.getElementById('add_adver').dataset.advertisement}/`) {
    console.log(window.location)
}