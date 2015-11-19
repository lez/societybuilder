var React = require('react');
var RoleThumbnail = require('./RoleThumbnail.jsx');

var Roles = React.createClass({

  getInitialState: function() {
    return {};
  },

  render: function() {
    var role = this.props.role;
    if (this.props.roles) {

    }
    return (
      <div className="Roles">
        <RoleThumbnail role={this.props.role} />
        {this.props.roles ? 'dropdown': null}
      </div>
    );
  },

});

module.exports = Roles;
