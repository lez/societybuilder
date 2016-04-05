import React from 'react';
import Comments from './Comments.jsx';
import Commenter from './Commenter.jsx';

export default React.createClass({
    getInitialState: function () {
        return {}
    },

    componentWillMount: function () {
        this.setState({'comments': this.props.comments});
    },

    render: function () {

        if (this.props.comments.length === 0 && !this.props.user) {
            return null;
        }

        return <div className="CommentPanel">
            <Comments comments={this.state.comments} user={this.props.user}/>
            {this.props.user ? <Commenter user={this.props.user} post={this.props.post} append={this.append}/> : null}
        </div>;
    },

    append: function (comment) {
        this.state.comments.push(comment);
        this.setState({'comments': this.state.comments});
    }

});
