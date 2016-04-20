import randomString from 'random-string';
import React from 'react';
import UploadImages from './UploadImages.jsx';
import Video from './Video.jsx';
import Strings from '../common_js/Strings.js';
import FileUploadButton from './FileUploadButton.jsx';
import RoleThumbnail from './RoleThumbnail.jsx';

class Poster extends React.Component {

    constructor(props) {
        super(props)
        this.state = {}
        if (props.editpost) {
            this.state.content = props.editpost.content
            this.state.images = props.editpost.images
        } else {
            this.state.content = ''
            this.state.images = []
        }
    }

    getMaxImgs() {
        return 12
    }

    render() {
        let max_imgs = this.getMaxImgs()

        return <div className="Poster clearfix">
            <RoleThumbnail role={this.props.role} />
            <div className="wrapper">
                <div>
                    {this.state.changed ?
                        <textarea
                            className="content"
                            onChange={this.updateTextArea}
                            ref="content"
                        />
                        :
                        <textarea
                            className="content"
                            onChange={this.updateTextArea}
                            value={this.state.content}
                            ref="content"
                        />
                    }
                </div>
                <UploadImages
                    images={this.state.images}
                    onImageDelete={this.handleImageDelete}
                    onUploadComplete={this.handleUploadComplete}
                />
                <table className="composer_footer">
                    <tbody>
                    <tr>
                        <td>
                            {(this.state.images.length < max_imgs) &&
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
        if (this.state.images.length + files.length > this.getMaxImgs()) {
            alert('Only ' + this.getMaxImgs() + ' images are allowed');
            return;
        }
        // files is of FileList type
        for (var i = 0; i < files.length; i++) {
            var f = files[i];
            f.key = randomString({length: 16});
            this.state.images.push(f);
        }
        this.setState({'images': this.state.images});
//        jQuery('#images').animate({'scrollLeft': 1000}, 1000);
    }

    handleImageDelete = (image) => {
        var i = this.state.images.indexOf(image);
        this.state.images.splice(i, 1);
        this.setState({'images': this.state.images});
    }

    handleUploadComplete = (image, thumbnail, image_id) => {
        var i = this.state.images.indexOf(image);
        this.state.images[i].thumbnail = thumbnail;
        this.state.images[i].image_id = image_id;
        this.setState({'images': this.state.images});
    }

    updateTextArea = () => {
        var content = this.refs.content;
        if (content.scrollHeight > content.clientHeight) {
            var new_height = content.scrollHeight + 12;
            if (new_height > 500) new_height = 500;
            content.style.height = new_height + "px";
        }
        this.setState({'content': content.value, 'changed': 1});
    }

    submit = () => {
        var image_ids = this.state.images.map(function (img) {
            if (img['image_id']) return img['image_id']; else return img['id'];
        });
        // TODO valoszinuleg kulon kellene szedni az ImgUp feltoltesi viselkedeset, es a torolheto thumbnail viselkedest
        var data = {
            images: image_ids.join(','),
            content: this.refs.content.value
        };
        if (this.props.wall) {
            data.wall = this.props.wall; // wall and role are not required when editing a post
            data.role = this.props.role.id;
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
        if (this.props.editpost) {
            args.url += '/' + this.props.editpost.id;
            args.type = 'PUT';
        }
        jQuery.ajax(args);
    }
}

export default Poster