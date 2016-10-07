import React, { PropTypes } from 'react'
import Time from '../common_js/Time.js'

class CreatedModified extends React.Component {

    render() {
        return <span className="CreatedModified">
            <a href={this.props.href}>
                {Time.human(this.props.created)}
                {(this.props.modified > this.props.created +1) &&
                    [' - módosítva ', Time.human(this.props.modified)]
                }
            </a>
        </span>
    }
}

CreatedModified.propTypes = {
    created: PropTypes.number.isRequired,
    modified: PropTypes.number,
    href: PropTypes.string
}

export default CreatedModified