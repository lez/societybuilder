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
        <div className="clearfix">
            <UserThumbnail user={this.props.comment.user} />
            <div className="comment_body">
                <UserName user={this.props.comment.user} />
                {this.props.comment.comment}
            </div>
        </div>
        {this.props.comment.image ? <Thumbnail image={this.props.comment.image} /> : null}
      </div>
    );
  }
});

module.exports = Commenter;