// Username validation
const userNameField = document.querySelector('#usernameField');
const feedBackField = document.querySelector('#invalid-feedback-username')

userNameField.addEventListener('keyup',(e)=>{
    var userNameEntered = e.target.value;

    // Only make calls when user enters something
    if(userNameEntered.length > 0){
     fetch('/accounts/validate_username', {
         body: JSON.stringify({username:userNameEntered}),
         method: "POST"
     }).then(result=>result.json()).then(data=>{
        // Check if the error exists and modify input box and notify user
         if(data.username_error){
             userNameField.classList.remove("is-valid")
             userNameField.classList.add('is-invalid')
             feedBackField.style.display = "block";

             feedBackField.innerHTML = `<p style="color: red">${data.username_error}</p>`;
         }
         else{
             userNameField.classList.remove('is-invalid')
             userNameField.classList.add('is-valid')
             feedBackField.style.display = "block";

             feedBackField.innerHTML = `<p style="color: #3fb618">${data.username_success}</p>`;
         }
     })
    }
})

// Email Validation