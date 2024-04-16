const regionOpened = document.querySelector(".region_opened");
      regionOpened.addEventListener('click', showCity);
const getElementSelectOblast = document.getElementById("select_oblast");
const getElementSelectCategory0 = document.getElementById("select_category_0");
const categorySelect = document.querySelector(".category_select");
      categorySelect.addEventListener('click', showCategory)
let regionStatus = ''
let statusCategory0 = ''
let statusCategory1 = ''
let statusCategory2 = ''
let statusCategory3 = ''
const informationList = document.querySelector(".additional_information");
      informationList.addEventListener('click', showAdditionalInformationTwo)
let statusElementTwo = ''


function showOblast() {
    fetch(`http://127.0.0.1:8000/api/v1/get_region_list/`)
        .then((response) => response.json())
        .then(data => {
            let array = data.filter(function (i) {
                return i.level === 0
            })
            array.map((elem) => {
                let optionElem = document.createElement('option')
                optionElem.setAttribute('value', `${elem.id}`)
                optionElem.innerText = `${elem.area}`
                getElementSelectOblast.append(optionElem)
            })
        })
}

showOblast()


function showCity(event) {
    if (event.target.value !== regionStatus) {
        regionStatus = event.target.value
        if (event.target.value !== "0") {
            fetch(`http://127.0.0.1:8000/api/v1/add_store/city/${event.target.value}`)
                .then((response) => response.json())
                .then(data => {
                    if (document.querySelector('.city')) {
                        document.getElementById('select_city').innerHTML = ` 
                    <option value="">---------</option>
                    ${data.map((elem) => `<option value=${elem.id}>${elem.area}</option>`)}`
                    } else {
                        let region = document.createElement('p')
                        region.classList.add("city")

                        region.innerHTML = `
                <select class="input_field" id="select_city" name="region">
                        <option value="">---------</option>
                    ${data.map((elem) => `<option value=${elem.id}>${elem.area}</option>`)}
                    </select>
                `
                        event.target.parentElement.parentElement.append(region)
                    }
                })
        } else if (event.target.value === "0") {
            if (document.querySelector('.city')) {
                document.querySelector('.city').remove()
            }
        }
    }
}

fetch("http://127.0.0.1:8000/api/v1/add_store/categories/")
    .then((response) => response.json())
    .then((data) => {
        let array = data.filter(function (i) {
            return i.level === 0
        })
        getElementSelectCategory0.innerHTML += array.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)

    })

function showCategory(event) {
    if (event.target === getElementSelectCategory0 && event.target.value !== statusCategory0) {
        statusCategory0 = event.target.value
        if (event.target.value !== '') {
            fetch(`http://127.0.0.1:8000/api/v1/get_category_list/?id=${event.target.value}`)
                .then((response) => response.json())
                .then((data) => {
                    informationList.innerHTML = '';
                    let category = document.createElement('p')
                    category.classList.add('category_level_1')
                    category.innerHTML += `
            <select class="input_field select_class_category" name="category" id="select_category_1">
                <option value="">---------</option>
                ${data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)}
            </select>

                `
                    event.target.parentElement.parentElement.append(category)
                    event.target.addEventListener('change', () => {
                        informationList.innerHTML = '';
                        if (document.querySelector('.category_level_1')) {
                            document.querySelector('.category_level_1').remove()
                        }
                        if (document.querySelector('.category_level_2')) {
                            document.querySelector('.category_level_2').remove()
                        }
                        if (document.querySelector('.category_level_3')) {
                            document.querySelector('.category_level_3').remove()
                        }
                    })
                })
        }
    }
    if (event.target === document.getElementById('select_category_1') && event.target.value !== statusCategory1) {
        statusCategory1 = event.target.value
        informationList.innerHTML = '';
        if (event.target.value !== '') {
            fetch(`http://127.0.0.1:8000/api/v1/get_category_list/?id=${event.target.value}`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.length !== 0) {
                        informationList.innerHTML = '';
                        let category = document.createElement('p')
                        category.classList.add('category_level_2')
                        category.innerHTML += `
            <select class="input_field select_class_category" name="category" id="select_category_2">
                <option value="">---------</option>
                ${data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)}
            </select>
                `
                        event.target.parentElement.parentElement.append(category)
                        event.target.addEventListener('change', () => {
                            informationList.innerHTML = '';
                            if (document.querySelector('.category_level_2')) {
                                document.querySelector('.category_level_2').remove()
                            }
                            if (document.querySelector('.category_level_3')) {
                                document.querySelector('.category_level_3').remove()
                            }
                        })
                    } else {
                        show_additional_information(event)
                    }

                })
        }
    }
    if (event.target === document.getElementById('select_category_2') && event.target.value !== statusCategory2) {
        statusCategory2 = event.target.value
        informationList.innerHTML = '';
        if (event.target.value !== '') {
            fetch(`http://127.0.0.1:8000/api/v1/get_category_list/?id=${event.target.value}`)
                .then((response) => response.json())

                .then((data) => {
                    if (data.length !== 0) {
                        informationList.innerHTML = '';
                        let category = document.createElement('p')
                        category.classList.add('category_level_3')
                        category.innerHTML += `
            <select class="input_field select_class_category" name="category" id="select_category_3">
                <option value="">---------</option>
                ${data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)}
            </select>
                `
                        event.target.parentElement.parentElement.append(category)
                        event.target.addEventListener('change', () => {
                            informationList.innerHTML = '';
                            if (document.querySelector('.category_level_3')) {
                                document.querySelector('.category_level_3').remove()
                            }
                        })
                    } else {
                        show_additional_information(event)
                    }
                })
        }
    }
    if (event.target === document.getElementById('select_category_3') && event.target.value !== statusCategory3) {
        statusCategory3 = event.target.value
        informationList.innerHTML = '';
        if (event.target.value !== '') {
            show_additional_information(event)
        }
    }
}

