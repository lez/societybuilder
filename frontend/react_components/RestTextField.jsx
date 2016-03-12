var React = require('react');
var ImageField = require('./ImageField.jsx');

var RestTextField = React.createClass({
    getInitialState: function() {
        return {};
    },

    // props: url, field, initial value (text)
    render: function() {
        return <div className="RestTextField">
            <span className="label">{this.props.label}</span>
            {this.state.changed ? <textarea id="text_id" key="yep" ref="field" onChange={this.onChange}/> : <textarea id="text_id" key="yep" value={this.props.text} ref="field" onChange={this.onChange}/>}
            {this.state.changed ? <button onClick={this.submit}>Mentés</button> : null}
        </div>;
    },

    getValue: function() {
        var field = this.refs.field.getDOMNode();
        return jQuery(field).val();
    },

    submit: function(event) {
        event.preventDefault();
        var data = {};
        data[this.props.field] = this.getValue();
        IS.submitRest(this.props.url, data, null);
    },

    onChange: function() {
        this.setState({changed: true});
    },

    done: function () {
        // TODO: bekotni ezt a fuggvenyt
        this.setState({changed: false, value: this.getValue()});
    }

});

module.exports = RestTextField;
