var React = require('react');
var Comment = require('./Comment.jsx');
randomstring = require('random-string');

var Comments = React.createClass({
  getInitialState: function() {
    return {}
  },

  render: function(){
    return (<div className="Comments">{this.props.comments.map(function(comment) {comment.key=randomstring(12); return <Comment comment={comment} key={comment.key} />;})}</div>);
  },

});

module.exports = Comments