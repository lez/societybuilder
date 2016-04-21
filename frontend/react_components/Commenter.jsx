import _ from 'lodash'
import React, { PropTypes } from 'react'

import ImgUp from './ImgUp.jsx'
import UserThumbnail from './UserThumbnail.jsx'
import FileUploadButton from './FileUploadButton.jsx'

class Commenter extends React.Component {

    constructor(props) {
        super(props)
        if (this.props.comment.isEditing)
            this.selector = `comments.find(function(c){return c.id===${this.props.comment.id}})`  // whoa
        else
            this.selector = 'newComment'
    }

    render() {
        let has_image = !_.isEmpty(this.props.comment.image)

        return <div className="Commenter clearfix">
            <UserThumbnail user={this.props.user} />
            <div className="middle_column">
                <textarea
                    className="inputtext"
                    disabled={!this.props.isActive}
                    onChange={this.updateBoxHeight}
                    onKeyDown={this.checkSubmit}
                    ref="content"
                    defaultValue={this.props.comment.comment}
                />
                {has_image && <ImgUp image={this.props.comment.image} onImageDelete={this.handleImageDelete} />}
            </div>
            {!has_image && <FileUploadButton upload={this.upload}><i className="demo-icon icon-camera"></i></FileUploadButton>}
            {this.props.comment.isEditing && 
                <span><a href="#" onClick={this.handleCancel}>cancel</a></span>
            }
        </div>
    }

    handleCancel = (e) => {
        e.preventDefault()
        this.props.onCancelEditComment(this.props.comment.id)
    }

    upload = (file) => {
        if (file) {
            this.props.onUpload(this.selector, file)
        }
        this.refs.content.focus()
    }

    handleImageDelete = () => {
        this.refs.content.focus()
        this.props.onDeleteImage(this.selector)
    }

    checkSubmit = (e) => {
        // send comment with ENTER
        if (e.keyCode == 13) {
            e.preventDefault();
            this.submit();
        }
    }

    updateBoxHeight = (e) => {
        var content = this.refs.content;
        if (content.scrollHeight > content.clientHeight) {
            var new_height = content.scrollHeight + 12;
            if (new_height > 500) new_height = 500;
            content.style.height = new_height + "px";
        }
    }

    submit = () => {
        if (!this.props.isActive) return false
        var data = {
            comment: this.refs.content.value
        }
        if (this.props.comment.image){
            if (this.props.comment.image.isUploading) {
                alert('a kep meg feltoltes alatt!')
                return
            } else if (this.props.comment.image.id) {
                data.image = this.props.comment.image.id
            } else {
                data.image = ''
            }
        } else {
            data.image = ''
        }

        if (this.props.comment.isEditing)
            this.props.onFinishEditComment(this.props.comment.id, data)
        else
            this.props.onAddComment(data)
    }
}

Commenter.propTypes = {
    onDeleteImage: PropTypes.func,
    onDeleteEditCommentImage: PropTypes.func,
    onAddComment: PropTypes.func,
    onFinishEditComment: PropTypes.func,
    comment: PropTypes.object,
    onUpload: PropTypes.func.isRequired,
    onCancelEditComment: PropTypes.func
}

export default Commenter