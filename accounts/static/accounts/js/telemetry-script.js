document.querySelector('.wrapper').parentElement
    .addEventListener('click', checkElement);


function checkElement(e) {
    const element = e.target;

    if (element.name !== 'telemetry') return;
    element.form.submit();
}