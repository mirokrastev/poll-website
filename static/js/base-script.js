document.querySelector('#homeLink')
.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo(0, 0);
});

document.getElementById('logout-anchor')
.addEventListener('click', (e) => {
    e.preventDefault();
    e.target.parentElement.submit();
});
