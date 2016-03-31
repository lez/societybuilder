var React = require('react');
var Comment = require('./Comment.jsx');
var randomstring = require('random-string');

var Comments = React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {

        return <div className="Comments">
            {this.props.comments.map(function (comment) {
                comment.key = randomstring(12);
                var editable = (this.props.user && comment.user.id == this.props.user.id);

                return <Comment comment={comment} key={comment.key} editable={editable}/>;
            }.bind(this))}
        </div>;
    }

});

module.exports = Comments;