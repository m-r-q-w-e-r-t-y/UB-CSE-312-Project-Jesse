function submitSignupForm() {
  const username = getValueById("username-input");
  const password = getValueById("password-input");
  const confirm_password = getValueById("confirm-password-input");
  const image_file = document.getElementById("avatar").files[0];

  var request = new XMLHttpRequest();
  request.open("POST", "/signup");
  request.onreadystatechange = function () {
    if (this.readyState === 4) {
      document.getElementById("signup-form-submission-message").innerHTML =
        this.response;
      document.getElementById("signup-form-submission-message").style.color =
        this.status == 200 ? "black" : "red";
      console.log(this.response);
    }
  };

  const form = new FormData();
  form.append("username", username);
  form.append("password", password);
  form.append("confirm-password", confirm_password);
  form.append("avatar", image_file);
  request.send(form);
}
