const parentElement = document.querySelector('section.wrapper').parentElement;
parentElement.addEventListener('click', apiView);

async function apiView(event) {
    const element = event.target;

    if (!element.classList.contains('hybrid'))
        return;

    event.preventDefault();
    const elementHref = element.href;
    const template = await (await fetch(elementHref)).text();
    parentElement.innerHTML = template;
}
