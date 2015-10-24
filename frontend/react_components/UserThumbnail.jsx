var React = require('react');
var Thumbnail = require('./Thumbnail.jsx');

var UserThumbnail = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    var size = this.props.size ? this.props.size : 'small';

    if (this.props.user.image) {
      return <Thumbnail image={this.props.user.image.thumbnail} size={size} />;
    }
    else {
      return <Thumbnail image="icon-user" size={size} />;
    }
  }
});

module.exports = UserThumbnail;