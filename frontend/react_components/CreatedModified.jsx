import React, { PropTypes } from 'react'
import Time from '../common_js/Time.js'

class CreatedModified extends React.Component {

    render() {
        return <span>
            {Time.human(this.props.created)}
            {this.props.modified &&
                [' - módositva ', Time.human(this.props.modified)]
            }
        </span>
    }
}

Comment.propTypes = {
    created: PropTypes.number.isRequired,
    modified: PropTypes.number
}

export default CreatedModified