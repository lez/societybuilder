import React from 'react';
import ImgUp from './ImgUp.jsx';
import randomString from 'random-string';

export default React.createClass({

    render: function () {

        var computed_classname = (this.props.images.length > 4) ? 'higher' : '';

        var imgups = [];
        for (var i = 0; i < this.props.images.length; i++) {
            var image = this.props.images[i];
            if (!image.key) image.key = randomString(16);
            imgups.push(<ImgUp key={image.key} image={image} onImageDelete={this.props.onImageDelete} />);
        }

        return <div className={"UploadImages " + computed_classname}>
            {imgups}
        </div>;
    }

});

