var React = require('react');

var AddProfileImage = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <span className="fileinput-button">
                    <i className="demo-icon icon-user-add"></i>
                    <input type="file" name="selected-file" onChange={this.upload} ref="selectedfile" />
               </span>;
    },

    upload: function() {
        alert('upload');
    }
});

module.exports = AddProfileImage;