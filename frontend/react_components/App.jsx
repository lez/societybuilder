Strings = require('../common_js/Strings');

var internet_state = {
  Poster: require('./Poster.jsx'),
  Post: require('./Post.jsx'),
  Test: require('./Test.jsx'),
  Commenter: require('./Commenter.jsx'),
  AddProfileImage: require('./AddProfileImage.jsx'),
  ImageField: require('./ImageField.jsx'),
  Comment: require('./Comment.jsx'),
  Comments: require('./Comments.jsx'),
  CommentPanel: require('./CommentPanel.jsx'),
  Thumbnail: require('./Thumbnail.jsx'),
  UserThumbnail: require('./UserThumbnail.jsx'),
  RoleThumbnail: require('./RoleThumbnail.jsx'),

  addAnyReactElement: function(react_class, element, attr) {
    var React = require('react');
    React.render(React.createElement(react_class, attr), element);
  },

  submit: function(event, element) {
    event.preventDefault();
    data = {};
    jQuery(element).find("input[type!='submit']").each(function (idx, input) {
      inp = jQuery(input);
      if (inp.attr('type') == 'checkbox') data[inp.attr('name')] = inp.prop('checked');
      else data[inp.attr('name')] = inp.val();
    });
    console.log(data);
    var url = element.getAttribute('data-url');
    jQuery.ajax({
      url: url,
      type: 'POST',
      data: data,
      success: function(result){
        if (!result.success) {
          alert(result.error ? result.error : Strings.general_error);
        } else {
          document.location.reload();
        }
      }.bind(this),
      error: function(result){
          alert(Strings.general_error);
        }.bind(this)
      });
    console.log(data);
  }
};

IS = internet_state;
