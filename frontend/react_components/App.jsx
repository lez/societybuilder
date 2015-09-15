Strings = require('../common_js/Strings');

var internet_state = {
  React: require('react'),
  Poster: require('./Poster.jsx'),

  addComposer: function(element, tube) {
    var React = require('react');
    var Poster = require('./Poster.jsx');
    React.render(<Poster tube={tube} />, element);
  },

/*  addCommenter: function(element, thumbnail, user_id, item_type, item_id, appendto){
    var React = require('react');
    var Commenter = require('./Commenter.jsx');

    React.render(
      <Commenter
        thumbnail={thumbnail}
        user_id={user_id}
        item_type={item_type}
        item_id={item_id}
        appendto={appendto}
      />,
      element
    );
  },*/

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
