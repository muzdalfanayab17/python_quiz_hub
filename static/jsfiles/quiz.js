let quizForm = document.getElementById("quizForm");
let submitQuizBtn = document.getElementById("submitQuizBtn");

if (submitQuizBtn) {
    submitQuizBtn.addEventListener("click", () => {
        console.log("Quiz submit button clicked");
    });
}

if (quizForm) {
    quizForm.addEventListener("submit", (event) => {

        let confirmSubmit = confirm(
            "Are you sure you want to submit the quiz?"
        );

        if (!confirmSubmit) {
            event.preventDefault();
        }
    });
    //quiz timmer
     let timer = document.getElementById("timer");

    let timeLeft = 180; // 180 seconds = 3 minutes

    let countdown = setInterval(() => {

        let minutes = Math.floor(timeLeft / 60);
        let seconds = timeLeft % 60;

        if (seconds < 10) {
            seconds = "0" + seconds;
        }

        timer.textContent =
            "Time Left: " + minutes + ":" + seconds;

        timeLeft--;

        // Time finished
        if (timeLeft < 0) {

            clearInterval(countdown);

            timer.textContent = "Time's Up!";

            alert("Time is over. Your quiz will be submitted.");

            quizForm.submit();
        }

    }, 1000);


}
