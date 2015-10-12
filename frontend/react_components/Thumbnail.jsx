var React = require('react');

var UserThumbnail = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    if (this.props.image) {
      if (this.props.image.thumbnail.startsWith('icon-')) {
        return <div className="Thumbnail"><i className={this.props.image.thumbnail}></i></div>;
      } else {
        return <div className="Thumbnail"><img src={this.props.image.thumbnail} /></div>;
      }
    }
    else {
      return <span>semmi</span>;
    }
  }
});

module.exports = UserThumbnail;