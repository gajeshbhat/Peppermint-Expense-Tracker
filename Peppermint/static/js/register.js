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
const emailField = document.querySelector('#emailField');
const emailValidityField = document.querySelector('#invalid-feedback-email')

emailField.addEventListener('keyup',(e)=>{
     var emailEntered = e.target.value;

    // Only make calls when user enters something
    if(emailEntered.length > 0){
     fetch('/accounts/validate_email', {
         body: JSON.stringify({email:emailEntered}),
         method: "POST"
     }).then(result=>result.json()).then(data=>{
        // Check if the error exists and modify input box and notify user
         if(data.email_error){
             emailField.classList.remove("is-valid")
             emailField.classList.add('is-invalid')
             emailValidityField.style.display = "block";

             emailValidityField.innerHTML = `<p style="color: red">${data.email_error}</p>`;
         }
         else{
             emailField.classList.remove('is-invalid')
             emailField.classList.add('is-valid')
             emailValidityField.style.display = "block";

             emailValidityField.innerHTML = `<p style="color: #3fb618">${data.email_success}</p>`;
         }
     })
    }
})

// Password Button Toggling

const passwordToggleButton = document.querySelector('#show-password-btn');

passwordToggleButton.addEventListener('click',(e)=>{
    const passwordFieldContent = document.querySelector('#passwordField');

    if(passwordToggleButton.textContent == "Show Password"){
       passwordToggleButton.textContent = "Hide";
       passwordFieldContent.setAttribute('type','text');
    }
    else{
        passwordToggleButton.textContent = "Show Password";
        passwordFieldContent.setAttribute('type','password');
    }
})
