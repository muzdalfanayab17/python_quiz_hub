 // Form ko select karna
    const form = document.getElementById("registerForm");

    // Message paragraph ko select karna
    const message = document.getElementById("message");


    // Form submit hone par
    form.addEventListener("submit", function(event) {

        // User ke inputs lena
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const gender = document.getElementById("gender").value;


        // Simple DOM validation
        if (name.length < 3) {

            event.preventDefault();

            message.textContent = "Name must contain at least 3 characters.";

            return;
        }


        if (password.length < 6) {

            event.preventDefault();

            message.textContent = "Password must contain at least 6 characters.";

            return;
        }


        if (gender === "") {

            event.preventDefault();

            message.textContent = "Please select your gender.";

            return;
        }


        // Agar sab theek hai
        message.textContent = "Creating your account...";

    });