var React = require('react');
var Thumbnail = require('./Thumbnail.jsx');

var Images = React.createClass({
    render: function () {
        var imgs = [];
        for (var i = 0; i < this.props.images.length; i++) {
            var image = this.props.images[i];
            imgs.push(<Thumbnail key={image.id} image={image.thumbnail} size="large"/>);
        }

        return <div className="Images clearfix">
            {imgs}
        </div>;
    }
});

module.exports = Images;