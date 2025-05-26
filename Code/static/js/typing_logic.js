let counter = 0;
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
    } else if (keyPressed === "CapsLock") {
        counter++;
        let CapsLock = document.getElementById('CapsLockWarning');
        if (counter % 2 === 0) {
            CapsLock.className = 'hide';
        } else {
            CapsLock.classList.remove("hide");
            CapsLock.textContent = 'CAPS LOCK';
        }
    }
});

let CapsLock = document.getElementById('CapsLockWarning');

function CapsLockCheck(event) {
    if (event.getModifierState('CapsLock')) {
        CapsLock.classList.remove("hide");
        CapsLock.textContent = 'CAPS LOCK';
    } else {
        CapsLock.className = 'hide';
    }
}

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
    CapsLockCheck(event);
});
