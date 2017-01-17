import React from 'react'
import { connect } from 'react-redux'
import randomstring from 'random-string'
import _ from 'lodash'

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
import JsDiff from '../common_js/jsdiff.js'
import { commentDelete, addComment, editPost, upload, deleteImage, editComment, finishEditComment, cancelEditComment, flagContent, addFlag } from '../actions'

// swaps newlines to <br/>
class PostContent extends React.Component {

    render() {
        let content = this.props.post.content
        let elements = []

        let flag = this.props.post.flags[0]
        if (flag) {
            let diff = JsDiff.diffStringRaw(flag.original, flag.fixed)
            elements = this.format_diff(diff)
        } else {
            elements = this.format_diff({'text': content})
        }

        return <div className="post-content">{elements}</div>
    }

    add_text_with_br(arr, text){
        let with_br = this.add_br(text)
        if (_.isArray(with_br)){
            with_br.forEach(elem => arr.push(elem))
        } else {
            arr.push(with_br)
        }
    }

    // takes a diff (as returned by diffStringRaw)
    // output consists of 2 kinds of items:
    // * string
    // * html node; one of <br/> <a>...</a>, <span>...</span>. And this can make up a tree.
    format_diff(diff){
        let out = []

        for(let i=0; i<diff.length; i++){
            let current = diff[i]
            if (current.text){
                // http links are only converted to <a href=...> in unchanged text
                let http_urls = current.text.match(/https?:\/\/[^\s]+/g)
                if (http_urls == null){
                    this.add_text_with_br(out, current.text)
                } else {
                    let text = current.text
                    let parts
                    http_urls.forEach((str) => {
                        parts = text.split(str, 2)
                        this.add_text_with_br(out, parts[0])
                        out.push(`<a href="${str}">` + str + '</a>')
                        text = parts[1]
                    })
                    this.add_text_with_br(out, parts[1])
                }
            }
            else
            {
                if (current.removed == '')
                   current.removed = '...'
                out.push(<span className="del" key={randomstring()}>{this.add_br(current.removed)}</span>)
                if (current.added != ''){
                    out.push(<span className="add" key={randomstring()}>{this.add_br(current.added)}</span>)
                }
            }
        }

        return out
    }

    add_br(str){
        let m = str.split(/\n/)
        if (m.length == 1) {
            return str
        }
        let out=[]
        let i
        for (i=0; i<m.length-1; i++){
            out.push(m[i])
            out.push(<br/>)
        }
        out.push(m[i])
        return out
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
        let flag_button_active = post.isFlagging && ! post.flag  // TODO multiple flags

        return <div className="Post">
            <div className="header clearfix">

                {post.isFlagging == 'medic' &&
                    <MedicFlag
                        content_type="post"
                        content_id={post.id}
                        content={post.content}
                        onCancel={this.handleCancelFlagging}
                        onSubmit={this.props.onSubmitFlag}
                        active={flag_button_active}
                    />
                }
                {post.isFlagging == 'forbid' &&
                    <ForbidFlag
                        content_type="post"
                        content_id={post.id}
                        onCancel={this.handleCancelFlagging}
                        onSubmit={this.props.onSubmitFlag}
                        active={flag_button_active}
                    />
                }

                <RoleThumbnail role={post.role} size="medium" />
                <div className="post_data">
                    <div>
                        <RoleLink role={post.role} />
                        {guest_post && <span className="arrow"><i className="icon-right-dir"></i></span>}
                        {guest_post && <RoleLink role={post.wall} />}
                    </div>
                    <div className="post_created_modified">
                        <CreatedModified created={post.created} modified={post.modified} />
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
                    <PostContent post={post} />
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
                    onSubmitFlag={this.props.onSubmitFlag}
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
        onSubmitFlag: (content_type, content_id, flag_data) => {
            dispatch(addFlag(ownProps.post.id, content_type, content_id, flag_data))
        }
    }
}

Post = connect(
    mapStateToProps,
    mapDispatchToProps
)(Post)

export default Post