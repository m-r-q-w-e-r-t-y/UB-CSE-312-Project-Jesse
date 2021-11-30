const http = require("http");
const routes = require("./routes/index");

const server = http.createServer(async (req, res) => {
  const { url, method } = req;
  for (let route of routes) {
    if (route.match(url, method)) {
      return route.sendResponse(req, res);
    }
  }
  res.writeHead(404, { "Content-Type": "text/plain" });
  res.end("Invalid API Call");
});

server.listen(8000, () => {
  console.log("Server running on port: 8000");
});
