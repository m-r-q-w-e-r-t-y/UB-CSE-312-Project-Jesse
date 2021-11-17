const Route = require("./route");
const routes = [];

routes.push(
  new Route("/hello", "GET", (req, res) => {
    res.writeHead(200, {
      "Content-Type": "application/json",
    });
    res.end(JSON.stringify({ hello: "world" }));
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
