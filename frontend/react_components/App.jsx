var internet_state = {
  addComposer: function(element, tube) {
    var React = require('react');
    var Poster = require('./Poster.jsx');
    React.render(
      <Poster tube={tube} />,
      element
    );
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
};

IS = internet_state;
