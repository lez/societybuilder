var React = require('react');

var UserThumbnail = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    if (this.props.user)
      return <img src={this.props.user.image.thumbnail30} />;
    else
      return <span>{this.props.user.id}</span>;
  }
});

module.exports = UserThumbnail;