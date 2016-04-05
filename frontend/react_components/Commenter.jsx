import randomString from 'random-string';
import React from 'react';
import ImgUp from './ImgUp.jsx';
import UserThumbnail from './UserThumbnail.jsx';
import FileUploadButton from './FileUploadButton.jsx';

export default React.createClass({
    getInitialState: function () {
        return {
            'image': null,
            'key': randomString(8),
            'submitting': false
        }
    },

    render: function () {
        var image = this.state.image;
        var file = this.state.file;
        var key = this.state.key;

        return <div className="Commenter clearfix" key={key}>
            <UserThumbnail user={this.props.user} />
            <div className="middle_column">
                <textarea
                    className="inputtext"
                    disabled={this.state.submitting}
                    onChange={this.updateBoxHeight}
                    onKeyDown={this.checkSubmit}
                    ref="content"
                />
                {file ? <ImgUp file={file} onImageDelete={this.handleImageDelete} onUploadComplete={this.handleUploadComplete} /> : null}
            </div>
            {file ? null : <FileUploadButton upload={this.upload}><i className="demo-icon icon-camera"></i></FileUploadButton>}
        </div>;
    },

    upload: function (file) {
        var f = file;
        if (f) {
            f.key = randomString({length: 16});
            this.setState({'file': f});
        }
        this.refs.content.focus();
    },

    handleImageDelete: function (image) {
        this.setState({'file': null, 'image': null});
        this.refs.content.focus();
    },

    handleUploadComplete: function (image, thumbnail, image_id) {
        alert('upl comp');
        var file = this.state.file;
        file.thumbnail = thumbnail;
        file.id = image_id;
        this.setState({'file': file});
    },

    checkSubmit: function (e) {
        // send comment with ENTER
        if (e.keyCode == 13) {
            e.preventDefault();
            this.submit();
        }
    },

    updateBoxHeight: function (e) {
        var content = this.refs.content;
        if (content.scrollHeight > content.clientHeight) {
            var new_height = content.scrollHeight + 12;
            if (new_height > 500) new_height = 500;
            content.style.height = new_height + "px";
        }
    },

    submit: function () {
        if (this.state.submitting) return false;
        this.setState({'submitting': true});
        var data = {
            comment: this.refs.content.value,
            item_type: 'post',
            item_id: this.props.post.id
        };
        if (this.state.file && this.state.file.id)
            data.image = this.state.file.id;

        jQuery.ajax({
            url: '/api/comment',
            type: 'POST',
            data: data,
            success: function (result) {
                if (this.props.append) {
                    this.props.append(result);
//            element.animate({'scrollTop': element[0].scrollHeight}, 200);
                    this.replaceState(this.getInitialState());
                    this.setState({'key': randomString(8)});
                } else {
                    document.location.reload();
                }
            }.bind(this),
            error: function (result) {
                alert('An error occured');
                this.setState({'submitting': false});
            }.bind(this)
        });
    }
});
