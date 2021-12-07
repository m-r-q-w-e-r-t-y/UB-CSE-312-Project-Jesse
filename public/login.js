function submitLoginForm() {
  const username = getValueById("username-input");
  const password = getValueById("password-input");

  var request = new XMLHttpRequest();
  request.open("POST", "/login");
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.response);
    }
  };

  const form = new FormData();
  form.append("username", username);
  form.append("password", password);
  request.send(form);
}