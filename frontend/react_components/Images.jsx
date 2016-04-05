import React from 'react';
import Thumbnail from './Thumbnail.jsx';

export default React.createClass({
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
