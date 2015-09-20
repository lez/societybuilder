var React = require('react');

var FileInputButton = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <div className="fileinput-button">
                    {this.props.children}
                    <input type="file" name="selected-file" onChange={this.upload} ref="selectedfile" />
               </div>;
    },

    upload: function() {
        var input = this.refs.selectedfile.getDOMNode();
        var file = input.files[0];
        this.props.upload(file);
    },
});

module.exports = FileInputButton;
