let wordElement = document.getElementById('word');
let UserInput = document.getElementById('input');
let start = document.getElementById('start');
start.innerHTML = "Start typing!";
start.setAttribute("class", "start");
let end = document.getElementById('end');
let startingMs = 0;
let startingMs2 = 0;
// let showTimer = document.getElementById("timer");
let showTimer2 = document.getElementById("timer2");
let bool = false;
let interval;
let interval2;
let showWpm = document.getElementById("wpm");
let accuracy = document.getElementById("accuracy");
let accuracy_stats = document.getElementById("accuracy_stats");

let string = document.getElementById("text").textContent;
console.log(string);
// let container = document.getElementById('word-data-container');
// let string = container.dataset.words.trim();
// console.log(string);

let stringLength = string.length;






function Spans(textToDisplay) {
    for (let i = 0; i < textToDisplay.length; i++) {
        let charSpan = document.createElement("span");
        charSpan.textContent = textToDisplay[i];
        wordElement.appendChild(charSpan);
    }
}


// Initial population of the #word
Spans(string);

chars_total = string.length;

// Outside the handler:
let prevValue = "";     // track the last input to detect deletions
let typing_errors = [];     // flat list of error indices, if you still need it
let errorEvents = [];     // detailed log of each mistyped keystroke
let letterSpans = wordElement.children;

// Your oninput handler:
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

                // Only log if this keystroke just introduced a new mismatch here
                // (i.e. previous value either didn't have this char or was correct)
                if (prevValue[i] !== UserStr[i]) {
                    typing_errors.push(i);
                    errorEvents.push({
                        index: i,
                        typedChar: UserStr[i],
                        expectedChar: string[i],
                        timestamp: new Date().toLocaleTimeString()
                    });
                }
            }
        } else {
            span.classList.remove("green_letter", "red_letter");
        }
    }

    // 4) (Optional) push a snapshot of current errors if you need history
    // typing_errors.push([...typing_errors_current]);

    // Zazna konec tipkanja
    if (UserStr.length === string.length) {
        clearInterval(interval2);
        completed(UserInput);
    }

    // Updejta preValue*_:
    prevValue = UserStr;
};


function chars_right() {
    let chars_right_int = 0;
    for (let i = 0; i < string.length; i++) {
        let span = letterSpans[i];
        if (span.className === "green_letter"){
            chars_right_int ++;
        }
    }
    return chars_right_int;
}
// Optional: Logic for when typedValue is longer than string (e.g., allow typing extra chars)
// The current loop only styles up to string.length.
// If you want to show extra typed characters as red, you might need to append new spans dynamically
// or have a separate area, but that's beyond the scope of fixing the current logic.


// Optional: Handle if user types more characters than the original string
// The loop above only styles spans up to the length of the original 'string'.
// You might want to add specific behavior if typedValue.length > string.length.


// Accuracy (%) = (Total Correct Characters / (Total Correct Characters + Total Incorrect Characters + Total Extra Characters)) * 100


function completed(UserInput) {
    chars_wrong = typing_errors.length;
    let right = chars_right();
    final_accuracy = Math.floor((right / (right + chars_wrong) * 100), 1);
    // accuracy.innerHTML = "Total: " + chars_total + "     Right:" + right + "     Wrong:" + chars_wrong;
    accuracy_stats.innerHTML = final_accuracy + "%";
    end.innerHTML = "You finished!";
    end.setAttribute("class", "end");
    console.log(typing_errors);
    console.log(string.length);
    // clearInterval(interval);
    clearInterval(interval2);
    calculateWPM(stringLength, startingMs2 * 10);
    // showTimer.innerHTML = "Final time: " + startingMs + " seconds";
    showTimer2.innerHTML = "Final time: " + startingMs2 / 100 + " seconds";
    UserInput.readOnly = true;
    onLessonComplete();
}



function calculateWPM(charactersTyped, timeMs) {
    let wpm = Math.round((charactersTyped * 60000) / (5 * timeMs));
    showWpm.innerHTML = "Your wpm: " + wpm;
}




// function updateTimer() { // works perfectly fine
//     startingMs++;
//     showTimer.innerHTML = "Time: " + startingMs + " seconds";
// };


function updateTimer2() { // works perfectly fine
    startingMs2++;
    showTimer2.innerHTML = "Time: " + startingMs2 * 10 + "milliseconds";
};


function reset() { // lahk tud nardis da reseta use variable - to je tud fine for now
    window.location.reload();
};