var React = require('react');

var UserThumbnail = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    if (this.props.image)
      return <div className="Thumbnail"><img src={this.props.image.thumbnail} /></div>;
    else
      return <span>semmi</span>;
  }
});

module.exports = UserThumbnail;