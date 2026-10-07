
const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function(event) {

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();
        const gender = document.getElementById("gender").value;

        const message = document.getElementById("message");

        message.textContent = "";

        // Name validation
        if (name === "") {
            event.preventDefault();
            message.textContent = "Name cannot be empty";
            return;
        }

        if (name.length < 3) {
            event.preventDefault();
            message.textContent = "Name must contain at least 3 characters";
            return;
        }

        // Email validation
        if (email === "") {
            event.preventDefault();
            message.textContent = "Email cannot be empty";
            return;
        }

        // Password validation
        if (password === "") {
            event.preventDefault();
            message.textContent = "Password cannot be empty";
            return;
        }

        if (password.length < 6) {
            event.preventDefault();
            message.textContent = "Password must contain at least 6 characters";
            return;
        }

        // Gender validation
        if (gender === "") {
            event.preventDefault();
            message.textContent = "Please select your gender";
            return;
        }

        // Everything is valid
        message.textContent = "Creating your account...";

    });

}