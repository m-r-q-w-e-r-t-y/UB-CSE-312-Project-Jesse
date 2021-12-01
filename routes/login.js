const fs = require("fs");

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

module.exports = login;
