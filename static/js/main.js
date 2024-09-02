// Function to validate the quiz form before submission
function validateQuizForm() {
    let inputs = document.querySelectorAll('input[type="text"]');
    let isValid = true;

    inputs.forEach(input => {
        if (input.value.trim() === '') {
            input.style.borderColor = 'red';
            isValid = false;
        } else {
            input.style.borderColor = 'initial';
        }
    });

    if (!isValid) {
        alert("Please answer all questions before submitting the quiz.");
    }

    return isValid;
}

// Attach the validation function to the quiz form
document.addEventListener('DOMContentLoaded', function() {
    let quizForm = document.querySelector('form');
    if (quizForm) {
        quizForm.onsubmit = validateQuizForm;
    }
});
