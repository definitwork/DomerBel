const region_opened = document.querySelector(".region_opened");
region_opened.addEventListener('click', show_city);
const get_element_select_city = document.querySelector("#select_city");
const get_element_select_oblast = document.querySelector("#select_oblast");
const get_element_select_category_0 = document.querySelector("#select_category_0");
const region_hidden = document.querySelector(".region_hidden")
const category_select = document.querySelector(".category_select");
category_select.addEventListener('click', show_category)
const get_element_select_category_1 = document.querySelector("#select_category_1");
const get_element_select_category_2 = document.querySelector("#select_category_2");
const get_element_select_category_3 = document.querySelector("#select_category_3");
let status_category_0 = ''
let status_category_1 = ''
let status_category_2 = ''
let status_category_3 = ''
const information_list = document.querySelector(".additional_information");
information_list.addEventListener('click', show_additional_information)
let status_element_two = ''


function show_oblast() {
    fetch(`http://127.0.0.1:8000/api/v1/get_region_list/`)
        .then((response) => response.json())
        .then(data => {
            let array = data.filter(function (i) {
                return i.level === 0
            })
            // get_element_select_city.innerHTML = `<option value="0">---------</option>`
            get_element_select_oblast.innerHTML += array.map((elem) => `<option value=${elem.id}>${elem.area}</option>`)
        })
}

show_oblast()


function show_city(event) {
    if (event.target.value !== "0") {
        fetch(`http://127.0.0.1:8000/api/v1/add_store/city/${event.target.value}`)
            .then((response) => response.json())
            .then(data => {
                region_hidden.style.display = "flex";
                get_element_select_city.innerHTML = `<option value="0">---------</option>`
                get_element_select_city.innerHTML += data.map((elem) => `<option value=${elem.id}>${elem.area}</option>`)
            })
    } else {
        get_element_select_city.innerHTML += "";
        region_hidden.style.display = "none";
    }
}


// let get_category = document.querySelector("#select_category");

fetch("http://127.0.0.1:8000/api/v1/add_store/categories/")
    .then((response) => response.json())
    .then((data) => {
        let array = data.filter(function (i) {
            return i.level === 0
        })
        get_element_select_category_0.innerHTML += array.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)

    })

function show_category(event) {
    if (event.target === get_element_select_category_0 && event.target.value !== '0' && event.target.value !== status_category_0) {
        status_category_0 = event.target.value
        fetch(`http://127.0.0.1:8000/api/v1/get_category_list/${event.target.value}`)
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                get_element_select_category_1.style.display = "flex";
                get_element_select_category_1.innerHTML = `<option value="0">---------</option>`
                get_element_select_category_1.innerHTML += data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)
                event.target.addEventListener('change', () => {
                    get_element_select_category_1.innerHTML = ''
                    get_element_select_category_2.innerHTML = ''
                    get_element_select_category_2.style.display = "none";
                    get_element_select_category_3.innerHTML = ''
                    get_element_select_category_3.style.display = "none";
                    information_list.innerHTML = '';

                })
            })
    }
    if (event.target === get_element_select_category_1 && event.target.value !== '0' && event.target.value !== status_category_1) {
        status_category_1 = event.target.value
        fetch(`http://127.0.0.1:8000/api/v1/get_category_list/${event.target.value}`)
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                if (data.length !== 0) {
                    get_element_select_category_2.style.display = "flex";
                    get_element_select_category_2.innerHTML = `<option value="0">---------</option>`
                    get_element_select_category_2.innerHTML += data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)
                    event.target.addEventListener('change', () => {
                        get_element_select_category_2.innerHTML = ''
                        get_element_select_category_3.innerHTML = ''
                        get_element_select_category_3.style.display = "none";
                        information_list.innerHTML = '';

                    })
                } else {
                    fetch(`http://127.0.0.1:8000/api/v1/get_field_list/${event.target.value}`)
                        .then((response) => response.json())
                        .then((data) => {
                            console.log('johan', data)
                            information_list.innerHTML = '';
                            for (let i of data) {
                                console.log(i)
                                if (i.spisok === null) {
                                    information_list.innerHTML += ` 
 <div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
 <input class="information_item-input" type="text" name="${i.title}">
        </p>
</div>

</div> 
`
                                } else {

                                    information_list.innerHTML += `
<div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
            <select class="input_field select_class select_info" id="information_${i.id}" name="${i.title}" style="margin-top: 5px;">
                <option value="0">---------</option>
                ${i.spisok.element_set?.map((elem) => `<option value=${elem.title} data-elementtwo="${elem.id}">${elem.title}</option>`)}
            </select>
        </p>
</div>

</div>
                    `
                                }
                            }
                        })
                }

            })
    }
    if (event.target === get_element_select_category_2 && event.target.value !== '0' && event.target.value !== status_category_2) {
        status_category_2 = event.target.value
        fetch(`http://127.0.0.1:8000/api/v1/get_category_list/${event.target.value}`)
            .then((response) => response.json())

            .then((data) => {
                console.log(data)
                if (data.length !== 0) {
                    get_element_select_category_3.style.display = "flex";
                    get_element_select_category_3.innerHTML = `<option value="0">---------</option>`
                    get_element_select_category_3.innerHTML += data.map((elem) => `<option value=${elem.id}>${elem.title}</option>`)
                    event.target.addEventListener('change', () => {
                        get_element_select_category_3.innerHTML = ''
                        information_list.innerHTML = '';

                    })
                } else {
                    fetch(`http://127.0.0.1:8000/api/v1/get_field_list/${event.target.value}`)
                        .then((response) => response.json())
                        .then((data) => {
                            console.log('johan', data)
                            information_list.innerHTML = '';
                            for (let i of data) {
                                console.log(i)
                                if (i.spisok === null) {
                                    information_list.innerHTML += ` <div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
 <input class="information_item-input" type="text" name="${i.title}">
        </p>
</div>

</div> `
                                } else {

                                    information_list.innerHTML += `
<div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
            <select class="input_field select_class select_info" id="information_${i.id}" name="${i.title}" style="margin-top: 5px;">
                <option value="0">---------</option>
                ${i.spisok.element_set?.map((elem) => `<option value=${elem.title} data-elementtwo="${elem.id}">${elem.title}</option>`)}
            </select>
        </p>
</div>

</div>
                    `
                                }
                            }
                        })
                }
            })
    }
    if (event.target === get_element_select_category_3 && event.target.value !== '0' && event.target.value !== status_category_2) {
        status_category_3 = event.target.value
        fetch(`http://127.0.0.1:8000/api/v1/get_field_list/${event.target.value}`)
            .then((response) => response.json())
            .then((data) => {
                console.log('johan', data)
                information_list.innerHTML = '';
                for (let i of data) {
                    console.log(i)
                    if (i.spisok === null) {
                        information_list.innerHTML += ` <div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
 <input class="information_item-input" type="text" name="${i.title}">
        </p>
</div>

</div> `
                    } else {

                        information_list.innerHTML += `
<div class="" style="display: flex;">
<div class="information_label label_fields">${i.title}</div>
<div class="information_select">
<p class="information_item">
            <select class="input_field select_class select_info" id="information_${i.id}" name="${i.title}" style="margin-top: 5px;">
                <option value="0">---------</option>
                ${i.spisok.element_set?.map((elem) => `<option value=${elem.title} data-elementtwo="${elem.id}">${elem.title}</option>`)}
            </select>
        </p>
</div>

</div>

                    
                    `
                    }
                }
            })
    }
}



