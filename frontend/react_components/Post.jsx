import React, { PropTypes } from 'react'
import { connect } from 'react-redux'
import randomstring from 'random-string'
import _ from 'lodash'
import { Tooltip, OverlayTrigger } from 'react-bootstrap'
import RoleThumbnail from './RoleThumbnail.jsx'
import RoleLink from './RoleLink.jsx'
import Images from './Images.jsx'
import Poster from './Poster.jsx'
import MedicFlag from './MedicFlag.jsx'
import FlagMenu from './FlagMenu.jsx'
import EditMenu from './EditMenu.jsx'
import ForbidFlag from './ForbidFlag.jsx'
import ShowFlag from './ShowFlag.jsx'
import CommentPanel from './CommentPanel.jsx'
import CreatedModified from './CreatedModified.jsx'
import Time from '../common_js/Time.js'
import JsDiff from '../common_js/jsdiff.js'

import { commentDelete, addComment, editPost, upload, deleteImage, editComment, finishEditComment, cancelEditComment, flagContent, addFlag, showPostFlag, closePostFlag } from '../actions'

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
                if (current.add != ''){
                    let tooltip_text
                    let tooltip
                    if (! this.props.post.show_flag){
                        if (current.remove == '') tooltip_text = current.add
                        else tooltip_text = 'Javasolt: ' + current.add
                        tooltip = <Tooltip id="tooltip">{tooltip_text}</Tooltip>
                    } else {
                        if (current.remove == '') tooltip_text = 'hozzáadva'
                        else tooltip_text = current.remove
                        tooltip = <Tooltip id="tooltip"><span class="tooltip_remove">{tooltip_text}</span></Tooltip>
                    }


                    if (current.remove == '')
                       current.remove = '...'

                    let x
                    if (this.props.post.show_flag){
                        x = <span className="add" key={randomstring()} onClick={this.props.onCloseFlag}>{this.add_br(current.add)}</span>
                    } else {
                        x = <span className="remove" key={randomstring()} onClick={this.show_flag}>{this.add_br(current.remove)}</span>
                    }
                    out.push(
                        <OverlayTrigger placement="top" overlay={tooltip} key={randomstring()}>
                            {x}
                        </OverlayTrigger>
                    )
                } else {
                    if (!this.props.post.show_flag){
                        out.push(<span className="remove" key={randomstring()}>{this.add_br(current.remove)}</span>)
                    }
                }
            }
        }

        return out
    }

    show_flag = () => {
        this.props.onShowPostFlag(1)
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

PostContent.propTypes = {
    post: PropTypes.object.isRequired,
    onCloseFlag: PropTypes.func.isRequired,
    onShowPostFlag: PropTypes.func.isRequired,
}


class Post extends React.Component {

    render() {
        let post = this.props.post;
        let can_edit = (this.props.user && this.props.user.id == post.author && ! post.isEditing)
        let is_author = (this.props.user && this.props.user.id == post.author)
        let show_flagmenu = (this.props.user && this.props.user.id != post.author) && ! post.isFlagging
        let show_commentpanel = this.props.comments && this.props.comments.length > 0 || this.props.user

        let wall_id = post.wall.user ? `user:${post.wall.user.id}` : `page:${post.wall.page.id}`
        let guest_post = wall_id !== post.role.id
        let flag_button_active = post.isFlagging && ! post.flag  // TODO multiple flags

        return <div className="Post">
            <div className="header clearfix">

                {post.show_flag &&
                    <ShowFlag
                        flag={post.flags[0]}
                        onClose={this.handleCloseFlag}
                        onAccept={this.handleAcceptFlag}
                        // onAgree={this.props.onAgreeFlag}
                        // onDisagree={this.props.onDisagreeFlag}
                        is_author={is_author}
                    />
                }

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

                {can_edit &&
                    <EditMenu
                        onClickEdit={this.handleEdit}
                        onClickDelete={this.handleDelete}
                    />
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
                    <PostContent post={post} onShowPostFlag={this.props.onShowPostFlag} onCloseFlag={this.handleCloseFlag} />
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

    handleCloseFlag = (e) => {
        e.preventDefault()
        this.props.onCloseFlag()
    }

    handleAcceptFlag = () => {
        console.log('handleAcceptFlag')
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
        },
        onShowPostFlag: (flag_id) => {
            dispatch(showPostFlag(ownProps.post.id, flag_id))
        },
        onCloseFlag: () => {
            dispatch(closePostFlag(ownProps.post.id))
        },
    }
}

Post = connect(
    mapStateToProps,
    mapDispatchToProps
)(Post)

export default Post