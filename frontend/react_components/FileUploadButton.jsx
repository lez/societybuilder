var React = require('react');

var FileUploadButton = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <div className="FileUploadButton">
                    {this.props.children}
                    <input type="file" name="selected-file" onChange={this.upload} onBlur={this.upload} ref="selectedfile" multiple={this.props.multiple} />
               </div>;
    },

    reset: function(e) {
        var elem = jQuery(e);
        elem.wrap('<form>').closest('form').get(0).reset();
        elem.unwrap();
    },

    upload: function() {
        var f;
        var node = this.refs.selectedfile.getDOMNode();
        if (!this.props.multiple){
            f = node.files[0];
        } else {
            f = node.files;
        }
        this.props.upload(f);
        this.reset(node);
    },
});

module.exports = FileUploadButton;
