const fs = require("fs");
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
  const form = formidable({
    uploadDir: "uploads",
    keepExtensions: true,
    filter: function ({ name, originalFilename, mimetype }) {
      return mimetype && mimetype.includes("image");
    },
  });
  form.parse(req, function (err, fields, files) {
    if (err) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end(err);
      return;
    }
    const username = fields["username"];
    const password = fields["password"];
    const confirm_password = fields["confirm-password"];
    const image_name =
      files["avatar"] && files["avatar"].toJSON()["newFilename"];

    //If any field is missing, return 400 error
    if (!(username && password && confirm_password && image_name)) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end("All fields must be filled");
      return;
    }

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
