import {html, render} from 'https://unpkg.com/lit-html?module';

const main = document.getElementById('results');

function template(answers) {
}

async function getPercentView() {
    const answers = await(await fetch('?ajax=true')).json();
    console.log(answers);
    // TODO: Implement to show percentages...
}

document.querySelector('#percent')
    .addEventListener('click', getPercentView);
