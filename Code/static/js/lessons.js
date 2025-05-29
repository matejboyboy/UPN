let wordElement = document.getElementById('word');
let UserInput = document.getElementById('input');
let start = document.getElementById('start');
start.innerHTML = "Start typing!";
start.setAttribute("class", "start");
let end = document.getElementById('end');
let string = document.getElementById("text").textContent;
console.log(string);

let stringLength = string.length;

function Spans(textToDisplay) {
    for (let i = 0; i < textToDisplay.length; i++) {
        let charSpan = document.createElement("span");
        charSpan.textContent = textToDisplay[i];
        wordElement.appendChild(charSpan);
    }
}

Spans(string);

chars_total = string.length;

let prevValue = ""; // shrani prejsnjo vrednost inputa.
let typing_errors = []; // list za shranjevanje indeksov napak.
let letterSpans = wordElement.children;

window.updateCursorPosition = function (currentIndex) {
    for (let i = 0; i < letterSpans.length; i++) {
        letterSpans[i].classList.remove('cursor');
    }
    if (currentIndex < letterSpans.length) {
        letterSpans[currentIndex].classList.add('cursor');
        wordElement.children[currentIndex].scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'nearest'
        });
    }
}
if (string.length > 0) {
    updateCursorPosition(0);
}

UserInput.oninput = function () {
    let UserStr = UserInput.value;
    // Zacne timer ko je prva tipka pritisnjena
    if (UserStr.length > 0 && !start.classList.contains('hide')) {
        start.classList.add('hide');
    }
    // Ignorira backspace saj se premikamo nazaj v stringu
    if (UserStr.length < prevValue.length) {
        for (let i = UserStr.length; i < string.length; i++) {
            letterSpans[i].classList.remove("green_letter", "red_letter", "missed_space");
        }
        prevValue = UserStr;
        updateCursorPosition(UserStr.length);
        return;
    }
    // Primerjava tipk med seboj
    for (let i = 0; i < string.length; i++) {
        let span = letterSpans[i];
        if (i < UserStr.length) {
            if (UserStr[i] === string[i]) {
                span.className = "green_letter";
            } else {
                if (string[i] === ' ') {
                    span.className = 'missed_space'; // Highlight missed spaces with red background
                } else {
                    span.className = 'red_letter';
                }
                if (prevValue[i] !== UserStr[i]) {
                    typing_errors.push(i);
                }
            }
        } else {
            span.classList.remove("green_letter", "red_letter", "missed_space");
        }
    }
    // Zazna konec tipkanja
    updateCursorPosition(UserStr.length);
    if (UserStr.length === string.length) {
        completed(UserInput);
    }
    // Updejta preValue*_:
    prevValue = UserStr;
};

function completed(UserInput) {
    end.innerHTML = "You finished!"; // Show completion message
    end.classList.remove('hide'); // Make end message visible
    console.log(typing_errors);
    console.log(string.length);
    UserInput.readOnly = true;
    // Hide only the main typing area including the input bar
    document.getElementById('main').classList.add('hide');
    onLessonComplete();
}

function reset() {
    window.location.reload();
};

// Define onLessonComplete to save lesson completion
function onLessonComplete() {
    fetch(`/complete_lesson/${window.lessonNumber}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Lesson completed');
            } else {
                console.error('Error completing lesson');
            }
        })
        .catch(error => console.error('Error:', error));
}