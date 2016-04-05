import React from 'react'
import Upload from '../components/upload.js'
import UploadedImg from './UploadedImg.jsx'
import Strings from '../common_js/Strings.js'

export default React.createClass({

    getInitialState: function () {
        return {};
    },

    render: function () {
        var thumb;
        if (this.props.file.thumbnail)
            thumb = <UploadedImg thumbnail={this.props.file.thumbnail}/>;
        else
            thumb = <canvas width="60" height="60" ref="canvas"/>;

        return <div className="ImgUp">
            <span className="percentage">{this.stateString()}</span>
            {this.props.onImageDelete ? <a href="#" onClick={this.handleImageDelete} className="delete_button"><i className="icon-cancel"></i></a> : null}
            <span id="preview" ref="preview" className="thumb">
                {thumb}
            </span>
        </div>;
    },

    componentDidMount: function () {
        if (!this.props.file.id) {
            this.startUpload();
        }
    },

    stateString: function () {
        if (!this.state.finished && !this.props.file.id)
            return '' + Math.round(this.state.percent) + "%";
        return '';
    },

    handleImageDelete: function (e) {
        if (this.upload) {
            this.upload.abort();
        }
        this.props.onImageDelete(this.props.file);
        e.preventDefault();
    },

    startUpload: function () {
        this.upload = new Upload(this.props.file);
        this.upload.to('/upload');
        this.upload.on('progress', function (progress) {
            this.setState({'percent': progress.percent})
        }.bind(this));
        this.upload.on('error', function (a, b) {
            alert(Strings.error_image_upload);
        });
        this.upload.on('end', function (a, b) {
            this.setState({'percent': 100, 'finished': true});
            var resp = JSON.parse(a.responseText);
            if (!resp.success) {
                // TODO generalze API handling
                alert(resp.error);
                return;
            }
            var filename = resp.thumbnail;
            var image_id = resp.image_id;
            this.showImage(filename, image_id);
        }.bind(this));
    },

    showImage: function (image, image_id) {
        if (this.props.handleUploadComplete) {
            this.props.handleUploadComplete(this.props.file, image, image_id);
        }
    }
});
