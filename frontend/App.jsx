import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'

import Strings from './common_js/Strings'

import Poster from './react_components/Poster.jsx';
import Post from './react_components/Post.jsx';
import Test from './react_components/Test.jsx';
import Commenter from './react_components/Commenter.jsx';
import ImageField from './react_components/ImageField.jsx';
import Comment from './react_components/Comment.jsx';
import Comments from './react_components/Comments.jsx';
import CommentPanel from './react_components/CommentPanel.jsx';
import Thumbnail from './react_components/Thumbnail.jsx';
import UserThumbnail from './react_components/UserThumbnail.jsx';
import PageThumbnail from './react_components/PageThumbnail.jsx';
import RoleThumbnail from './react_components/RoleThumbnail.jsx';
import RestImageField from './react_components/RestImageField.jsx';
import RestTextField from './react_components/RestTextField.jsx';

import { rootReducer } from './reducers'


const store = createStore(
    rootReducer,
    applyMiddleware(
        thunk
    )
)

window.IS = {
    Poster: Poster,
    Post: Post,
    Test: Test,
    Commenter: Commenter,
    ImageField: ImageField,
    Comment: Comment,
    Comments: Comments,
    CommentPanel: CommentPanel,
    Thumbnail: Thumbnail,
    UserThumbnail: UserThumbnail,
    PageThumbnail: PageThumbnail,
    RoleThumbnail: RoleThumbnail,
    RestImageField: RestImageField,
    RestTextField: RestTextField,

    store: store,

    init: () => {
        store.subscribe(() =>
            console.log('STATE', store.getState())
        )
    },

    addAnyReactElement: function (react_class, element, attr) {
        if (react_class === Post) {
            this.store.dispatch({type: 'POST', post: attr.post})
            this.store.dispatch({type: 'ME', user: attr.user}) // FIXME only once
        }
        let react_element = React.createElement(react_class, attr)
        ReactDOM.render(<Provider store={this.store}>{react_element}</Provider>, element)

    },

    // create page, signup, etc. (pyxl forms)
    submit: function (event, element, callback) {
        event.preventDefault();
        var data = {};
        jQuery(element).find("input[type!='submit']").each(function (idx, input) {
            var inp = jQuery(input);
            if (!inp.hasClass('exclude-from-rest')) {
                if (inp.attr('type') == 'checkbox') data[inp.attr('name')] = inp.prop('checked');
                else data[inp.attr('name')] = inp.val();
            }
        });
        var url = element.getAttribute('data-url');

        jQuery.ajax({
            url: url,
            type: 'POST',
            data: data
        }).done(function (result) {
            if (callback) callback(result);
            else document.location.reload();
        }).fail(function (xhr) {
            var result = JSON.parse(xhr.responseText);

            this.clearErrors(element);
            if (result.errors !== undefined) {
                for (var i = 0; i < result.errors.length; i++) {
                    this.displayError(element, result.errors[i]);
                }
                return;
            }

            if (!result.error) {
                alert(Strings.general_error);
                return;
            }
            if (!result.field) {
                alert(result.error);
                return;
            }
            this.displayError(element, result);
        }.bind(this));
    },

    clearErrors: function (element) {
        jQuery(element).find('span.error').html('');
    },

    submitLogin: function (event, element, callback) {
        event.preventDefault();
        var data = {};
        data['login'] = jQuery(element).find("input[name='login']").val();
        data['passwd'] = jQuery(element).find("input[name='passwd']").val();
        var url = element.getAttribute('data-url');

        jQuery.ajax({
            url: url,
            type: 'POST',
            data: data
        }).done(function (result) {
            if (callback) callback(result);
            else document.location.reload();
        }).fail(function (xhr) {
            console.log('failed');
            var result = JSON.parse(xhr.responseText);
            this.clearErrors(element);
            jQuery(element).find('#error').find('span.error').html(result.error);
            console.log('failed no');

            //jQuery('#loginbox').find('#error').find('span.error').html('fakk')
        }.bind(this));
    },

    displayError: function (element, error_with_field) {
        var error = error_with_field.error;
        var field = error_with_field.field;
        var container = jQuery(element).find('#' + field + '_error').find('span.error');
        if (container.length == 0) {
            alert(error + '; field=' + field);
        } else {
            container.html(error);
        }
    },

    // react
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

IS.init()