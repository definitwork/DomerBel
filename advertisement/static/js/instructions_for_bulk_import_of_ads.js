//const area = document.querySelector('.areas_or_cities')
const area = document.querySelector('.one_city')
const city = document.querySelector('.cities_or_districts')
area.addEventListener('click', openList)

function openList(){
    city.classList.toggle('cities_or_districts__active');
}



