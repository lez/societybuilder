Strings = require('../common_js/Strings');

var internet_state = {
  Poster: require('./Poster.jsx'),
  Test: require('./Test.jsx'),
  Commenter: require('./Commenter.jsx'),
  ProfileImage: require('./ProfileImage.jsx'),
  ImageField: require('./ImageField.jsx'),



  addAnyReactElement: function(react_class, element, attr) {
    var React = require('react');
    React.render(React.createElement(react_class, attr), element);
  },

/*  addGallery: function(element, image, current_user){
    var React = require('react');
    var Gallery = require('./Gallery.jsx');

    React.render(
      <Gallery image={image} current_user={current_user}/>,
      element
    );
    jQuery('#user_header').load("/fragments/user_header.php?user_id=" + image.user_id);
    jQuery('#comments').load("/fragments/image.php?img=" + image.image_id + '-' + image.serial);
  },*/




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
  },





};





IS = internet_state;
