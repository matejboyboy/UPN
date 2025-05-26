let wordElement = document.getElementById('word');
let UserInput = document.getElementById('input');
let start = document.getElementById('start');
start.innerHTML = "Start typing!";
start.setAttribute("class", "start");
let end = document.getElementById('end');
let startingMs = 0;
let startingMs2 = 0;
let showTimer2 = document.getElementById("timer2");
let bool = false;
let interval;
let interval2;
let showWpm = document.getElementById("wpm");
let accuracy = document.getElementById("accuracy");
let accuracy_stats = document.getElementById("accuracy_stats");
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
let errorEvents = []; // list za shranjevanje dogodkov napak.
let letterSpans = wordElement.children;

window.updateCursorPosition = function (currentIndex) {
    if (document.activeElement === UserInput) {
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
}
if (string.length > 0) {
    updateCursorPosition(0);
}

UserInput.oninput = function () {
    let UserStr = UserInput.value;
    // Zacne timer ko je prva tipka pritisnjena
    if (UserStr.length > 0 && !bool) {
        bool = true;
        interval2 = setInterval(updateTimer2, 10);
        start.remove();
    }
    // Ignorira backspace saj se premikamo nazaj v stringu
    if (UserStr.length < prevValue.length) {
        for (let i = UserStr.length; i < string.length; i++) {
            letterSpans[i].classList.remove("green_letter", "red_letter");
        }
        prevValue = UserStr;
        return;
    }
    // Primerjava tipk med seboj
    for (let i = 0; i < string.length; i++) {
        let span = letterSpans[i];
        if (i < UserStr.length) {
            if (UserStr[i] === string[i]) {
                span.className = "green_letter";
            } else {
                span.className = "red_letter";
                if (prevValue[i] !== UserStr[i]) {
                    typing_errors.push(i);
                    // errorEvents.push({
                    //     index: i,
                    //     typedChar: UserStr[i],
                    //     expectedChar: string[i],
                    //     timestamp: new Date().toLocaleTimeString()
                    // });
                }
            }
        } else {
            span.classList.remove("green_letter", "red_letter");
        }
    }
    // Zazna konec tipkanja
    if (UserStr.length === string.length) {
        clearInterval(interval2);
        completed(UserInput);
    }
    // Updejta preValue*_:
    prevValue = UserStr;
};
// isto kt v typing_animation.js
function chars_right() {
    let chars_right_int = 0;
    for (let i = 0; i < string.length; i++) {
        let span = letterSpans[i];
        if (span.className === "green_letter") {
            chars_right_int++;
        }
    }
    return chars_right_int;
}

// Accuracy (%) = (Total Correct Characters / (Total Correct Characters + Total Incorrect Characters + Total Extra Characters)) * 100

function completed(UserInput) {
    chars_wrong = typing_errors.length;
    let right = chars_right();
    final_accuracy = Math.floor((right / (right + chars_wrong) * 100), 1);
    accuracy_stats.innerHTML = final_accuracy + "%";
    end.innerHTML = "You finished!";
    end.setAttribute("class", "end");
    console.log(typing_errors);
    console.log(string.length);
    clearInterval(interval2);
    calculateWPM(stringLength, startingMs2 * 10);
    showTimer2.innerHTML = "Final time: " + startingMs2 / 100 + " seconds";
    UserInput.readOnly = true;
    onLessonComplete();
}

function calculateWPM(charactersTyped, timeMs) {
    let wpm = Math.round((charactersTyped * 60000) / (5 * timeMs));
    showWpm.innerHTML = "Your wpm: " + wpm;
}

function updateTimer2() {
    startingMs2++;
    showTimer2.innerHTML = "Time: " + startingMs2 * 10 + "milliseconds";
};

function reset() {
    window.location.reload();
};
