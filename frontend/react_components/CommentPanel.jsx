var React = require('react');
var Comments = require('./Comments.jsx');
var Commenter = require('./Commenter.jsx');

var CommentPanel = React.createClass({
  getInitialState: function() {
    return {
    }
  },

  componentWillMount: function() {
    this.setState({'comments': this.props.comments});
  },

  render: function() {
    return (
      <div className="CommentPanel">
        <Comments comments={this.state.comments} />
        <Commenter user={this.props.user} post={this.props.post} append={this.append} />
      </div>
    );
  },

  append: function(comment) {
    this.state.comments.push(comment)
    this.setState({'comments': this.state.comments});
  },

});

module.exports = CommentPanel;
