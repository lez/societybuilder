import React, { PropTypes } from 'react'
import { Button, FormControl, FormGroup, ControlLabel } from 'react-bootstrap'
import ReactDOM from 'react-dom'
import SbTextarea from './SbTextarea.jsx'

class ForbidFlag extends React.Component {

    render() {
        return <div className="ForbidFlag">
            <form ref="forbid_form">
                <FormGroup controlId="flag_reason" ref="dat">
                    <ControlLabel>Nem való ide, mert van benne: (*)</ControlLabel>
                    <FormControl componentClass="select" ref="flag_reason">
                        <option value="null">válassz...</option>
                        <option value="cynical">cinikus felhang</option>
                        <option value="offensive">erőszak</option>
                        <option value="personal">személyeskedés</option>
                        <option value="badwords">trágárság</option>
                        <option value="generalize">általánosítás</option>
                        <option value="other">egyéb</option>
                    </FormControl>
                </FormGroup>
                <p><SbTextarea ref="note" placeholder="magyarázat"></SbTextarea></p>
                <Button active={this.props.active} bsStyle="danger" onClick={this.handleSubmit}>Tiltás</Button>
                {this.props.active &&
                    <span className="ForbidFlagCancel">
                        <Button bsSize="xsmall" bsStyle="link" onClick={this.props.onCancel}>mégse</Button>
                    </span>
                }
            </form>
        </div>
    }

    handleSubmit = (e) => {
        let flag_reason = ReactDOM.findDOMNode(this.refs.flag_reason).value
        let note = ReactDOM.findDOMNode(this.refs.note).value

        let flag = {
            flag_type: 'forbid',
            flag_reason: flag_reason,
            note: note,
        }

        // content_type (comment/post), fixed content (can be null), flag_reason (select), note (text), content_visible (bool), content_id
        this.props.onSubmit(this.props.content_type, this.props.content_id, flag)
    }
}

ForbidFlag.propTypes = {
    active: PropTypes.bool.isRequired,
    content_type: PropTypes.string.isRequired,
    content_id: PropTypes.number.isRequired,
    onCancel: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
}

export default ForbidFlag