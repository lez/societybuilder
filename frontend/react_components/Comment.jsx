var React = require('react');
var UserName = require('./UserName.jsx');
var UserThumbnail = require('./UserThumbnail.jsx');

var Commenter = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function() {
    return (
      <div className="Comment clearfix">
        <UserThumbnail user={this.props.comment.user} />
        <div className="comment_body">
            <UserName user={this.props.comment.user} />
            {this.props.comment.comment}
        </div>
      </div>
    );
  }
});

module.exports = Commenter;