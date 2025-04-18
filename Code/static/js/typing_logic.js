document.addEventListener('keydown', function (event) {
    let keyPressed = event.key;

    if (["Shift", "Alt", "Control", "Meta"].includes(keyPressed)) {
        return;
    }

    let input = document.getElementById('input');

    if (keyPressed === "Backspace") {
        input.textContent = input.textContent.slice(0, -1);
    } else if (keyPressed === "Enter") {
        input.textContent += '\n';
        
    } else if (/^[a-zA-Z0-9`~!@#$%^&*()_+-={}\[\]|\\:;"'<>,.?\/ ]$/.test(keyPressed)) {
        input.textContent += keyPressed;
    }
});