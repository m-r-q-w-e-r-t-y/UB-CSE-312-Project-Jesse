const fs = require("fs");

function stylesheetGet(req, res) {
  const data = fs.readFileSync("views/main.css");
  const css = data.toString();
  res.writeHead(200, {
    "Content-Type": "text/css",
    "X-Content-Type-Options": "nosniff",
    "Content-Length": Buffer.byteLength(css),
  });
  res.end(css);
}

module.exports = stylesheetGet;
