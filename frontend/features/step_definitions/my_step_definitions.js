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


    this.Then(/^I get logged out$/, function () {

        this.browser.assert.element('#loginbox');
        this.browser.assert.cookie('me');

    });


    this.When(/^I create a page called "(.*)" with the description "(.*)"$/, function (name, description, callback) {

        this.browser.visit('/page/create', function () {
            this.browser.fill('input[name="name"]', name)
                        .fill('input[name="description"]', description)
                        .pressButton('Create Page', function() {
                            this.browser.assert.success();
                            this.browser.assert.url(/\/page\/(.*)\/show/);
                            this.page_id = this.browser.url.match(/\/page\/(.*)\/show/)[1];
                            callback();
                        }.bind(this));
        }.bind(this));

    });


    this.Then(/^the page name is "(.*)"/, function (name) {
        this.browser.assert.text('#showpage .title', name);
    });


    this.Then(/^the page description is "(.*)"/, function (description) {
        this.browser.assert.text('.description', description);
    });


    this.When(/^I visit the edit page$/, function (callback) {
        this.browser.visit('/page/'+this.page_id+'/edit', callback);
    });


    this.When(/^I visit the edit profile page$/, function (callback) {
        this.browser.visit('/komakoma/profile', callback);
    });


    this.When(/^I visit "(.*)"$/, function (url, callback) {
        this.browser.visit(url, callback);
    });


    this.When(/^I set the page description to "(.*)"$/, function (description) {
        this.browser.fill('textarea.description', description);
    });


    this.When(/^I set the about me to "(.*)"$/, function (about) {
        this.browser.fill('textarea.about', about);
    });


    this.When(/^I press the button "(.*)"$/, function (button, callback) {
        this.browser.pressButton(button, callback);
    });


    this.Then(/^the page description on edit page is "(.*)"/, function (description) {
        this.browser.assert.text('textarea.description', description);
    });


    this.Then(/^the about me says I am "(.*)"/, function (about) {
        this.browser.assert.text('textarea.about', about);
    });


    this.When(/^I post "(.*)"$/, function (content, callback) {
        this.browser.fill('textarea.content', content)
                    .pressButton('Küldés', callback);
    });

    this.When(/^I refresh the page$/, function (callback) {
        this.browser.visit(this.browser.url, callback);
    });


    this.Then(/^I see a post with content "(.*)"$/, function (content) {
        this.browser.assert.text('.Post .content', content);
    });

};

