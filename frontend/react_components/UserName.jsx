import React from 'react';

export default React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {
        return <span className="UserName">
            <a href={'/' + this.props.user.login}>{this.props.user.login}</a>
        </span>;
    }
});
