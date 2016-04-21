import React from 'react'
import { dispatch, connect } from 'react-redux'

import RoleThumbnail from './RoleThumbnail.jsx'
import UserName from './UserName.jsx'
import Images from './Images.jsx'
import Poster from './Poster.jsx'
import CommentPanel from './CommentPanel.jsx'
import Time from '../common_js/Time.js'
import { commentDelete, addComment, editPost, upload, deleteImage, editComment, finishEditComment, deleteEditCommentImage } from '../actions'

class Post extends React.Component {

    render() {
        let post = this.props.post;
        let show_edit = (this.props.user && this.props.user.id == post.author && ! post.isEditing)
        let show_commentpanel = this.props.comments && this.props.comments.length > 0 || this.props.user

        return <div className="Post">
            <div className="header clearfix">
                <RoleThumbnail role={post.role} size="medium"/>
                <div className="post_data">
                    <div>
                        {post.role.user ? <UserName user={post.role.user} /> : <span className="UserName"><a href={'/' + post.role.page.permalink}>{post.role.page.name}</a></span>}
                    </div>
                    <div>
                        <span className="TimeStamp"><a href={post.permalink}>{Time.human(post.created)}</a></span>
                    </div>
                </div>
                {show_edit &&
                    <div>
                        <div className="DeletePostButton">
                            <a href="#" onClick={this.handleDelete}><i className="icon-cancel"></i></a>
                        </div>
                        <div className="EditPostButton">
                            <a href="#" onClick={this.handleEdit}><i className="icon-edit"></i></a>
                        </div>
                    </div>
                 }
            </div>
            {post.isEditing ?
                <Poster user={this.props.user} editpost={post} role={post.role} />
                :
                <div>
                    <div className="content">{post.content}</div>
                    <Images images={post.images} />
                </div>
            }

            {show_commentpanel &&
                <CommentPanel
                    comments={post.comments}
                    user={this.props.user}
                    post={post}
                    onAddComment={this.props.onAddComment}
                    onCommentDelete={this.props.onCommentDelete}
                    onUpload={this.props.onUpload}
                    onDeleteImage={this.props.onDeleteImage}
                    onEditComment={this.props.onEditComment}
                    onFinishEditComment={this.props.onFinishEditComment}
                    onDeleteEditCommentImage={this.props.onDeleteEditCommentImage}
                />
            }
        </div>
    }

    handleDelete = (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this post?')){
            // todo move it to redux
            jQuery.ajax({
                url: '/api/post/' + this.props.post.id,
                type: 'DELETE',
                success: function(result){
                    document.location.reload();
                },
                error: function(result){
                   alert(Strings.general_error);
                }
            });
        }
    }

    handleEdit = (e) => {
        e.preventDefault()
        this.props.onEditPost()
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        post: state.posts[ownProps.post.id],
        user: state.me,
    }
}

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        onCommentDelete: (comment_id) => {
            dispatch(commentDelete(ownProps.post.id, comment_id))
        },
        onAddComment: (rest_data) => {
            dispatch(addComment(rest_data, ownProps.post.id))
        },
        onEditPost: (post_id) => {
            dispatch(editPost(ownProps.post.id))
        },
        onUpload: (selector, file_input) => {
            dispatch(upload(ownProps.post.id, selector, file_input))
        },
        onDeleteImage: (selector) => {
            dispatch(deleteImage(ownProps.post.id, selector))
        },
        onDeleteEditCommentImage: (comment_id) => {
            dispatch(deleteEditCommentImage(ownProps.post.id, comment_id))
        },
        onEditComment: (comment_id) => {
            dispatch(editComment(ownProps.post.id, comment_id))
        },
        onFinishEditComment: (comment_id, rest_data) => {
            dispatch(finishEditComment(ownProps.post.id, comment_id, rest_data))
        },
    }
}

Post = connect(
    mapStateToProps,
    mapDispatchToProps
)(Post)

export default Post