const sortTypeItem = document.querySelectorAll('.sort__type-list-item');
const advertisementList = document.querySelector('.advertisement__list')
if(!localStorage.getItem("sortType")) {
    localStorage.setItem("sortType", "default__item")
}

const type = ['second__item','default__item']
function setSortIcon() {
    sortTypeItem.forEach(item => {
        item.style.opacity = '1'
    })
    sortTypeItem[type.findIndex(i => i == localStorage.getItem("sortType"))].style.opacity = '0.5'
}

setSortIcon()

function setClassAdvertisementList() {
    advertisementList.classList.add(localStorage.getItem("sortType"))
}

setClassAdvertisementList()

sortTypeItem.forEach(item => {
    item.addEventListener('click', (e) => {
        localStorage.setItem("sortType", type[Array.from(e.currentTarget.parentElement.children).findIndex(i => i == e.currentTarget)])
        advertisementList.classList.remove(advertisementList.classList[1])
        advertisementList.classList.add(localStorage.getItem("sortType"))
        setSortIcon()
    })
})