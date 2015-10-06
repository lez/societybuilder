var randomString = require('random-string');
var React = require('react');
var UploadImages = require('./UploadImages.jsx');
var Video = require('./Video.jsx');
var Strings = require('../common_js/Strings.js');
var FileUploadButton = require('./FileUploadButton.jsx');

var Poster = React.createClass({
  getInitialState: function() {
    return {
      'imgs': []
    }
  },

  getMaxImgs: function() {
    return 12;
  },

  render: function() {
    var image_delete = this.onImageDelete;
    var upload_complete = this.onUploadComplete;
    var remove_video = this.onRemoveVideo;
    var max_imgs = this.getMaxImgs();

    return (
      <div className="Poster">
        <div className="wrapper">
          <div>
            <textarea
              className="content"
              ref="content"
              onChange={this.updateTextArea}
            />
          </div>
          <UploadImages
            images={this.state.imgs}
            onImageDelete={image_delete}
            onUploadComplete={upload_complete}
          />
          <table className="composer_footer">
            <tr>
              <td>
                {(this.state.imgs.length < max_imgs) ?
                <FileUploadButton multiple="1" upload={this.upload}>
                  <i className="icon-camera"></i>
                </FileUploadButton> : null}
              </td>
              <td></td>
              <td>
                <input type="submit" className="post-button ns2_btn1" name="post" value="Küldés" onClick={this.submit} />
              </td>
            </tr>
          </table>
        </div>
      </div>
    );
  },

  upload: function(files) {
    if (this.state.imgs.length + files.length > this.getMaxImgs()){
      alert('Only '+this.getMaxImgs()+' images are allowed');
      return;
    }
    // files is of FileList type
    for (var i=0; i<files.length; i++){
      var f = files[i];
      f.key = randomString({length: 16});
      this.state.imgs.push(f);
    }
    this.setState({'imgs': this.state.imgs});
//    jQuery('#images').animate({'scrollLeft': 1000}, 1000);
  },

  onImageDelete: function(image){
    var i = this.state.imgs.indexOf(image);
    this.state.imgs.splice(i, 1);
    this.setState({'imgs': this.state.imgs});
  },

  onUploadComplete: function(image, thumbnail, image_id){
    var i = this.state.imgs.indexOf(image);
    this.state.imgs[i].thumbnail = thumbnail;
    this.state.imgs[i].image_id = image_id;
    this.setState({'imgs': this.state.imgs});
  },

  updateTextArea: function(){
    var content = this.refs.content.getDOMNode();
    if (content.scrollHeight > content.clientHeight) {
      var new_height = content.scrollHeight+12;
      if (new_height > 500) new_height = 500;
      content.style.height =  new_height + "px";
    }
  },

  submit: function() {
    var data = {
      image_ids: this.state.imgs.map(function (img){return img['image_id']}),
      content: this.refs.content.getDOMNode().value,
    };
    jQuery.ajax({
      url: '/api/post',
      type: 'POST',
      data: data,
      success: function(result){
        if (!result.success) {
          alert(result.error ? result.error : Strings.general_error);
        } else {
          document.location.reload();
        }
      }.bind(this),
      error: function(result){
        alert(Strings.general_error);
      }.bind(this)
    });
  }
});

module.exports = Poster;
