function formValidate() {
    if (
        document.getElementById("password-input").value ===
        document.getElementById("confirm-password-input").value
    ) {
        document.getElementById("signup-input").disabled = false;
        document.getElementById("error-message").innerHTML = "";
    } else {
        document.getElementById("signup-input").disabled = true;
        document.getElementById("error-message").innerHTML =
            "Passwords do not match";
    }
}