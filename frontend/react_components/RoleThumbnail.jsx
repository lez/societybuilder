import React from 'react';
import PageThumbnail from './PageThumbnail.jsx';
import UserThumbnail from './UserThumbnail.jsx';

export default React.createClass({
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

