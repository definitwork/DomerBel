const more = document.querySelector(".description_more_button");
const more_popup = document.querySelector(".description_feedback_share_list_modal");



more.addEventListener("click", (event) => {
    if (event.currentTarget.classList.contains("description_more_button")) {
        more_popup.style.display = "flex";
    }
});

document.addEventListener("click", (event) => {

    if (event.target.classList.contains('description_feedback_share_list_modal')
        || event.target.classList.contains('description_feedback_share_list_item_modal')
        || event.target.tagName === "svg" || event.target.tagName === "path") {
    return
    }
    more_popup.style.display = "none";
})

    // console.log(event.target.tagName !== "svg" || event.target.tagName !== "path")
    // console.log(event.target.classList.contains("description_feedback_share_list_modal")
    //     ||
    //     event.target.classList.contains("description_feedback_share_list_item_modal")
    //     ||
    //     event.target.tagName !== "svg" || event.target.tagName !== "path")
    // // more_popup.style.display = "none";
    // if (!event.target.classList.contains("description_feedback_share_list_modal")
    //     ||
    //     !event.target.classList.contains("description_feedback_share_list_item_modal")
    //     ||
    //     event.target.tagName !== "svg" || event.target.tagName !== "path"
    // ) {
    //     console.log(222)
    //     more_popup.style.display = "none";
    // }