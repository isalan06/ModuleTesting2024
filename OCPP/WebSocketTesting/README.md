@ match path
https://stackoverflow.com/questions/43140950/node-js-and-websocket-with-wildcard-in-url-path
 
 WebSocket.Server.prototype.shouldHandle = function shouldHandle(req) {
// Add your own logic and return `true` or `false` accordingly.
};

 ...
  let customShouldHandle (req) {
    const pattern = new require('url-patter')('/some/:key/path')
    const url = require('url').parse(req.url).pathname
    const match = pattern.match(url)
    
    if (!match) {
      return false
    }
    
    if (!req.params) {
      req.params = {}
    }
    req.params.key = match.key
    return true
  }
    
  ...
  let server = new WebSocket.Server({ 
    server: httpServer, 
    path: this.customShouldHandle 
  })
  ...

  @