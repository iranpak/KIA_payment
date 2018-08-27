inputs = document.getElementsByTagName('input');
textAreas = document.getElementsByTagName('textarea');

for (let i = 0; i < inputs.length; i++) {
    inputs[i].classList.add('form-control');
}

for (let i = 0; i < textAreas.length; i++) {
    textAreas[i].classList.add('form-control');
}