var React = require('react');
var RoleThumbnail = require('./RoleThumbnail.jsx');
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
        return <div className="Post">
            <div className="header clearfix">
                <RoleThumbnail role={post.role} size="medium"/>
                <div className="post_data">
                    <div>
                        {post.role.user ? <UserName user={post.role.user} /> : <span className="UserName"><a href={'/' + post.role.page.name}>{post.role.page.name}</a></span>}
                    </div>
                    <div>
                        <span className="TimeStamp"><a href={post.permalink}>{Time.human(post.created)}</a></span>
                    </div>
                </div>
                {(!this.state.editing) ? <div>
                <div className="DeletePostButton">
                        <a href="#" onClick={this.handleDelete}><i className="icon-cancel"></i></a>
                    </div>
                    <div className="EditPostButton">
                        <a href="#" onClick={this.handleEdit}><i className="icon-edit"></i></a>
                    </div></div>
                 : null
                 }
            </div>
            {this.state.editing ? <Poster user={this.props.user} editpost={post} />
                : <div>
                    <div className="content">{post.content}</div>
                    <Images images={post.images} />
                  </div>
            }

            <CommentPanel comments={post.comments} user={this.props.user} post={post} />
        </div>;
    },

    handleDelete: function(e) {
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

    handleEdit: function(e) {
        e.preventDefault();
        this.setState({'editing': 1});
    }
});

module.exports = Post;
