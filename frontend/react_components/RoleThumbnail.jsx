var React = require('react');
var PageThumbnail = require('./PageThumbnail.jsx');
var UserThumbnail = require('./UserThumbnail.jsx');

var RoleThumbnail = React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {
        var size = this.props.size ? this.props.size : 'small';

        if (this.props.role.user) {
            return <UserThumbnail user={this.props.role.user} size={size}/>;
        }
        else if (this.props.role.page) {
            return <PageThumbnail page={this.props.role.page} size={size}/>;
        } else {
            throw 'invalid role type';
        }
    }
});

module.exports = RoleThumbnail;
