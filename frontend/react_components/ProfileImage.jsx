var React = require('react');
var AddProfileImage = require('./AddProfileImage.jsx');

var ProfileImage = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {

        return <div className="ProfileImage">
            {this.props.user.thumbnail ? "booz" : <AddProfileImage />}
        </div>;
    }
});

module.exports = ProfileImage;