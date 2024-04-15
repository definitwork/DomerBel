const checkBoxes = document.querySelectorAll('.favorite-list__item__input')
const listCheckBoxes = []

for(item of checkBoxes){
    listCheckBoxes.push(item.getAttribute('id'))
}

const deleteButton = document.querySelector('.delete-favorites')

const fLink = document.querySelector('.favorites')
const favoritesHref = fLink.getAttribute('href')
const fNumber = document.querySelector('.favorites__quantity')

const user = getCookie('user_auth')
const favorite = localStorage.getItem(`${user}favorites`)

if (listCheckBoxes){
    setStarsInHeader(checkBoxes, listCheckBoxes)
}

fLink.onmouseover = function(e) {
    fNumber.style.color = 'red'
}

fLink.onmouseout = function(e) {
    fNumber.style.color = '#307792'
}

function setStarsInHeader(num, list){
    const user = getCookie('user_auth')
    const favorites = document.querySelector('.favorites')
    const fNum = document.querySelector('.favorites__quantity')
    if (list.length){
        fNum.innerText = `[${num.length}]`
        favorites.className = 'favorites active'
        favorites.href = `${favoritesHref}?list=${JSON.stringify(list)}`
        localStorage.setItem(`${user}favorites`, JSON.stringify(list))

    } else {
        fNum.innerText = `[]`
        favorites.className = 'favorites'
        favorites.href = `${favoritesHref}?list=[]`
    }
}

if (deleteButton){
    deleteButton.addEventListener('click', deleteCards)
}

function deleteCards(e){
    e.preventDefault()
    e.stopPropagation()

    if (checkBoxes){
        const cardsDelList = []
        const newList = []

        const user = getCookie('user_auth')
        

        for (let i = 0; i < checkBoxes.length; i++){
            newList.push(checkBoxes[i].getAttribute('id'))
        }
        
        localStorage.setItem(`${user}favorites`, JSON.stringify(newList))

        const favorite = localStorage.getItem(`${user}favorites`)

        for (let i = 0; i < checkBoxes.length; i++){
            if (checkBoxes[i].checked){
                cardsDelList.push(checkBoxes[i].getAttribute('id'))
            }
        }
        
        if (favorite) {
            const list = JSON.parse(favorite)
            if (list && cardsDelList.length){
                for (let i = list.length - 1; i >= 0; i--) {
                    for (let j = 0; j < cardsDelList.length; j++) {
                        if (list[i] === cardsDelList[j]) {
                            list.splice(i, 1)
                            break
                        }
                    }
                }
                const href = JSON.stringify(list)
                localStorage.setItem(`${user}favorites`, href)
                location.href = `${favoritesHref}?list=${href}`
            }
        }
    }
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));

    return matches ? decodeURIComponent(matches[1]) : undefined;
}