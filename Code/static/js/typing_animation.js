


function i_am_desperate_for_this_to_work(){

    window.wordElement = document.getElementById('word');
    window.UserInput = document.getElementById('input');
    window.start = document.getElementById('start');
    window.main = document.getElementById('main');
    window.options = document.getElementById('options');
    start.innerHTML = "Start typing!";
    start.setAttribute("class", "start");
    window.end = document.getElementById('end');
    window.startingMs2 = 0;
    window.showTimer2 = document.getElementById("timer2");
    window.bool = false;
    window.interval2;
    window.showWpm = document.getElementById("wpm");
    window.accuracy_stats = document.getElementById("accuracy_stats");
    window.results = document.getElementById("results");
    window.result_text_wpm = document.getElementById('result_text_wpm');
    window.result_value_wpm = document.getElementById('result_numbers_wpm');
    window.container = document.getElementById('container-words');
    window.result_text_accuracy = document.getElementById('result_text_accuracy');
    window.result_value_accuracy = document.getElementById('result_numbers_accuracy');
    window.result_numbers_time = document.getElementById('result_numbers_time');
    window.result_text_time = document.getElementById('result_text_time');

    window.string = container.textContent.trim();
    console.log(string);

    window.stringLength = string.length;






    function Spans(textToDisplay) {
        for (let i = 0; i < textToDisplay.length; i++) {
            let charSpan = document.createElement("span");
            charSpan.textContent = textToDisplay[i];
            wordElement.appendChild(charSpan);
        }
    }

    wordElement.textContent = '';
    // Initial population of the #word
    Spans(string);

    chars_total = string.length;

    // Outside the handler:
    window.prevValue = "";     // track the last input to detect deletions
    window.typing_errors = [];     // flat list of error indices, if you still need it
    window.errorEvents = [];     // detailed log of each mistyped keystroke
    window.letterSpans = wordElement.children;


     // --- START OF CURSOR LOGIC ---
    
    window.updateCursorPosition = function (currentIndex) { // Define a function to manage the cursor's class.
        // if (!letterSpans || letterSpans.length === 0) return; // Do nothing if there are no letter spans.

        for (let i = 0; i < letterSpans.length; i++) { // Loop through all letter spans.
            letterSpans[i].classList.remove('cursor'); // Remove 'cursor' class from any span that might have it.
        }

        if (currentIndex < letterSpans.length) { // If the current index is within the bounds of available spans.
            letterSpans[currentIndex].classList.add('cursor'); // Add 'cursor' class to the span at the current index.
        }
        // Optional: Handle cursor at the very end of the text if desired
        // else if (letterSpans.length > 0 && currentIndex >= letterSpans.length) {
        //     letterSpans[letterSpans.length - 1].classList.add('cursor'); // Or place on the last character
        // }
    }

    if (string.length > 0) { // If there is text to type.
        updateCursorPosition(0); // Set the initial cursor position at the beginning of the text.
    }
    // --- END OF CURSOR LOGIC ---


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
                    span.className = "red_letter";
                    if (string[i] === ' '){
                        span.className = 'missed_space';
                    }

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
            }
            // } else {
            //     span.classList.remove("green_letter", "red_letter", "missed_space");
            // }
        }


        updateCursorPosition(UserStr.length);


        // Zazna konec tipkanja
        if (UserStr.length === string.length) {
            clearInterval(interval2);
            completed(UserInput);
        }

        // Updejta preValue
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


    // Accuracy (%) = (Total Correct Characters / (Total Correct Characters + Total Incorrect Characters + Total Extra Characters)) * 100


    function completed(UserInput) {
        chars_wrong = typing_errors.length;
        let right = chars_right();
        final_accuracy = Math.floor((right / (right + chars_wrong) * 100), 1);
        end.setAttribute("class", "end");
        console.log(typing_errors);
        console.log(string.length);
        clearInterval(interval2);
        interval2 = null;
        bool = false;
        calculateWPM(stringLength, startingMs2 * 10);
        UserInput.readOnly = true;
        main.classList.add("hide");
        options.classList.add("hide");
        results.classList.remove("hide");
        showWpm.classList.add('results-row');
        showTimer2.classList.remove("hide");
        showTimer2.classList.add('results-row');
        accuracy_stats.classList.remove("hide");
        accuracy_stats.classList.add('results-row');
        wpm.classList.remove("hide");
        result_text_accuracy.innerHTML = 'Your accuracy: ';
        result_value_accuracy.innerHTML = final_accuracy + '%';
        result_text_time.innerHTML = "Final time: ";        
        result_numbers_time.innerHTML = startingMs2 / 100 + 's';
    }



    function calculateWPM(charactersTyped, timeMs) {
        let wpm = Math.round((charactersTyped * 60000) / (5 * timeMs));
        result_text_wpm.innerHTML = "Your wpm:";
        return result_value_wpm.innerHTML = wpm;
    }






    function updateTimer2() {
        startingMs2++;
    };
    
};

function reset() {
    window.location.reload();
}