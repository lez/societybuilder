var React = require('react');
var ImgUp = require('./ImgUp.jsx');

var UploadImages = React.createClass({

  render: function() {
    var onImageDelete = this.props.onImageDelete;
    var onUploadComplete = this.props.onUploadComplete;
    var images = this.props.images;
    var computed_classname = '';
    if (this.props.images.length > 4)
      computed_classname = 'higher';
    return (
      <div id="images" className={computed_classname}>
        {images.map(function(image){
          return <ImgUp key={image.key} file={image} onImageDelete={onImageDelete} onUploadComplete={onUploadComplete} />;
        })}
      </div>
    );
  }

});


module.exports = UploadImages;