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
        elem.wrap('<form>').closest('form').get(0).reset(); // FIXME there's no more form
        elem.unwrap();
    },

    upload: function() {
        var f;
        var node = this.refs.selectedfile;
        if (this.props.multiple){
            f = node.files;
        } else {
            f = node.files[0];
        }
        this.props.upload(f);
        this.reset(node);
    }
});

module.exports = FileUploadButton;
