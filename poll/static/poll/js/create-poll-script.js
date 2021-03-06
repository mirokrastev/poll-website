const formField = document.getElementById('fields');
let answerForms = formField.querySelectorAll('input[type=text]').length
const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
const maxAllowedForms = Number(document.querySelector('#id_form-MAX_NUM_FORMS').value);
const formRegex = /form-(\d)-/g;

document.getElementById('add-form-btn')
    .addEventListener('click', (e) => {
        e.preventDefault();

        if (answerForms >= maxAllowedForms)
            return alert(`The maximum number of answers is ${maxAllowedForms}`);

        const newLabel = formField.children[0].cloneNode(true);
        const newForm = formField.children[1].cloneNode(true);
        const newHiddenInput = formField.children[2].cloneNode(true);

        const fragment = document.createDocumentFragment();
        fragment.appendChild(document.createElement('br'));
        fragment.appendChild(newLabel);
        fragment.appendChild(newForm);
        fragment.appendChild(newHiddenInput);

        formField.appendChild(fragment);

        newLabel.outerHTML = newLabel.outerHTML.replace(formRegex, `form-${answerForms}-`)
        newForm.outerHTML = newForm.outerHTML.replace(formRegex, `form-${answerForms}-`);
        newHiddenInput.outerHTML = newHiddenInput.outerHTML.replace(formRegex, `form-${answerForms}-`);

        totalForms.value = ++answerForms;
    })