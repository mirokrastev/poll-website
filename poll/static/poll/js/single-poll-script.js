let hasRequested = false;
// TODO: ON REQUEST CHANGE!
async function getPercentView() {
    if (hasRequested) return;
    hasRequested = true;

    const answers = await(await fetch('?ajax=true')).json();
    [...document.querySelector('#id_answers').children]
        .forEach(e => {
            const children = e.children[0];
            const key = e.textContent.trim();
            const answer = answers[key];
            const word = answer[0] === 1 ? 'Vote' : 'Votes';
            children.innerHTML += ` (${answer[0]} ${word} - ${answer[1].toFixed(2)}%)`
        }, 0)
}

document.querySelector('#percent')
    .addEventListener('click', getPercentView);
