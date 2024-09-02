document.addEventListener('DOMContentLoaded', function() {
    console.log("Quiz app loaded!");

    // Shuffle questions and options
    const quizForm = document.querySelector('form');
    if (quizForm) {
        shuffleQuestions(quizForm);
    }

    // Add a countdown timer
    const timerDisplay = document.getElementById('timer');
    if (timerDisplay) {
        startTimer(60, timerDisplay); // 60 seconds timer
    }

    // Form submission handling
    quizForm.addEventListener('submit', function(event) {
        event.preventDefault();
        let score = 0;
        const totalQuestions = quizForm.querySelectorAll('.question').length;
        
        quizForm.querySelectorAll('.question').forEach(question => {
            const selectedOption = question.querySelector('input[type="radio"]:checked');
            if (selectedOption && selectedOption.value === question.dataset.correct) {
                score++;
            }
        });

        alert(`You scored ${score} out of ${totalQuestions}`);
        this.submit();  // Uncomment this line if you want the form to actually submit after showing the alert
    });

    // Function to shuffle questions and options
    function shuffleQuestions(form) {
        const questions = Array.from(form.querySelectorAll('.question'));
        questions.forEach(question => {
            const options = Array.from(question.querySelectorAll('input[type="radio"]'));
            shuffleArray(options);
            const parent = options[0].closest('div');
            options.forEach(option => parent.appendChild(option.closest('label')));
        });
        shuffleArray(questions);
        const parent = form.querySelector('div.questions');
        questions.forEach(question => parent.appendChild(question));
    }

    // Utility function to shuffle an array
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Countdown timer
    function startTimer(duration, display) {
        let timer = duration, minutes, seconds;
        const interval = setInterval(function () {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(interval);
                alert("Time's up!");
                quizForm.submit();  // Automatically submit the form when time's up
            }
        }, 1000);
    }
});
