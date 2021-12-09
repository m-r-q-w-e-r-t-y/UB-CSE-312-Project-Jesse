function submitLoginForm() {
  const username = getValueById("username-input");
  const password = getValueById("password-input");

  var request = new XMLHttpRequest();
  request.open("POST", "/login");
  request.onreadystatechange = function () {
    if (this.readyState === 4) {
      if (this.status == 200) {
        document.getElementById("login-form-submission-message").innerHTML =
          "Successfully logged in";
        document.getElementById("login-form-submission-message").style.color =
          "black";

        setTimeout(function () {
          window.location.href = "/";
        }, 1000);
      } else if (this.status == 400 || this.status == 401) {
        document.getElementById("login-form-submission-message").innerHTML =
          this.response;
        document.getElementById("login-form-submission-message").style.color =
          "red";
      }
    }
  };

  const form = new FormData();
  form.append("username", username);
  form.append("password", password);
  request.send(form);
}
