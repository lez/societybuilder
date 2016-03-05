var React = require('react');
var ImageField = require('./ImageField.jsx');

var RestImageField = React.createClass({
    getInitialState: function() {
        return {};
    },

    // props: url, field, initial value (image)
    render: function() {
        return <div className="RestImageField">
            <ImageField image={this.props.image} onChange={this.onChange} ref="imagefield"/>
            {this.state.changed ? <button onClick={this.submit}>Csere</button> : null}
        </div>;
    },

    submit: function(event) {
        event.preventDefault();
        var imagefield = this.refs.imagefield.getDOMNode();
        // never be afraid of a tiny boilerplate
        var val = jQuery(imagefield).find('input[name="image_id"]').val();
        var data = {};
        data[this.props.field] = val;
        IS.submitRest(this.props.url, data, this.done);
    },

    onChange: function() {
        this.setState({changed: true});
    },

    done: function () {
        this.setState({changed: false});
    }

});

module.exports = RestImageField;
