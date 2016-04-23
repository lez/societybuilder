import React from 'react';

export default React.createClass({
    render: function () {
        let link
        let name

        if (this.props.user) {
            link = this.props.user.login
            name = this.props.user.login
        }
        else if (this.props.role) {
            if (this.props.role.page) {
                link = this.props.role.page.permalink
                name = this.props.role.page.name
            } else if (this.props.role.user) {
                link = this.props.role.user.login
                name = this.props.role.user.login
            } else {
                alert('programming error')
            }
        } else {
            alert('programming error')
        }

        return <span className="RoleLink">
            <a href={`/${link}`}>{name}</a>
        </span>;
    }
});
