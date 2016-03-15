var React = require('react');
var Util = require('../common_js/util.js');

var dimensions = {
    micro: '15x15',
    small: '30x30',
    medium: '60x60',
    large: '100x100'
};

var Thumbnail = React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {
        var content;
        var size = this.props.size ? this.props.size : 'small';
        var dimension = dimensions[size];

        if (this.props.image.startsWith('icon-')) {
            // fontello icon
            content = <i className={this.props.image}/>;
        } else {
            var thumbnail = Util.get_thumbnail(this.props.image, dimension);
            content = <img src={thumbnail}/>;
        }

        return <div className={"Thumbnail " + size}>
            {content}
        </div>
    }
});

module.exports = Thumbnail;