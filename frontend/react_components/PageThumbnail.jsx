import React from 'react';
import Thumbnail from './Thumbnail.jsx';

export default React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {
        var size = this.props.size ? this.props.size : 'small';

        if (this.props.page.image) {
            return <Thumbnail image={this.props.page.image.thumbnail} size={size}/>;
        }
        else {
            return <Thumbnail image="icon-box" size={size}/>;
        }
    }
});
