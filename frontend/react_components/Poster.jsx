var randomString = require('random-string');
var React = require('react');
var Images = require('./Images.jsx');
var Video = require('./Video.jsx');

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
          <Images
            images={this.state.imgs}
            onImageDelete={image_delete}
            onUploadComplete={upload_complete}
          />
          {this.state.video?<Video
            video={this.state.video}
            onRemoveVideo={remove_video}
          />:null}
          <table className="composer_footer">
            <tr>
              <td>
                {(this.state.imgs.length < max_imgs) ?
                <span className="fileinput-button">
                  <img src="/images/icons/photoupload.png" />
                  <span>kép</span>
                  <input
                    type="file"
                    name="selected-files"
                    multiple={comment ? 0 : 1}
                    onChange={this.upload}
                    ref="selectedfiles"
                  />
                </span> : null}
              </td>
              <td></td>
              <td>
                <input type="submit" className="post-button ns2_btn1" name="post" value="Küldés" onClick={this.submit}></input>
              </td>
            </tr>
          </table>
        </div>
      </div>
    );
  },

  upload: function() {
    var input = this.refs.selectedfiles.getDOMNode();
    // input.files in itself is of FileList type
    for (var i=0; i<input.files.length; i++){
      if (this.state.imgs.length >= this.getMaxImgs()){
        alert('Jelenleg csak '+this.getMaxImgs()+' képet tudsz feltölteni egy hozzászóláshoz!');
        break;
      }
      var f = input.files[i];
      f.key = randomString({length: 16});
      this.state.imgs.push(f);
    }
    this.setState({'imgs': this.state.imgs});
    jQuery('#images').animate({'scrollLeft': 1000}, 1000);
  },

  onImageDelete: function(image){
    var i = this.state.imgs.indexOf(image);
    this.state.imgs.splice(i,1);
    this.setState({'imgs': this.state.imgs});
  },

  onUploadComplete: function(image, thumbnail, image_id){
    var i = this.state.imgs.indexOf(image);
    this.state.imgs[i].thumbnail = thumbnail;
    this.state.imgs[i].image_id = image_id;
    this.setState({'imgs': this.state.imgs});
  },

  onRemoveVideo: function() {
    this.setState({'video': null, 'video_removed': true});
    return false;
  },

  updateTextArea: function(){
    var content = this.refs.content.getDOMNode();
    if (content.scrollHeight > content.clientHeight) {
      var new_height = content.scrollHeight+12;
      if (new_height > 500) new_height = 500;
      content.style.height =  new_height + "px";
    }

    // youtube videos:
    if (!this.state.video_removed && !this.state.video){
      var match = content.value.match(/(youtube\.com)\/(v\/|u\/|embed\/|watch\?v=)([^#\&\?]{11})/i);
      if (match){
        jQuery.ajax({
          url: '/req/rest/video.php',
          type: 'GET',
          data: {'url': 'http://www.'+match[0]},
          success: function(result) {
            var replydata = JSON.parse(result);
            if (replydata.success) {
              this.setState({'video': replydata.video});
            }
          }.bind(this)
        });
        console.log(match);
      }
    }
  },

  submit: function() {
    if (this.submitting) return false;
    this.submitting = true;
    var image_ids = [];
    for (var i=0; i<this.state.imgs.length; i++){
      image_ids.push(this.state.imgs[i].image_id);
    }
    var data = {
      image_ids: image_ids,
      comment: this.refs.content.getDOMNode().value,
    };
    if (this.props.reply_id) data.reply_id = this.props.reply_id;
    if (this.state.video) data.video_url = this.state.video.url;
    jQuery.ajax({
      url: '/api/content',
      type: 'POST',
      data: data,
      success: function(result){
        var replydata = JSON.parse(result);
        if (!replydata.success) {
          alert(replydata.error);
          this.submitting = false;
        }
        else
          document.location.reload();
      }.bind(this),
      error: function(result){
        this.submitting = false;
      }.bind(this)
    });
  }
});

module.exports = Poster;
