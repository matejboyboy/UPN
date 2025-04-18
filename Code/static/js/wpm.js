function calculateWPM(charactersTyped, timeInMinutes) {
    const words = charactersTyped / 5;
    const wpm = words / timeInMinutes;
    return wpm;
}
export { calculateWPM };