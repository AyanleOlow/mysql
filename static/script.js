/* Her kan du putte JavaScript :) */
const pages = {
    index: "/index",
    about: "/about"
}

function switchPage(page) {
    window.location.href = pages[page]
}