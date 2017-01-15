import React, { PropTypes } from 'react'
import { Button, Checkbox, FormGroup, ControlLabel, FormControl } from 'react-bootstrap'

import SbTextarea from './SbTextarea.jsx'
import ReactDOM from 'react-dom'

class MedicFlag extends React.Component {

    render() {
        return <div className="MedicFlag">
            <p>Javítsd meg!</p>
            <form>
                <SbTextarea ref="fixed" defaultValue={this.props.content}></SbTextarea>
                <p><span className="MedicFlagCaption">Javasolt szöveg</span></p>
                <SbTextarea ref="note" placeholder="magyarázat"></SbTextarea>
                <p><span className="MedicFlagCaption">A javítás okai</span></p>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>ez volt benne:</ControlLabel>
                    <FormControl componentClass="select" ref="flag_reason">
                        <option value="select">válassz...</option>
                        <option value="cynical">cinikus felhang</option>
                        <option value="offensive">erőszak</option>
                        <option value="personal">személyeskedés</option>
                        <option value="badwords">trágárság</option>
                        <option value="generalize">általánosítás</option>
                        <option value="other">egyéb</option>
                    </FormControl>
                </FormGroup>
                <Checkbox ref="content_visible" defaultChecked>Maradjon látható</Checkbox>
                <Button active={this.props.active} bsStyle="success" onClick={this.handleSubmit}>Javítás</Button>
                {this.props.active &&
                    <span className="MedicFlagCancel">
                        <Button bsSize="xsmall" bsStyle="link" onClick={this.props.onCancel}>mégse</Button>
                    </span>
                }
            </form>
        </div>
    }
    handleSubmit = (e) => {
        let flag_reason = ReactDOM.findDOMNode(this.refs.flag_reason).value
        let note = ReactDOM.findDOMNode(this.refs.note).value
        let fixed = ReactDOM.findDOMNode(this.refs.fixed).value
        let content_visible = jQuery(ReactDOM.findDOMNode(this.refs.content_visible)).find('input').val() == 'on' ? 1 : 0

        let flag = {
            flag_type: 'medic',
            flag_reason: flag_reason,
            note: note,
            fixed: fixed,
            content_visible: content_visible,
            original: this.props.content,
        }

        this.props.onSubmit(this.props.content_type, this.props.content_id, flag)
    }
}

MedicFlag.propTypes = {
    active: PropTypes.bool.isRequired,
    content_type: PropTypes.string.isRequired,
    content_id: PropTypes.number.isRequired,
    content: PropTypes.string.isRequired,
    onCancel: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
}

export default MedicFlag