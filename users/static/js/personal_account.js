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