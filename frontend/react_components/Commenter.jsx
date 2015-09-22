var randomString = require('random-string');
var React = require('react');
var ImgUp = require('./ImgUp.jsx');
var FileInputButton = require('./FileInputButton.jsx');

var Commenter = React.createClass({
  getInitialState: function() {
    return {
      'image': null,
      'key': randomString(8),
      'submitting': false
    }
  },

  render: function() {
    var image_delete = this.onImageDelete;
    var upload_complete = this.onUploadComplete;
    var image = this.state.image;
    var file = this.state.file;
    var key = this.state.key;

    return (
      <div className="Commenter clearfix" key={key}>
        <div>
          <img className="thumbnail" src={this.props.user.thumbnail}/>
          <textarea
            className="content"
            ref="content"
            onKeyDown={this.checkSubmit}
            onChange={this.updateBoxHeight}
            disabled={this.state.submitting}
          />
          {!file ? <FileInputButton upload={this.upload}>x</FileInputButton> : null}
        </div>
        {file ? <ImgUp file={file} onImageDelete={image_delete} onUploadComplete={upload_complete} /> : null}
      </div>
    );
  },

  upload: function(file) {
    f = file;
    if (f) {
      f.key = randomString({length: 16});
      this.setState({'file': f});
    }
  },

  onImageDelete: function(image){
    this.setState({'file': null, 'image': null});
  },

  onUploadComplete: function(image, thumbnail, image_id){
    var image = {'thumbnail':thumbnail, 'id': image_id};
    var file = this.state.file;
    file.thumbnail = thumbnail;
    this.setState({'image': image, 'file': file});
  },

  checkSubmit: function(e) {
    // send comment with ENTER
    if (e.keyCode == 13) {
      e.preventDefault();
      this.submit();
    }
  },

  updateBoxHeight: function(e) {
    var content = this.refs.content.getDOMNode();
    if (content.scrollHeight > content.clientHeight) {
      var new_height = content.scrollHeight+12;
      if (new_height > 500) new_height = 500;
      content.style.height =  new_height + "px";
    }
  },

  submit: function() {
    if (this.state.submitting) return false;
    this.setState({'submitting': true});
    var data = {
      user_id: this.props.user_id,
      comment: this.refs.content.getDOMNode().value,
      item_type: this.props.item_type,
      item_id: this.props.item_id
    };
    if (this.state.image)
      data.image_id = this.state.image.image_id;

    jQuery.ajax({
      url: '/req/rest/comment.php',
      type: 'POST',
      data: data,
      success: function(result){
        var replydata = JSON.parse(result);
        if (!replydata.success) {
          alert(replydata.error);
          this.setState({'submitting': false});
        } else {
          if (this.props.appendto){
            var element = jQuery('#' + this.props.appendto);
            element.append(replydata.comment);
            element.animate({'scrollTop': element[0].scrollHeight}, 200);
            this.replaceState(this.getInitialState());
            this.setState({'key': randomString(8)});
          } else {
            document.location.reload();
          }
        }
      }.bind(this),
      error: function(result){
        this.setState({'submitting': false});
      }.bind(this)
    });
  }
});

module.exports = Commenter;
