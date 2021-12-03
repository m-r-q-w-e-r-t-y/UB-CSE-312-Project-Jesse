const fs = require("fs");
const bcrypt = require("bcryptjs");
const formidable = require("formidable");
const { tokenGenerator } = require("./../utils.js");
const { User } = require("./../db_init");

const login = {};

login.GET = function (req, res) {
  const data = fs.readFileSync("views/login.html");
  const html = data.toString();
  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "X-Content-Type-Options": "nosniff",
    "Content-Length": Buffer.byteLength(html, "utf-8"),
  });
  res.end(html);
};

login.POST = function (req, res) {
  const form = formidable({});
  form.parse(req, (err, fields, files) => {
    if (err) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end(err.toString());
      return;
    }
    const username = fields["username"];
    const password = fields["password"];

    if (!username || !password) {
      res.writeHead(400, { "Content-Type": "text/plain" });
      res.end("Fields cannot be empty");
      return;
    }
    User.getUserRecordByName([username], (user_record, db_err) => {
      if (db_err) {
        res.writeHead(400, { "Content-Type": "text/plain" });
        res.end(db_err.toString());
        return;
      }
      if (
        !user_record ||
        !bcrypt.compareSync(password, user_record.hashedPassword)
      ) {
        res.writeHead(401, { "Content-Type": "text/plain" });
        res.end("Incorrect Username or Password");
        return;
      }
      const authToken = tokenGenerator();
      User.updateUserAuthTokenByName(
        [authToken, username],
        (set_auth_token_err) => {
          if (set_auth_token_err) {
            res.writeHead(500, { "Content-Type": "text/plain" });
            res.end(set_auth_token_err.toString());
            return;
          }
          res.writeHead(200, {
            "Content-Type": "text/plain",
            "Set-Cookie": `auth_token=${authToken};Max-Age=20000;HttpOnly`,
          });
          res.end("Logged in " + authToken);
        }
      );
    });
  });
};

module.exports = login;
