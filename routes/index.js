const Route = require("./../route");
const loginGet = require("./login");
const { signupGet, signupPost } = require("./signup");
const stylesheetGet = require("./stylesheet");

const routes = [];

routes.push(new Route("/login", "GET", loginGet));
routes.push(new Route("/signup", "GET", signupGet));
routes.push(new Route("/signup", "POST", signupPost));
routes.push(new Route("/main.css", "GET", stylesheetGet));

module.exports = routes;
