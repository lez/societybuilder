var React = require('react');
var RoleThumbnail = require('./RoleThumbnail.jsx');
var Thumbnail = require('./Thumbnail.jsx');

var RoleMenuItem = React.createClass({
    render: function () {
        return <a href="#" onClick={this.handleClick}>
            <div className="RoleMenuItem" key={this.props.key}>
                <RoleThumbnail role={this.props.role}/>
                {this.props.role.name}
                {this.props.selected ? <Thumbnail image="icon-ok" size="micro"/> : null}
            </div>
        </a>
    },
    handleClick: function (e) {
        //console.log('hello click');
        e.preventDefault();
        this.props.onChangeRole(this.props.role.id);
    }
});

var RoleMenu = React.createClass({
    render: function () {
        var menuitems = [];
        for (var i = 0; i < this.props.roles.length; i++) {
            var selected = false;
            var role = this.props.roles[i];
            if (role.id == this.props.current) {
                selected = true;
            }
            menuitems.push(<RoleMenuItem role={this.props.roles[i]} key={i} selected={selected} onChangeRole={this.props.onChangeRole}/>);
        }

        return <div className="RoleMenu">
            {menuitems}
        </div>
    }
});

var RolesDropdown = React.createClass({

    getInitialState: function () {
        return {
            open: false
        };
    },

    render: function () {
        var roles = this.props.roles;
        var role = null;

        for (var i = 0; i < this.props.roles.length; i++) {
            if (this.props.roles[i].id == this.props.current)
                role = this.props.roles[i];
        }

        return <div className="RolesDropdown">
            <a href="#" onClick={this.handleClick}>
                <RoleThumbnail role={role}/>
                <Thumbnail image="icon-down" size="micro"/>
            </a>
            {this.state.open ? <RoleMenu roles={this.props.roles} current={this.props.current} onChangeRole={this.handleChangeRole}/> : null}
        </div>;
    },

    handleClick: function (e) {
        e.preventDefault();
        this.setState({open: !this.state.open})
    },

    // close the dropdown menu
    handleChangeRole(role) {
        this.setState({open: false});
        this.props.onChangeRole(role);
    }

});

module.exports = RolesDropdown;