function show_additional_information(event) {
    fetch(`http://127.0.0.1:8000/api/v1/get_field_list/?id=${event.target.value}`)
        .then((response) => response.json())
        .then((data) => {
            informationList.innerHTML = '';
            for (let i of data) {
                if (i.spisok === null && i.min_val_interval_date === 0 && i.title !== 'Цена' && i.title !== 'Арендная плата') {
                    informationList.innerHTML += ` 
<div class="additional_information_item-${i.id}">
<div class="additional_information_item item_input">
<div class="information_label label_fields">
${i.title}
</div>
<div class="information_select">
<p class="information_item">
 <input class="information_item-input" id="information_${i.id}" type="text" name="${i.id}">
        </p>
</div>
</div> 
</div>
`
                } else if (i.min_val_interval_date !== 0) {
                    let minValDate = i.min_val_interval_date
                    const dateArray = []
                    dateArray.push(minValDate)
                    while (minValDate !== i.max_val_interval_date) {
                        minValDate = minValDate + 1
                        dateArray.push(minValDate)
                    }
                    informationList.innerHTML += `
<div class="additional_information_item-${i.id}">
<div class="additional_information_item item_input">
<div class="information_label label_fields">
${i.title}
</div>
<div class="information_select">
<p class="information_item">
            <select class="input_field select_class select_info" id="information_${i.id}" name="${i.id}">
                <option value="">---------</option>
                ${dateArray.map((elem) => `<option value=${elem}>${elem}</option>`)}
            </select>
        </p>
</div>
</div>
</div>
                    `
                } else if (i.title === 'Цена' || i.title === 'Арендная плата') {
                    informationList.innerHTML += ` 
<div class="additional_information_item-price">
<div class="additional_information_item item_input">
<div class="information_label label_fields">
${i.title} руб
</div>
<div class="information_select">
<p class="information_item">
 <input class="information_item-input price" id="information_${i.id}" type="text" name="${i.id}">
 <input class="information_item-input price-hidden" id="information_${i.title}" type="hidden" name="${i.title}">
        </p>
</div>
</div> 
</div>
`
                } else {

                    informationList.innerHTML += `
<div class="additional_information_item-${i.id}">
<div class="additional_information_item item_input">
<div class="information_label label_fields">
${i.title}
</div>
<div class="information_select">
<p class="information_item">
            <select class="input_field select_class select_info" id="information_${i.id}" name="${i.id}">
                <option value="">---------</option>
                ${i.spisok.element_set?.map((elem) => `<option value=${elem.title} data-elementtwo="${elem.id}">${elem.title}</option>`)}
            </select>
        </p>
</div>
</div>
</div>
                    `
                }
            }
        })
}


