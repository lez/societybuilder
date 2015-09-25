var React = require('react');

var FileUploadButton = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <div className="fileinput-button">
                    {this.props.children}
                    <input type="file" name="selected-file" onChange={this.upload} onBlur={this.upload} ref="selectedfile" />
               </div>;
    },

    upload: function() {
        var file = this.refs.selectedfile.getDOMNode().files[0];
        this.props.upload(file);
    },
});

module.exports = FileUploadButton;
