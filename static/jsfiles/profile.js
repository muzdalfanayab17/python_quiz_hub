let profileForm = document.getElementById('profileForm');

if (profileForm) {

    profileForm.addEventListener('submit', (event) => {

        let newName = document.getElementById('newName').value.trim();

        if (newName.length < 3) {
            event.preventDefault();
            alert('Name must contain at least 3 characters');
        }

    });

}