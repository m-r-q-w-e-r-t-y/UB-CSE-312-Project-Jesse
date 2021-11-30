const fs = require("fs");
const formidable = require("formidable");
const Route = require("./route");

const routes = [
  new Route("/signup", "GET", (req, res) => {
    const data = fs.readFileSync("views/signup.html");
    const html = data.toString();
    res.writeHead(200, {
      "Content-Type": "text/html; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
      "Content-Length": Buffer.byteLength(html, "utf-8"),
    });
    res.end(html);
  }),
  new Route("/login", "GET", (req, res) => {
    const data = fs.readFileSync("views/login.html");
    const html = data.toString();
    res.writeHead(200, {
      "Content-Type": "text/html; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
      "Content-Length": Buffer.byteLength(html, "utf-8"),
    });
    res.end(html);
  }),
  new Route("/main.css", "GET", (req, res) => {
    const data = fs.readFileSync("views/main.css");
    const css = data.toString();
    res.writeHead(200, {
      "Content-Type": "text/css",
      "X-Content-Type-Options": "nosniff",
      "Content-Length": Buffer.byteLength(css),
    });
    res.end(css);
  }),
  new Route("/signup", "POST", (req, res) => {
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
      const { username, password } = fields;
      const image_name = files["avatar"].toJSON()["newFilename"];
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
  }),
];

const notFoundRoute = new Route("*", "*", (req, res) => {
  res.writeHead(404, {
    "Content-Type": "application/json",
  });
  res.end(JSON.stringify({ message: "Invalid API call" }));
});

module.exports = {
  routes,
  notFoundRoute,
};
