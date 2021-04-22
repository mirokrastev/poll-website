async function getPercentView() {
    const answers = await(await fetch('?ajax=true')).json();
    [...document.querySelector('#id_answers').children]
        .forEach(e => {
            const key = e.querySelector('[name=answers]').nextSibling.textContent.slice(2);
            const answer = answers[key];
            const word = answer[0] === 1 ? 'Vote' : 'Votes';

            const spanEl = document.createElement('span');
            spanEl.className = 'info';
            spanEl.textContent = ` (${answer[0]} ${word} - ${answer[1].toFixed(2)}%)`;

            const lastEl = e.lastElementChild;
            if (lastEl.tagName === 'SPAN' || lastEl.classList.contains('info')) {
                lastEl.remove();
            }

            e.append(spanEl);

        }, 0)
}

document.querySelector('#percent')
    .addEventListener('click', getPercentView);
