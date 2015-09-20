var React = require('react');
var Upload = require('../components/upload.js');
var UploadedImg = require('./UploadedImg.jsx');

var ImgUp = React.createClass({

  getInitialState: function() {
    return {"percent": 0};
  },

  render: function() {
    if (this.props.file.thumbnail)
      var thumb = <UploadedImg file={this.props.file.thumbnail} />
    else
      var thumb = <canvas width="60" height="60" ref="canvas" />

    return (
      <div className="ImgUp">
        <span className="percentage">{this.stateString()}</span>
        {this.props.onImageDelete?<a href="#" onClick={this.del} className="delete_button"><i className="icon-cancel"></i></a>:null}
        <span id="preview" ref="preview" className="thumb">
          {thumb}
        </span>
      </div>
    );
  },

  componentDidMount: function() {
    this.startUpload();
  },

  stateString: function() {
    if (!this.state.finished)
      return '' + Math.round(this.state.percent) + "%";
    return '';
  },

  del: function() {
    this.up.abort();
    this.props.onImageDelete(this.props.file);
  },

  startUpload: function (){
    this.up = new Upload(this.props.file);
    this.up.to('/upload');
    this.up.on('progress', function(progress){this.setState({'percent': progress.percent})}.bind(this));
    this.up.on('error', function(a,b){alert('hiba a képek feltöltésénél!');});
    this.up.on('end', function(a,b){
      this.setState({'percent': 100, 'finished': true});
      var resp = JSON.parse(a.responseText);
      if (!resp.success){
        alert(resp.error);
        return;
      }
      var filename = resp.thumbnail;
      var image_id = resp.image_id;
      this.showImage(filename, image_id);
    }.bind(this));
  },

  showImage: function(image, image_id) {

    this.props.onUploadComplete(this.props.file, image, image_id);
  }
});

module.exports = ImgUp;
