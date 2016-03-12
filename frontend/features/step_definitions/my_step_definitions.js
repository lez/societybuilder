module.exports = function () {

    this.Given(/^I am on the front page$/, function (callback) {

        this.visit('/', callback);

    });


    this.Given(/^I am logged in$/, function (callback) {

        this.browser.visit('/', function () {
            this.browser.fill('#loginbox input[name="login"]', 'komakoma')
                        .fill('#loginbox input[name="passwd"]', 'komakoma')
                        .pressButton('Log in', callback)
        }.bind(this));

    });


    this.When(/^I log in$/, function (callback) {

        this.browser.fill('#loginbox input[name="login"]', 'komakoma')
                    .fill('#loginbox input[name="passwd"]', 'komakoma')
                    .pressButton('Log in', callback);

    });


    this.When(/^I log out$/, function (callback) {

        this.browser.assert.element('.logoutbutton');
        this.browser.visit('/logout', callback);

    });


    this.When(/^I sign up$/, function (callback) {

        this.browser.fill('#signupbox input[name="login"]', 'komakoma')
                    .fill('#signupbox input[name="passwd"]', 'komakoma')
                    .fill('#signupbox input[name="email"]', 'komakoma@gmail.com')
                    .pressButton('Sign up', callback);

    });


    this.Then(/^I get logged in$/, function (callback) {

        this.browser.assert.element('#profilemenu');
        this.browser.assert.text('.userlink', 'komakoma');
        if (!this.browser.getCookie('me')) {
            callback(new Error('Token not found in cookie'));
        }
        callback();

    });


    this.Then(/^I get logged out$/, function (callback) {

        this.browser.assert.element('#loginbox');
        this.browser.assert.cookie('me');
        callback();

    });


    this.When(/^I create a page called "(.*)" with the description "(.*)"$/, function (name, description, callback) {

        this.browser.visit('/page/create', function () {
            this.browser.fill('input[name="name"]', name)
                        .fill('input[name="description"]', description)
                        .pressButton('Create Page', callback)
        }.bind(this));

    });


    this.Then(/^the page is created$/, function (callback) {
        this.browser.assert.success();
        //this.browser.assert.global('location', '/page/(.*)/show', 'the url should be right');
        callback();
    });


    this.Then(/^the page name is "(.*)"/, function (name, callback) {
        this.browser.assert.text('#showpage .title', name);
        callback();
    });


    this.Then(/^the page description is "(.*)"/, function (description, callback) {
        this.browser.assert.text('.description', description);
        callback();
    });


};

