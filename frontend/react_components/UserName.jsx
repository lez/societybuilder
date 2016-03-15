var React = require('react');

var UserName = React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {
        return <span className="UserName">
            <a href={'/' + this.props.user.login}>{this.props.user.login}</a>
        </span>;
    }
});

module.exports = UserName;