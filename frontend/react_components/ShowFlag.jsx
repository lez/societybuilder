import React, { PropTypes } from 'react'
import { Button, FormControl, FormGroup, ControlLabel } from 'react-bootstrap'
import ReactDOM from 'react-dom'
import SbTextarea from './SbTextarea.jsx'

class ShowFlag extends React.Component {

    render() {
        return <div className="ShowFlag">

            <span>
                Miért javasolták: {this.props.flag.note}<br/>
                Egyelőre kénytelen leszel elfogadni az újat.<br/>
            </span>

            {this.props.is_author &&
                <Button active={true} bsStyle="success" onClick={this.handleAccept}>Elfogadás</Button>
            }

            <span className="ShowFlagClose">
                <Button bsSize="xsmall" bsStyle="link" onClick={this.props.onClose}>bezár</Button>
            </span>
        </div>
    }

    handleAccept = (e) => {
        this.props.onAccept(this.props.flag.id)
    }
}

ShowFlag.propTypes = {
    flag: PropTypes.object.isRequired,
    is_author: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onAccept: PropTypes.func.isRequired,
    // onAgree: PropTypes.func.isRequired,
    // onDisagree: PropTypes.func.isRequired,
}

export default ShowFlag