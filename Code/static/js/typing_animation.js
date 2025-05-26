function i_am_desperate_for_this_to_work() {

    window.wordElement = document.getElementById('word');
    window.UserInput = document.getElementById('input');
    window.start = document.getElementById('start');
    window.main = document.getElementById('main');
    window.options1 = document.getElementById('options1');
    window.options2 = document.getElementById('options2');
    window.options = document.getElementById('options');
    start.innerHTML = "Start typing!";
    start.setAttribute("class", "start");
    window.end = document.getElementById('end');
    window.startingMs2 = 0;
    window.showTimer2 = document.getElementById("timer2");
    window.bool = false;
    window.countdown_timer = document.getElementById('countdown_timer');
    window.interval2 = null;
    window.interval1 = null;
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
    window.CapsLock = document.getElementById('CapsLockWarning');
    window.buttons_time = document.getElementsByName("buttons_time");
    window.all_buttons = document.getElementById('button-bar');
    window.string = container.textContent.trim();
    window.startingMs15 = 1500;
    window.hardcodedTime = 0;
    window.original_countdownMS = 0;
    window.selected_time;
    console.log(string);
    window.stringLength = string.length;
    let og_time_ms = 0;

    let buttons = [...document.getElementsByName('buttons'), ...document.getElementsByName('buttons_time')];
    
    
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function () {
            for (let j = 0; j < buttons.length; j++) {
                buttons[j].classList.remove('activeButton');
            }
            buttons[i].classList.add('activeButton');
        });
    }

    function Spans(textToDisplay) {
        for (let i = 0; i < textToDisplay.length; i++) {
            let charSpan = document.createElement("span");
            charSpan.textContent = textToDisplay[i];
            wordElement.appendChild(charSpan);
        }
    }

    wordElement.textContent = '';
    Spans(string);

    window.chars_total = string.length;
    window.prevValue = "";
    window.typing_errors = [];
    window.errorEvents = [];
    window.letterSpans = wordElement.children;


    window.updateCursorPosition = function (currentIndex) {
        if (document.activeElement === UserInput){
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

        if (UserStr.length > 0 && !bool) {
            bool = true;

            window.timeButtons = document.getElementsByName('buttons_time');
            window.usingCountdown = false;
            for (let i = 0; i < timeButtons.length; i++) {
                if (timeButtons[i].classList.contains("activeButton")) {
                    selected_time = parseInt(timeButtons[i].textContent)*1000;
                    og_time_ms = selected_time;

                    console.log(selected_time);
                    usingCountdown = true;
                    countdown_timer.classList.remove('hide');
                    break;
                }
            }
            if (usingCountdown) {
                countdownStartTime = Date.now();
                interval1 = setInterval(countdown, 10);
            } else {
                interval2 = setInterval(updateTimer2, 10);
            }
            start.remove();
        }

        if (UserStr.length < prevValue.length) {
            for (let i = UserStr.length; i < string.length; i++) {
                letterSpans[i].classList.remove("green_letter", "red_letter", "missed_space");
            }
            prevValue = UserStr;
            updateCursorPosition(UserStr.length);
            return;
        }

        for (let i = 0; i < string.length; i++) {
            let span = letterSpans[i];
            if (i < UserStr.length) {
                if (UserStr[i] === string[i]) {
                    span.className = "green_letter";
                } else {
                    span.className = "red_letter";
                    if (string[i] === ' ') {
                        span.className = 'missed_space';
                    }
                    if (prevValue[i] !== UserStr[i]) {
                    typing_errors.push(i);
                    //     errorEvents.push({
                    //         index: i,
                    //         typedChar: UserStr[i],
                    //         expectedChar: string[i],
                    //         timestamp: new Date().toLocaleTimeString()
                    //     });
                    }
                }
            }
        }

        updateCursorPosition(UserStr.length);

        if (UserStr.length === string.length) {
            clearInterval(interval2);
            completed(UserInput);
        }

        prevValue = UserStr;
    };


    function chars_right() { // Funkcija ki prešteje pravilne znake.
    let chars_right_int = 0;
    for (let i = 0; i < string.length; i++) { // Zanka ki gre skozi vse znake v stringu.
        let span = letterSpans[i]; // Pridobimo kere vrtste razred ima span.
        if (span.className === "green_letter") { // Preverimo ali je črka pravilna.
            chars_right_int++; // Če je pravilna se poveča števec pravilnih znakov.
        }
    }
    return chars_right_int;
} 

    function completed(UserInput) {
        if (usingCountdown === true) {
            chars_wrong = typing_errors.length;
            let right = chars_right();
            final_accuracy = Math.floor((right / (right + chars_wrong) * 100), 1);
            end.setAttribute("class", "end");
            console.log(typing_errors);
            console.log(string.length);
            clearInterval(interval1);
            interval1 = null;
            bool = false;
            let charactersTyped = chars_right();
            calculateWPM(charactersTyped, og_time_ms, 'time');
            UserInput.readOnly = true;
            main.classList.add("hide");
            all_buttons.classList.add('hide');
            results.classList.remove("hide");
            showWpm.classList.add('results-row');
            showTimer2.classList.add('results-row');
            accuracy_stats.classList.remove("hide");
            accuracy_stats.classList.add('results-row');
            wpm.classList.remove("hide");
            result_text_accuracy.innerHTML = 'Your accuracy: ';
            result_value_accuracy.innerHTML = final_accuracy + '%';
            result_text_time.innerHTML = "Final time: ";        
            result_numbers_time.innerHTML = og_time_ms / 100 + 's';
            CapsLock.remove();
        } else {
            chars_wrong = typing_errors.length;
            let right = chars_right();
            final_accuracy = Math.floor((right / (right + chars_wrong) * 100), 1);
            end.setAttribute("class", "end");
            console.log(typing_errors);
            console.log(string.length);
            clearInterval(interval2);
            interval2 = null;
            bool = false;
            let charactersTyped = chars_right();
            calculateWPM(charactersTyped, startingMs2 * 10, 'word');
            UserInput.readOnly = true;
            main.classList.add("hide");
            all_buttons.classList.add('hide');

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
            CapsLock.remove();
        }
    }


function calculateWPM(charactersTyped, timeMs, testType) {
        let wpm = timeMs === 0 ? 0 : Math.round((charactersTyped * 60000) / (5 * timeMs)); // Za izračun wpm.
        result_text_wpm.innerHTML = "Your wpm:"; // Doda besedilo v rezultat.
        result_value_wpm.innerHTML = wpm; // Doda še vrednost wpm v rezultat.
        // Preveri ali je tip testa word.
        if (testType === 'word') {
            console.log('Saving score with wpm:', wpm, 'and word_count:', window.selected_word_count); // izpis v konzolo o pridobljenih razultatih.
            // Isto kot pri lessonih.
            fetch('/save_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ wpm: wpm, word_count: window.selected_word_count })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error saving score:', data.error);
                        alert('Failed to save score: ' + data.error);
                    } else if (data.updated) {
                        end.innerHTML += '<div class="new-pb"> New personal best!</div>';
                    }
                })
                .catch(err => console.error('Error saving WPM:', err));
            // Preveri ali je tip testa time.
            // Ponovimo kot pri word tipu.
        } else if (testType === 'time') {
            console.log('Saving score with wpm:', wpm, 'and time:', window.selected_time);
            fetch('/save_score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ wpm: wpm, time: window.selected_time })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error saving score:', data.error);
                        alert('Failed to save score: ' + data.error);
                    } else if (data.updated) {
                        end.innerHTML += '<div class="new-pb">🎉 New personal best!</div>';
                    }
                })
                .catch(err => console.error('Error saving WPM:', err));
        }
        return wpm;
    }
    let countdownStartTime = 0;

    function countdown() {
        const elapsed = Date.now() - countdownStartTime;
        countdown_timer.innerHTML = ((og_time_ms - elapsed)/1000).toFixed();
        if (elapsed >= og_time_ms) {
            clearInterval(interval1);
            completed(UserInput);
        }
    }

    function updateTimer2() {
        startingMs2++;
    }
}

function reset() {
    window.location.reload();
}
