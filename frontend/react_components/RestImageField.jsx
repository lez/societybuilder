var React = require('react');
var ImageField = require('./ImageField.jsx');

var RestImageField = React.createClass({
    getInitialState: function() {
        return {};
    },

    // props: url, field, initial value (image), reload (bool)
    render: function() {
        return <div className="RestImageField" ref="main">
            <ImageField image={this.props.image} onChange={this.onChange}/>
            {this.state.changed ? <button onClick={this.submit}>Csere</button> : null}
        </div>;
    },

    reload_after_edit: function() {
        return (this.props.reload === true);
    },

    submit: function(event) {
        event.preventDefault();
        var restimagefield = this.refs.main;

        // never be afraid of a tiny boilerplate
        var val = jQuery(restimagefield).find('input[name="image_id"]').val();
        var data = {};
        data[this.props.field] = val;
        IS.submitRest(this.props.url, data, this.reload_after_edit() ? null : this.done);
    },

    onChange: function() {
        this.setState({changed: true});
    },

    done: function () {
        this.setState({changed: false});
    }

});

module.exports = RestImageField;
