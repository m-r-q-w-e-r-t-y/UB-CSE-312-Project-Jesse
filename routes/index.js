const Route = require("./../route");
const login = require("./login");
const signup = require("./signup");
const stylesheet = require("./stylesheet");

const routes = [];

routes.push(new Route("/login", "GET", login.GET));
routes.push(new Route("/login", "POST", login.POST));
routes.push(new Route("/signup", "GET", signup.GET));
routes.push(new Route("/signup", "POST", signup.POST));
routes.push(new Route("/main.css", "GET", stylesheet.GET));

module.exports = routes;
