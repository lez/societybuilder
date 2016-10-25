import React from 'react'
import { connect } from 'react-redux'

import RoleThumbnail from './RoleThumbnail.jsx'
import RoleLink from './RoleLink.jsx'
import Images from './Images.jsx'
import Poster from './Poster.jsx'
import MedicFlag from './MedicFlag.jsx'
import FlagMenu from './FlagMenu.jsx'
import ForbidFlag from './ForbidFlag.jsx'
import CommentPanel from './CommentPanel.jsx'
import CreatedModified from './CreatedModified.jsx'
import Time from '../common_js/Time.js'
import { commentDelete, addComment, editPost, upload, deleteImage, editComment, finishEditComment, cancelEditComment, flagContent } from '../actions'

// swaps newlines to <br/>
class PostContent extends React.Component {
    linkify(str, pattern) {
        let url = str.replace(pattern, '$2')
        return <a href={url} rel="nofollow">{url}</a>
    }

    render() {
        let lines = this.props.children.split('\n')
        let elements = []
        for (let x of lines) {
            let pattern = /(.*)(https?:\/\/[^ ]*)(.*)/
            if (x.search(/https?:\/\//) >= 0){
                let leftright = x.split(/https?:\/\/[^ ]*/)
                elements.push(leftright[0])
                elements.push(this.linkify(x, pattern))
                elements.push(leftright[1])
            } else {
                elements.push(x)
            }
            elements.push(<br/>)
        }
        elements.pop()
        return <div className="post-content">{elements}</div>
    }
}

class Post extends React.Component {

    render() {
        let post = this.props.post;
        let show_edit = (this.props.user && this.props.user.id == post.author && ! post.isEditing)
        let show_flagmenu = (this.props.user && this.props.user.id != post.author) && ! post.isFlagging
        let show_commentpanel = this.props.comments && this.props.comments.length > 0 || this.props.user

        let wall_id = post.wall.user ? `user:${post.wall.user.id}` : `page:${post.wall.page.id}`
        let guest_post = wall_id !== post.role.id

        return <div className="Post">
            <div className="header clearfix">

                {post.isFlagging == 'medic' &&
                    <MedicFlag content={post.content} onCancel={this.handleCancelFlagging}/>
                }
                {post.isFlagging == 'forbid' &&
                    <ForbidFlag onCancel={this.handleCancelFlagging}/>
                }

                <RoleThumbnail role={post.role} size="medium"/>
                <div className="post_data">
                    <div>
                        <RoleLink role={post.role} />
                        {guest_post &&
                            [<span className="arrow"><i className="icon-right-dir"></i></span>, <RoleLink role={post.wall} />]
                        }
                    </div>
                    <div className="post_created_modified">
                        <CreatedModified created={post.created} modified={post.modified}/>
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

                {show_flagmenu &&
                    <FlagMenu
                        onClickMedic={this.handleMedic}
                        onClickForbid={this.handleForbid}
                    />
                }

            </div>
            {post.isEditing ?
                <Poster user={this.props.user} post={post} role={post.role} />
                :
                <div>
                    <PostContent>{post.content}</PostContent>
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
                    onCancelEditComment={this.props.onCancelEditComment}
                    onDeleteImage={this.props.onDeleteImage}
                    onEditComment={this.props.onEditComment}
                    onFinishEditComment={this.props.onFinishEditComment}
                    onDeleteEditCommentImage={this.props.onDeleteEditCommentImage}
                    onFlagContent={this.props.onFlagContent}
                />
            }
        </div>
    }

    handleMedic = (e) => {
        e.preventDefault()
        this.props.onFlagContent('post', 'medic')
    }

    handleForbid = (e) => {
        e.preventDefault()
        this.props.onFlagContent('post', 'forbid')
    }

    handleCancelFlagging = (e) => {
        e.preventDefault()
        this.props.onFlagContent('post', null)
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
        onEditComment: (comment_id) => {
            dispatch(editComment(ownProps.post.id, comment_id))
        },
        onFinishEditComment: (comment_id, rest_data) => {
            dispatch(finishEditComment(ownProps.post.id, comment_id, rest_data))
        },
        onCancelEditComment: (comment_id) => {
            dispatch(cancelEditComment(ownProps.post.id, comment_id))
        },
        onFlagContent: (content_type, flag, comment_id=null) => {
            dispatch(flagContent(ownProps.post.id, content_type, flag, comment_id))
        },
    }
}

Post = connect(
    mapStateToProps,
    mapDispatchToProps
)(Post)

export default Post