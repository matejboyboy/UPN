document.addEventListener('keydown', function (event) {
    let keyPressed = event.key;

    if (["Shift", "Alt", "Control"].includes(keyPressed)) {
        return;
    }

    let input = document.getElementById('input');

    if (keyPressed === "Backspace") {
        input.textContent = input.textContent.slice(0, -1);
    } else if (keyPressed === "Enter") {
        input.textContent += '\n';
    } else if (keyPressed.length === 1) {
    input.textContent += keyPressed;
    }
});