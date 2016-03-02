var zombie = require('zombie');

zombie.localhost('localhost', 81);

function World() {

  this.browser = new zombie();

  this.browser.on('loaded', function(doc) {
    this.browser.window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {};
  }.bind(this));

  this.visit = function (url, callback) {
    this.browser.visit(url, callback);
  };

}

module.exports = function() {
  this.World = World;
};