function showAdditionalInformationTwo(event) {
    if (event.target.className === "input_field select_class select_info" && event.target.value !== statusElementTwo) {
        statusElementTwo = event.target.value
        let elementtwo = ''
        for (let i of event.target.children) {
            if (i.value === event.target.value) {
                elementtwo = i.dataset.elementtwo
                break
            }
        }
        if (elementtwo) {
            fetch(`http://127.0.0.1:8000/api/v1/get_elementtwo_list/?slug=${elementtwo}`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.length > 0) {
                        if (document.querySelector('.information_item_two')) {
                            document.querySelector('.information_item_two').remove()
                        }
                        let elementP = document.createElement('p')
                        elementP.classList.add('information_item')
                        elementP.classList.add('information_item_two')
                        elementP.innerHTML += `
            <select class="input_field select_class select_info_two" id='element_two-${event.target.getAttribute('name')}' name="${event.target.getAttribute('name')}">
                <option value="">---------</option>
                ${data.map((elem) => `<option value=${elem.title}>${elem.title}</option>`)}
            </select>
                `
                        event.target.parentElement.parentElement.append(elementP)
                    }
                })
        } else if (event.target === document.querySelector('.information_item_two').parentElement.children[0].children[0]) {
            if (document.querySelector('.information_item_two')) {
                document.querySelector('.information_item_two').remove()
            }
        }
    }
}


const preview = document.querySelector('.photo_preview')
preview.addEventListener('click', removeImg)
const inputElement = document.getElementById("photo_list");
inputElement.addEventListener("change", handleFiles, false);
let inputElementArray = []
let mainImg = ""

function handleFiles() {
    const dt = new DataTransfer();
    const fileList = this.files;
    for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        if (!file.type.startsWith("image/")) {
            continue;
        }
        const img = document.createElement("img");
        img.classList.add("img_preview");
        if (i === 0) {
            img.classList.add("main_img");
            mainImg = img
        }
        img.file = file;
        img.setAttribute('name', fileList[i].name)
        img.setAttribute('data-id', i)
        const div = document.createElement("div")
        div.classList.add("photo_img")
        const div2 = document.createElement("div")
        div2.classList.add("delete_img")
        div2.setAttribute('data-name', fileList[i].name)
        div.append(div2)
        div.append(img);
        preview.append(div);

        const reader = new FileReader();
        reader.onload = (function (aImg) {
            return function (event) {
                aImg.src = event.target.result;
            };
        })(img);
        reader.readAsDataURL(file);
    }
    inputElementArray = Array.from(inputElement.files);
}

function removeImg(event) {
    const dt = new DataTransfer();
    let z = []
    let target = event.target

    if (target.classList.contains("delete_img")) {
        target.parentElement.remove()
        inputElementArray = inputElementArray.filter(file => file.name !== target.dataset.name);
        for (let i of inputElementArray) {
            dt.items.add(i)
        }
        z = dt.files
        inputElement.files = z
    }
    if (target.classList.contains("img_preview")) {
        if (mainImg) {
            mainImg.classList.remove("main_img")
        }
        target.classList.add("main_img")
        mainImg = target
    }
}

const addAdvForm = document.getElementById('add_adver')
const addAdvButton = document.querySelector('.add_adv')
addAdvButton.addEventListener('click', saveAdvertisement)

