let welcomeMessage = document.getElementById('welcomeMessage');

let startQuizBtn = document.getElementById('startQuizBtn');
let logoutLink= document.getElementById('logoutLink');
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
if(logoutLink){
    logoutLink.addEventListener('click',(event)=>{
        let confirmLogout=confirm('Are you sure you want to logout?');
        if(!confirmLogout){
            event.preventDefault();
        }
    })
}
if (startQuizBtn) {

    startQuizBtn.addEventListener('click', (event) => {

        console.log('Start Quiz button Clicked');

    });

}

if (welcomeMessage) {

    welcomeMessage.textContent = 'Welcome to Python Quiz Hub!';

}