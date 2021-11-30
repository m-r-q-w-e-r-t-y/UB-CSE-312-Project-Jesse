const fs = require("fs");
const Route = require("./route");
const routes = [];

routes.push(
  new Route("/hello", "GET", (req, res) => {
    res.writeHead(200, {
      "Content-Type": "application/json",
    });
    res.end(JSON.stringify({ hello: "world" }));
  }),
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
  })
);

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
