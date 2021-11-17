const http = require("http");

const { routes, notFoundRoute } = require("./routes");

const server = http.createServer(async (req, res) => {
  const { url, method } = req;
  for (let route of routes) {
    if (route.match(url, method)) {
      return route.sendResponse(req, res);
    }
  }
  notFoundRoute.sendResponse(req, res);
});

server.listen(8000, () => {
  console.log("Server running on port: 8000");
});
