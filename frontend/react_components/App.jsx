Strings = require('../common_js/Strings');

var internet_state = {
    Poster: require('./Poster.jsx'),
    Post: require('./Post.jsx'),
    Test: require('./Test.jsx'),
    Commenter: require('./Commenter.jsx'),
    ImageField: require('./ImageField.jsx'),
    Comment: require('./Comment.jsx'),
    Comments: require('./Comments.jsx'),
    CommentPanel: require('./CommentPanel.jsx'),
    Thumbnail: require('./Thumbnail.jsx'),
    UserThumbnail: require('./UserThumbnail.jsx'),
    RoleThumbnail: require('./RoleThumbnail.jsx'),
    RestImageField: require('./RestImageField.jsx'),
    RestTextField: require('./RestTextField.jsx'),

    reducer: function (state, action) {
        return action.active;
    },

    addAnyReactElement: function (react_class, element, attr) {
        var React = require('react');
        var ReactDOM = require('react-dom');

        ReactDOM.render(React.createElement(react_class, attr), element);
    },


    submit: function (event, element, callback) {
        event.preventDefault();
        var data = {};
        jQuery(element).find("input[type!='submit']").each(function (idx, input) {
            var inp = jQuery(input);
            if (inp.attr('type') == 'checkbox') data[inp.attr('name')] = inp.prop('checked');
            else data[inp.attr('name')] = inp.val();
        });
        var url = element.getAttribute('data-url');
        jQuery.ajax({
            url: url,
            type: 'POST',
            data: data,
            success: function (result) {
                if (callback) callback(result);
                else document.location.reload();
            }.bind(this),
            error: function (result) {
                alert(result.error ? result.error : Strings.general_error);
            }.bind(this)
        });
    },

    submitRest: function (url, data, callback) {
        jQuery.ajax({
            url: url,
            type: 'PUT',
            data: data,
            success: function (result) {
                if (callback) callback(result);
                else document.location.reload();
            }.bind(this),
            error: function (result) {
                alert(Strings.general_error);
            }.bind(this)
        });
    }
};

IS = internet_state;

//var redux = require('redux');
//IS.store = redux.createStore(IS.reducer);
//IS.store.subscribe(function () {console.log(IS.store.getState());});
