// Регионы для поиска магазинов
let location_opened = document.querySelector(".location_opened");
    location_opened.addEventListener('click', show_region);
let get_element_select_region = document.querySelector("#select_region_2");
let location_hidden = document.querySelector(".location_hidden")


function show_region(event){
    if (event.target.value !== "0"){
        fetch(`http://127.0.0.1:8000/api/v1/add_store/city/${event.target.value}`)
            .then((response) => response.json())
            .then(data => {
                location_hidden.style.display = "flex";
                get_element_select_region.innerHTML = `<option value="0">Любое расположение</option>`
                get_element_select_region.innerHTML += data.map((elem)=>`<option value=${elem.id}>${elem.area}</option>`)
            })
    }
    else {
        get_element_select_region.innerHTML += "";
        location_hidden.style.display = "none";
    }
}


// Выделение объявлений в ЛК поштучно либо сразу всех
let select_all = document.getElementById('select_all');
let checkboxes = document.getElementsByName('ads_checkbox');

select_all.addEventListener('change', select_all_ads);

function select_all_ads(event) {
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = event.target.checked;
    }
}

for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('change', find_unchecked_ads)
}

function find_unchecked_ads(event) {
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == false) {
            select_all.checked = false;
            break;
        }
        select_all.checked = true;
    }
}