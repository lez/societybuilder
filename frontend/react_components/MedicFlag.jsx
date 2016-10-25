import React, { PropTypes } from 'react'
import { Button, Checkbox, FormGroup, ControlLabel, FormControl } from 'react-bootstrap'

import SbTextarea from './SbTextarea.jsx'

class MedicFlag extends React.Component {

    render() {
        return <div className="MedicFlag">
            <p>Javítsd meg!</p>
            <form>
                <SbTextarea name="content" defaultValue={this.props.content}></SbTextarea>
                <p><span className="MedicFlagCaption">Javasolt szöveg</span></p>
                <SbTextarea name="note" placeholder="magyarázat"></SbTextarea>
                <p><span className="MedicFlagCaption">A javítás okai</span></p>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>ez van benne:</ControlLabel>
                    <FormControl componentClass="select" placeholder="plholdersz">
                        <option value="select">válassz...</option>
                        <option value="cynical">cinikus felhang</option>
                        <option value="offensive">erőszak</option>
                        <option value="personal">személyeskedés</option>
                        <option value="badwords">trágárság</option>
                        <option value="generalize">általánosítás</option>
                        <option value="other">egyéb</option>
                    </FormControl>
                </FormGroup>
                <Checkbox defaultChecked>Maradjon látható</Checkbox>
                <Button bsStyle="success">Javítás</Button>
                <span className="MedicFlagCancel">
                    <Button bsSize="xsmall" bsStyle="link" onClick={this.props.onCancel}>mégse</Button>
                </span>
            </form>
        </div>
    }
}

MedicFlag.propTypes = {
    content: PropTypes.string.isRequired,
    onCancel: PropTypes.func.isRequired,
}

export default MedicFlag