function show_additional_information(event) {
    if (event.target.className === "input_field select_class select_info" && event.target.value !== evTarg){
        status_element_two = event.target.value
        let elementtwo = ''
        for (let i of event.target.children){
            if (i.value === event.target.value) {
                elementtwo = i.dataset.elementtwo
                break
            }
        }
        if (elementtwo) {

        fetch(`http://127.0.0.1:8000/api/v1/get_elementtwo_list/${elementtwo}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.length > 0) {
                    if(document.querySelector('.information_item_two')){
                        document.querySelector('.information_item_two').remove()
                    }
                   let z = document.createElement('p')
                       z.classList.add('information_item')
                       z.classList.add('information_item_two')

                    z.innerHTML += `
            <select class="input_field select_class select_info_two" name="${event.target.getAttribute('name')}" style="margin-top: 5px;">
                <option value="0">---------</option>
                ${data.map((elem) => `<option value=${elem.title}>${elem.title}</option>`)}
            </select>

                `
                    event.target.parentElement.parentElement.append(z)
                }

            })
        }

    }

}


const preview = document.querySelector('.photo_preview')
preview.addEventListener('click', remove_img)
let inputElement = document.querySelector("#photo_list");
inputElement.addEventListener("change", handleFiles, false);
let inputElementArray = []
let main_img = ""

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
        if (i === 0){
            img.classList.add("main_img");
            main_img = img
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



function remove_img (event) {
    const dt = new DataTransfer();
    let z = []
    let target = event.target

    if (target.classList.contains("delete_img")){
        target.parentElement.remove()
        inputElementArray = inputElementArray.filter(file => file.name !== target.dataset.name);
        for (let i of inputElementArray) {
            dt.items.add(i)
            console.log(i)
        }
        z = dt.files
        inputElement.files = z
    }

    if (target.classList.contains("img_preview")) {
        if (main_img) {
            main_img.classList.remove("main_img")
        }
        target.classList.add("main_img")
        main_img = target
    }
}

const addAdver = document.querySelector('#add_adver')
const addAdvButton = document.querySelector('.add_adv')
addAdvButton.addEventListener('click', save_advertisement)

function save_advertisement() {
    let data = new FormData(addAdver);
    data.append("preview_img", main_img.name)
    fetch(`http://127.0.0.1:8000/api/v1/save_advertisement/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: data,
    })
    for (let i of data){
        // console.log(i)
        }
    console.log(main_img)
}

