var React = require('react');

var Test = React.createClass({
    getInitialState: function() {
        return {
            count: this.props.initialCount
        };
    },

    _increment: function() {
        this.setState({ count: this.state.count + 1 });
    },

    render: function() {
        return <div onClick={this._increment}>
            {this.state.count}
        </div>;
    }
});

module.exports = Test;