function saveAdvertisement() {
    if (document.querySelector('.price-hidden')) {
        document.querySelector('.price-hidden').value = document.querySelector('.price').value
    }
    let data = new FormData(addAdvForm);
    data.append("preview_img", mainImg.name)
    if (data.has("Цена")) {
        data.append("price", data.get("Цена"))
        data.delete("Цена")
    } else if (data.has("Арендная плата")) {
        data.append("price", data.get("Арендная плата"))
        data.delete("Арендная плата")
    }
    fetch(`http://127.0.0.1:8000/api/v1/save_advertisement/`, {
        method: "POST", headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        }, body: data,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error || data.error_additional) {
              const error = new Error('error')
                error.data = data
                throw error
            }
            document.location.href = 'http://127.0.0.1:8000/'}).catch( (msg) => {
           if (msg.data.error.title) {
                        if (document.querySelector('.title_error')) {
                            document.querySelector('.title_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('title_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.title} `
                        document.querySelector('.title_adver').append(errorText)
                        document.getElementById('title_input').classList.add('input_error')
                        document.getElementById('title_input').oninput = () => {
                            if (document.querySelector('.title_error')) {
                                document.querySelector('.title_error').remove()
                                document.getElementById('title_input').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.region) {
                        if (document.querySelector('.region_error')) {
                            document.querySelector('.region_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('region_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.region} `
                        document.querySelector('.region').append(errorText)
                        if (document.getElementById('select_city')) {
                            document.getElementById('select_city').classList.add('input_error')
                            document.getElementById('select_city').oninput = () => {
                                if (document.querySelector('.region_error')) {
                                    document.querySelector('.region_error').remove()
                                    document.getElementById('select_city').classList.remove('input_error')
                                }
                            }
                        } else {
                            document.getElementById('select_oblast').classList.add('input_error')
                            document.getElementById('select_oblast').oninput = () => {
                                if (document.querySelector('.region_error')) {
                                    document.querySelector('.region_error').remove()
                                    document.getElementById('select_oblast').classList.remove('input_error')
                                }
                            }
                        }
                    }
                    if (msg.data.error.category) {
                        if (document.querySelector('.category_error')) {
                            document.querySelector('.category_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('category_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.category} `
                        document.querySelector('.category').append(errorText)
                        if (document.getElementById('select_category_3')) {
                            document.getElementById('select_category_3').classList.add('input_error')
                            document.getElementById('select_category_3').oninput = () => {
                                if (document.querySelector('.category_error')) {
                                    document.querySelector('.category_error').remove()
                                    document.getElementById('select_category_3').classList.remove('input_error')
                                }
                            }
                        } else if (document.getElementById('select_category_2')) {
                            document.getElementById('select_category_2').classList.add('input_error')
                            document.getElementById('select_category_2').oninput = () => {
                                if (document.querySelector('.category_error')) {
                                    document.querySelector('.category_error').remove()
                                    document.getElementById('select_category_2').classList.remove('input_error')
                                }
                            }
                        } else if (document.getElementById('select_category_1')) {
                            document.getElementById('select_category_1').classList.add('input_error')
                            document.getElementById('select_category_1').oninput = () => {
                                if (document.querySelector('.category_error')) {
                                    document.querySelector('.category_error').remove()
                                    document.getElementById('select_category_1').classList.remove('input_error')
                                }
                            }
                        } else if (document.getElementById('select_category_0')) {
                            document.getElementById('select_category_0').classList.add('input_error')
                            document.getElementById('select_category_0').oninput = () => {
                                if (document.querySelector('.category_error')) {
                                    document.querySelector('.category_error').remove()
                                    document.getElementById('select_category_0').classList.remove('input_error')
                                }
                            }
                        }
                    }
                    if (msg.data.error.description) {
                        if (document.querySelector('.description_error')) {
                            document.querySelector('.description_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('description_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.description} `
                        document.querySelector('.description').append(errorText)
                        document.getElementById('description').classList.add('input_error')
                        document.getElementById('description').oninput = () => {
                            if (document.querySelector('.description_error')) {
                                document.querySelector('.description_error').remove()
                                document.getElementById('description').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.bearer) {
                        if (document.querySelector('.bearer_error')) {
                            document.querySelector('.bearer_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('bearer_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.bearer} `
                        document.querySelector('.bearer').append(errorText)
                        for (let i of document.querySelectorAll('.custom_radio')) {
                            i.classList.add('radio_error')
                        }
                        document.getElementById('bearer_private_person').oninput = () => {
                            if (document.querySelector('.bearer_error')) {
                                document.querySelector('.bearer_error').remove()
                                for (let i of document.querySelectorAll('.custom_radio')) {
                                    i.classList.remove('radio_error')
                                }
                            }

                        }
                        document.getElementById('bearer_company').oninput = () => {
                            if (document.querySelector('.bearer_error')) {
                                document.querySelector('.bearer_error').remove()
                                for (let i of document.querySelectorAll('.custom_radio')) {
                                    i.classList.remove('radio_error')
                                }
                            }
                        }
                    }
                    if (msg.data.error.contact_name) {
                        if (document.querySelector('.contact_error')) {
                            document.querySelector('.contact_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('contact_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.contact_name} `
                        document.querySelector('.contact_information').append(errorText)
                        document.getElementById('contact').classList.add('input_error')
                        document.getElementById('contact').oninput = () => {
                            if (document.querySelector('.contact_error')) {
                                document.querySelector('.contact_error').remove()
                                document.getElementById('contact').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.email) {
                        if (document.querySelector('.email_error')) {
                            document.querySelector('.email_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('email_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.email} `
                        document.querySelector('.email_information').append(errorText)
                        document.getElementById('email').classList.add('input_error')
                        document.getElementById('email').oninput = () => {
                            if (document.querySelector('.email_error')) {
                                document.querySelector('.email_error').remove()
                                document.getElementById('email').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.phone_num) {
                        if (document.querySelector('.phone_error')) {
                            document.querySelector('.phone_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('phone_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.phone_num} `
                        document.querySelector('.phone_information').append(errorText)
                        document.getElementById('phone').classList.add('input_error')
                        document.getElementById('phone').oninput = () => {
                            if (document.querySelector('.phone_error')) {
                                document.querySelector('.phone_error').remove()
                                document.getElementById('phone').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.store) {
                        if (document.querySelector('.store_error')) {
                            document.querySelector('.store_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('store_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.store} `
                        document.querySelector('.bearer_company_store').append(errorText)
                        document.getElementById('select_store').classList.add('input_error')
                        document.getElementById('select_store').oninput = () => {
                            if (document.querySelector('.store_error')) {
                                document.querySelector('.store_error').remove()
                                document.getElementById('select_store').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error.price) {
                        if (document.querySelector('.price_error')) {
                            document.querySelector('.price_error').remove()
                        }
                        const errorText = document.createElement('p')
                        errorText.classList.add('price_error')
                        errorText.classList.add('error')
                        errorText.innerHTML = `${msg.data.error.price} `
                        document.querySelector('.additional_information_item-price').append(errorText)
                        document.querySelector('.price').classList.add('input_error')
                        document.querySelector('.price').oninput = () => {
                            if (document.querySelector('.price_error')) {
                                document.querySelector('.price_error').remove()
                                document.querySelector('.price').classList.remove('input_error')
                            }
                        }
                    }
                    if (msg.data.error_additional) {
                        for (let i of msg.data.error_additional) {
                            if (document.querySelector(`.additional_${i.id}_error`)) {
                                document.querySelector(`.additional_${i.id}_error`).remove()
                            }
                            const errorText = document.createElement('p')
                            errorText.classList.add(`additional_${i.id}_error`)
                            errorText.classList.add('error')
                            errorText.innerHTML = `${i.error} `
                            document.querySelector(`.additional_information_item-${i.id}`).append(errorText)
                            document.getElementById(`information_${i.id}`).classList.add('input_error')
                            if (document.getElementById(`element_two-${i.id}`)) {
                                document.getElementById(`element_two-${i.id}`).classList.add('input_error')
                                document.getElementById(`element_two-${i.id}`).oninput = () => {
                                    if (document.querySelector(`.additional_${i.id}_error`)) {
                                        document.querySelector(`.additional_${i.id}_error`).remove()
                                        document.getElementById(`information_${i.id}`).classList.remove('input_error')
                                        document.getElementById(`element_two-${i.id}`).classList.remove('input_error')
                                    }
                                }
                            }
                            document.getElementById(`information_${i.id}`).oninput = () => {
                                if (document.querySelector(`.additional_${i.id}_error`)) {
                                    document.querySelector(`.additional_${i.id}_error`).remove()
                                    document.getElementById(`information_${i.id}`).classList.remove('input_error')
                                }
                            }

                        }
                    }
    })

}

const bearerCompany = document.querySelector('.description_radio')
bearerCompany.addEventListener('click', bearerCompanyInfo)

function bearerCompanyInfo(event) {
    if (event.target.id === 'bearer_company') {
        if (!document.querySelector('.bearer_company_store')) {
            fetch`http://127.0.0.1:8000/api/v1/get_store_for_advertisement/`
                .then((response) => response.json())
                .then(data => {
                    const bearerCompanyStore = document.createElement('div')
                    bearerCompanyStore.classList.add('bearer_company_store')
                    bearerCompanyStore.innerHTML = `
                    <div class="store_input item_input">
                        <p class="store_label label_fields">
                        Магазин
                        </p>
                    <div class="store_select">
                        <p class="bearer_store">
                            <select class="input_field" name="store" id="select_store">
                                <option value="">---------</option>
                                ${data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)}
                            </select>
                        </p>
                    </div>
                </div>`
                    const bearerCompanyVendorCode = document.createElement('div')
                    bearerCompanyVendorCode.classList.add('bearer_company_vendor_code')
                    bearerCompanyVendorCode.innerHTML = `
        <div class="vendor_code_input item_input">
                        <p class="vendor_code_label label_fields">Артикул</p>
                        <input type="text" name="article" id="article" class="information_item-input">
                    </div>
        `
                    document.querySelector('.bearer_company_additional_info').append(bearerCompanyStore)
                    document.querySelector('.bearer_company_additional_info').append(bearerCompanyVendorCode)
                })
        }
    } else if (event.target.id === 'bearer_private_person') {
        document.querySelector('.bearer_company_additional_info').innerHTML = ''
    }
}
