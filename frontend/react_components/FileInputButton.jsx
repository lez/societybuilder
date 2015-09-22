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
        var file = this.refs.selectedfile.getDOMNode().files[0];
        if (file)
            this.props.upload(file);
    },
});

module.exports = FileInputButton;
