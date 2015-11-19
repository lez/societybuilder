var React = require('react');
var ImageField = require('./ImageField.jsx');


var AddProfileImage = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <div className="AddProfileImage">
            <form data-url="/api/user" method="post" onSubmit={this.submit} ref="form">
                <ImageField image={this.props.user.image} onChange={this.onChange}/>
                {this.state.changed ? <input type="submit" value="Csere" /> : null}
            </form>
        </div>;
    },

    submit: function(event) {
        var form = this.refs.form.getDOMNode();
        IS.submit(event, form);
    },

    onChange: function() {
        this.setState({'changed': true});
    }
});

module.exports = AddProfileImage;
