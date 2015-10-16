var React = require('react');
var Thumbnail = require('./Thumbnail.jsx');
var UserName = require('./UserName.jsx');
var Images = require('./Images.jsx');
var Poster = require('./Poster.jsx');
var CommentPanel = require('./CommentPanel.jsx');
var Time = require('../common_js/Time.js');

var Post = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        var post = this.props.post;
        return (
        <div className="Post">
            <div className="header clearfix">
                <Thumbnail image={post.user.image} />
                <div className="post_data">
                    <div>
                        <UserName user={post.user} />
                    </div>
                    <div>
                        <span className="TimeStamp"><a href={post.permalink}>{Time.human(post.created)}</a></span>
                    </div>
                </div>
                {(!this.state.editing) ?<div>
                <div className="DeletePostButton">
                        <a href="#" onClick={this.delete}><i className="icon-cancel"></i></a>
                    </div>
                    <div className="EditPostButton">
                        <a href="#" onClick={this.edit}><i className="icon-edit"></i></a>
                    </div></div>
                 : null
                 }
            </div>
            {this.state.editing ? <Poster user={this.props.user} editpost={post} />
                : <div className="content">{post.content}</div>
            }
            <Images images={post.images} />
            <CommentPanel comments={post.comments} user={this.props.user} post={post} />
        </div>
        );
    },

    delete: function(e) {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this post?')){
            jQuery.ajax({
                url: '/api/post/' + this.props.post.id,
                type: 'DELETE',
                success: function(result){
                    if (!result.success) {
                        alert(result.error ? result.error : Strings.general_error);
                    } else {
                        document.location.reload();
                    }
                },
                error: function(result){
                   alert(Strings.general_error);
                }
            });
        }
    },
    edit: function(e) {
        e.preventDefault();
        this.setState({'editing': 1});
    }
});

module.exports = Post;
