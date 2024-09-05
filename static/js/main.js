// Example list of questions and answers
const quizData = [
    {
        question: "What is the output of print(2 ** 3)?",
        options: ["5", "6", "8", "9"],
        correctAnswer: "8"
    },
    {
        question: "Which of the following is a valid variable name in Python?",
        options: ["2abc", "_abc", "def", "for"],
        correctAnswer: "_abc"
    },
    {
        question: "What is the output of print(type([]))?",
        options: ["<class 'list'>", "<class 'tuple'>", "<class 'dict'>", "<class 'set'>"],
        correctAnswer: "<class 'list'>"
    },
    {
        question: "Which keyword is used for function declaration in Python?",
        options: ["function", "void", "def", "lambda"],
        correctAnswer: "def"
    },
    {
        question: "What does the 'len()' function do in Python?",
        options: ["Calculates length", "Returns last element", "Sorts items", "Generates sequence"],
        correctAnswer: "Calculates length"
    }
];

let currentQuestion = 0;
let score = 0;
const totalQuestions = quizData.length;
const userAnswers = [];

// Function to handle quiz submission
function submitQuiz() {
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    
    if (selectedAnswer) {
        const answerValue = selectedAnswer.value;
        userAnswers[currentQuestion] = answerValue;
        checkAnswer(answerValue);  // Function to validate the answer

        // Move to the next question or show the results
        if (currentQuestion < totalQuestions - 1) {
            currentQuestion++;
            loadNextQuestion();
        } else {
            showResults();
        }
    } else {
        alert("Please select an answer before submitting!");
    }
}

// Function to load the next question
function loadNextQuestion() {
    const questionTitle = document.querySelector('#question-title');
    const options = document.querySelectorAll('input[name="answer"]');
    const labels = document.querySelectorAll('label');

    const currentQuiz = quizData[currentQuestion];
    
    questionTitle.innerText = `Question ${currentQuestion + 1}: ${currentQuiz.question}`;
    
    options.forEach((option, index) => {
        option.checked = false;  // Reset radio button
        option.value = currentQuiz.options[index]; // Update value of radio button
        labels[index].innerText = currentQuiz.options[index];  // Update option text
    });
}

// Function to check if the selected answer is correct
function checkAnswer(answerValue) {
    const correctAnswer = quizData[currentQuestion].correctAnswer;
    if (answerValue === correctAnswer) {
        score++;
    }
}

// Function to display the final results
function showResults() {
    const resultMessage = `You scored ${score} out of ${totalQuestions}`;
    const resultDiv = document.querySelector('#quiz-result');
    resultDiv.innerText = resultMessage;
    resultDiv.style.display = 'block';
}

// Event listener for submit button
document.querySelector('#submit-btn').addEventListener('click', submitQuiz);

// Show quiz section and load the first question on Start Quiz button click
document.querySelector('#start-quiz-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent page reload
    document.querySelector('#quiz-section').style.display = 'block'; // Show the quiz
    loadNextQuestion();
});

// Load the first question on page load (if needed)
window.onload = function() {
    loadNextQuestion();
};
