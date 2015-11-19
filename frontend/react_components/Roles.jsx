var React = require('react');
var RoleThumbnail = require('./RoleThumbnail.jsx');
var RolesDropdown = require('./RolesDropdown.jsx');

var Roles = React.createClass({

  getInitialState: function() {
    return {};
  },

  render: function() {
    var role = this.props.role;
    if (this.props.roles.length == 1) {
      return <div className="Roles">
        <RoleThumbnail role={this.props.roles[0]}/>
      </div>;
    }

    return <div className="Roles multiple">
      <RolesDropdown roles={this.props.roles} current={this.props.current} onChangeRole={this.props.onChangeRole} />
    </div>
  }

});

module.exports = Roles;
