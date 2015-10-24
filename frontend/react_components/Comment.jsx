var React = require('react');
var UserName = require('./UserName.jsx');
var UserThumbnail = require('./UserThumbnail.jsx');
var Thumbnail = require('./Thumbnail.jsx');

var Commenter = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    return (
      <div className="Comment clearfix">
        <div className="float_left"><UserThumbnail user={this.props.comment.user} /></div>
        <div className="comment_body float_left">
            <UserName user={this.props.comment.user} />
            {this.props.comment.comment}
            <br/>
            {this.props.comment.image ? <Thumbnail image={this.props.comment.image.thumbnail} size="large" /> : null}
        </div>
      </div>
    );
  }
});

module.exports = Commenter;