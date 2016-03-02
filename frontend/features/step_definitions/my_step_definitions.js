module.exports = function () {

  this.Given(/^I am on the front page$/, function (callback) { // `this` is set to a World instance.

    this.visit('/', callback);

  });


  this.When(/^I log in$/, function (callback) {

    this.browser.fill('#loginbox input[name="login"]', 'komakoma')
                .fill('#loginbox input[name="passwd"]', 'komakoma')
                .pressButton('Log in', callback);

  });


  this.Then(/^I am logged in$/, function (callback) {

    this.browser.assert.element('#profilemenu');
    this.browser.assert.text('.userlink', 'komakoma');
    if (!this.browser.getCookie('me')) {
        callback(new Error('Token not found in cookie'));
    }
    callback();

  });


  this.When(/^I sign up$/, function (callback) {

    this.browser.fill('#signupbox input[name="login"]', 'komakoma')
                .fill('#signupbox input[name="passwd"]', 'komakoma')
                .fill('#signupbox input[name="email"]', 'komakoma@gmail.com')
                .pressButton('Sign up', callback);

  });

};

