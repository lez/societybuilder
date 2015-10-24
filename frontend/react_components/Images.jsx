var React = require('react');
var Thumbnail = require('./Thumbnail.jsx');

var Images = React.createClass({
  render: function() {
    var images = this.props.images;
    return (
      <div className="Images clearfix">
        {images.map(function(image){
          return <Thumbnail key={image.id} image={image.thumbnail} size="large" />;
        })}
      </div>
    );
  }
});

module.exports = Images;