const fs = require("fs");
const path = require("path");
const formidable = require("formidable");
const signup = {};

signup.GET = function (req, res) {
  const data = fs.readFileSync("views/signup.html");
  const html = data.toString();
  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "X-Content-Type-Options": "nosniff",
    "Content-Length": Buffer.byteLength(html, "utf-8"),
  });
  res.end(html);
};

signup.POST = function (req, res) {
  const form = formidable({ keepExtensions: true });
  form.parse(req, function (err, fields, files) {
    if (err) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end(err);
      return;
    }
    const username = fields["username"];
    const password = fields["password"];
    const confirm_password = fields["confirm-password"];
    const image = files["avatar"];

    //If any field is missing, return 400 error
    if (!(username && password && confirm_password && image)) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end("All fields must be filled");
      return;
    }

    //If password fields do not match, return 400 error
    if (password != confirm_password) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end("Passwords do not match");
      return;
    }

    //Check filetype
    if (!(image.mimetype && image.mimetype.includes("image"))) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end("Filetype must be image");
      return;
    }

    //Save the image to server
    const image_name = image && image.newFilename;
    const image_data = fs.readFileSync(image.filepath);
    fs.writeFileSync("uploads/" + image_name, image_data);

    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(
      JSON.stringify(
        {
          username,
          password,
          image_name,
        },
        null,
        2
      )
    );
  });
};

module.exports = signup;
