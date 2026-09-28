// ====================
// LOGIN FORM
// ====================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const emailError = document.getElementById("emailError");
        const passwordError = document.getElementById("passwordError");

        emailError.textContent = "";
        passwordError.textContent = "";

        let isValid = true;

        if (email === "") {
            emailError.textContent = "Please enter your email";
            isValid = false;
        }

        if (password === "") {
            passwordError.textContent = "Please enter your password";
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        }

    });

}


// ====================
// REGISTER FORM
// ====================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function(event) {

        const name = document.getElementById("name").value;
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const gender = document.getElementById("gender").value;

        const nameError = document.getElementById("nameError");
        const emailError = document.getElementById("registerEmailError");
        const passwordError = document.getElementById("registerPasswordError");
        const genderError = document.getElementById("genderError");

        nameError.textContent = "";
        emailError.textContent = "";
        passwordError.textContent = "";
        genderError.textContent = "";

        let isValid = true;

        if (name === "") {
            nameError.textContent = "Please enter your name";
            isValid = false;
        }

        if (email === "") {
            emailError.textContent = "Please enter your email";
            isValid = false;
        }

        if (password === "") {
            passwordError.textContent = "Please enter your password";
            isValid = false;
        }

        if (gender === "") {
            genderError.textContent = "Please select your gender";
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        }

    });

}
