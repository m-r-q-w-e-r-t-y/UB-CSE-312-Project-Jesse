function Route(pathname, http_method, callback) {
  this._pathname = pathname;
  this._http_method = http_method;
  this._callback = callback;
}

Route.prototype.match = function (pathname, http_method) {
  return http_method === this._http_method && pathname === this._pathname;
};

Route.prototype.sendResponse = function (req, res) {
  this._callback(req, res);
};

module.exports = Route;
