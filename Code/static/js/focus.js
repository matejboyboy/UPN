
// function setupFocusBlur() {
//   let input_field = document.getElementById("input");
//   let container = document.getElementById("main");
//   let timeoutId; // Track the timeout ID

//   input_field.addEventListener("blur", () => {
//     // Clear any existing timeout to prevent multiple triggers
//     clearTimeout(timeoutId);
//     // Schedule adding the class after 1000ms (1 second)
//     timeoutId = setTimeout(() => {
//       container.classList.add('focus');
//     }, 1000);
//   });

//   input_field.addEventListener("focus", () => {
//     // Remove the class and cancel the pending timeout
//     container.classList.remove("focus");
//     clearTimeout(timeoutId);
//     input_field.selectionStart = input_field.selectionEnd = input_field.value.length;
//   });
// }

// // Call after DOM loads
// window.addEventListener('DOMContentLoaded', () => {
//   setupFocusBlur();
// });

