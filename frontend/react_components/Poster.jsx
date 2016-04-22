import React from 'react'
import { connect } from 'react-redux'

import UploadImages from './UploadImages.jsx'
import Video from './Video.jsx'
import Strings from '../common_js/Strings.js'
import FileUploadButton from './FileUploadButton.jsx'
import RoleThumbnail from './RoleThumbnail.jsx'

import { addPostImage, deletePostImage } from '../actions'

class Poster extends React.Component {

    state = {}

    getMaxImgs() {
        return 12
    }
    render() {
        let post = this.props.post
        let max_imgs = this.getMaxImgs()

        let default_value = post.content ? post.content : ''

        return <div className="Poster clearfix">
            <RoleThumbnail role={this.props.role} />
            <div className="wrapper">
                <div>
                    <textarea
                        className="content"
                        onChange={this.updateTextArea}
                        ref="content"
                        defaultValue={default_value}
                    />
                </div>
                <UploadImages
                    images={post.images}
                    onImageDelete={this.handleDeleteImage}
                />
                <table className="composer_footer">
                    <tbody>
                    <tr>
                        <td>
                            {(post.images.length < max_imgs) &&
                                <FileUploadButton multiple="1" upload={this.handleUploadStart}>
                                    <i className="icon-camera"/>
                                </FileUploadButton>
                            }
                        </td>
                        <td/>
                        <td>
                            <input type="submit" className="post-button ns2_btn1" name="post" value="Küldés" onClick={this.submit}/>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    }

    handleUploadStart = (files) => {
        if (this.props.post.images.length + files.length > this.getMaxImgs()) {
            alert(`Only ${this.getMaxImgs()} images are allowed`)
            return
        }
        // files is of FileList type
        for (var i = 0; i < files.length; i++) {
            this.props.onAddImage(files[i])
        }
//        jQuery('#images').animate({'scrollLeft': 1000}, 1000);
    }

    handleDeleteImage = (image) => {
        console.log(image)
        this.props.onDeleteImage(image.key)
    }

    updateTextArea = () => {
        var content = this.refs.content;
        if (content.scrollHeight > content.clientHeight) {
            var new_height = content.scrollHeight + 12;
            if (new_height > 500) new_height = 500;
            content.style.height = new_height + "px";
        }
    }

    submit = () => {
        var image_ids = this.props.post.images.map(img => img.id)
        var data = {
            images: image_ids.join(','),
            content: this.refs.content.value
        }
        if (this.props.wall) {
            data.wall = this.props.wall // wall and role are not required when editing a post
            data.role = this.props.role.id
        }
        var args = {
            url: '/api/post',
            type: 'POST',
            data: data,
            success: function (result) {
                document.location.reload();
            },
            error: function (result) {
                alert(Strings.general_error);
            }
        };
        if (this.props.post.isEditing) {
            args.url += '/' + this.props.post.id;
            args.type = 'PUT';
        }
        jQuery.ajax(args);
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        post: state.posts[ownProps.post.id],
        user: state.me,
        role: ownProps.role,
        wall: ownProps.wall,
    }
}

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        onAddImage: (file) => {
            dispatch(addPostImage(ownProps.post.id, file))
        },
        onDeleteImage: (key) => {
            dispatch(deletePostImage(ownProps.post.id, key))
        },
    }
}

Poster = connect(
    mapStateToProps,
    mapDispatchToProps
)(Poster)

export default Poster


