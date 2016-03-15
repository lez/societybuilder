var randomString = require('random-string');
var React = require('react');
var UploadImages = require('./UploadImages.jsx');
var Video = require('./Video.jsx');
var Roles = require('./Roles.jsx');
var Strings = require('../common_js/Strings.js');
var FileUploadButton = require('./FileUploadButton.jsx');

var Poster = React.createClass({
    getInitialState: function () {
        if (this.props.editpost) {
            return {
                imgs: this.props.editpost.images,
                content: this.props.editpost.content,
                changed: 0
            }
        } else {
            return {
                imgs: [],
                content: '',
                changed: 0,
                role: this.props.role.id
            }
        }
    },

    getMaxImgs: function () {
        return 12;
    },

    handleChangeRole: function (role) {
        this.setState({role: role});
    },

    render: function () {
        var max_imgs = this.getMaxImgs();

        return (
            <div className="Poster clearfix">
                <Roles roles={this.props.roles} current={this.state.role} onChangeRole={this.handleChangeRole}/>
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
                        images={this.state.imgs}
                        onImageDelete={this.handleImageDelete}
                        onUploadComplete={this.handleUploadComplete}
                    />
                    <table className="composer_footer">
                        <tbody>
                        <tr>
                            <td>
                                {(this.state.imgs.length < max_imgs) ?
                                    <FileUploadButton multiple="1" upload={this.handleUploadStart}>
                                        <i className="icon-camera"/>
                                    </FileUploadButton>
                                    : null}
                            </td>
                            <td/>
                            <td>
                                <input type="submit" className="post-button ns2_btn1" name="post" value="Küldés"
                                       onClick={this.submit}/>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        );
    },

    handleUploadStart: function (files) {
        if (this.state.imgs.length + files.length > this.getMaxImgs()) {
            alert('Only ' + this.getMaxImgs() + ' images are allowed');
            return;
        }
        // files is of FileList type
        for (var i = 0; i < files.length; i++) {
            var f = files[i];
            f.key = randomString({length: 16});
            this.state.imgs.push(f);
        }
        this.setState({'imgs': this.state.imgs});
//        jQuery('#images').animate({'scrollLeft': 1000}, 1000);
    },

    handleImageDelete: function (image) {
        var i = this.state.imgs.indexOf(image);
        this.state.imgs.splice(i, 1);
        this.setState({'imgs': this.state.imgs});
    },

    handleUploadComplete: function (image, thumbnail, image_id) {
        var i = this.state.imgs.indexOf(image);
        this.state.imgs[i].thumbnail = thumbnail;
        this.state.imgs[i].image_id = image_id;
        this.setState({'imgs': this.state.imgs});
    },

    updateTextArea: function () {
        var content = this.refs.content;
        if (content.scrollHeight > content.clientHeight) {
            var new_height = content.scrollHeight + 12;
            if (new_height > 500) new_height = 500;
            content.style.height = new_height + "px";
        }
        this.setState({'content': content.value, 'changed': 1});
    },

    submit: function () {
        var image_ids = this.state.imgs.map(function (img) {
            if (img['image_id']) return img['image_id']; else return img['id'];
        });
        // TODO valoszinuleg kulon kellene szedni az ImgUp feltoltesi viselkedeset, es a torolheto thumbnail viselkedest
        var data = {
            images: image_ids.join(','),
            content: this.refs.content.value
        };
        if (this.props.wall) {
            data.wall = this.props.wall; // wall and role are not required when editing a post
            data.role = this.state.role;
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
});

module.exports = Poster;
