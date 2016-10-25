import React, { PropTypes } from 'react'
import { Button, FormControl, FormGroup, ControlLabel } from 'react-bootstrap'

import SbTextarea from './SbTextarea.jsx'

class ForbidFlag extends React.Component {

    render() {
        return <div className="ForbidFlag">
            <form>
                <FormGroup controlId="formControlsSelect">
                    <ControlLabel>Nem való ide, mert van benne: (*)</ControlLabel>
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
                <Button bsStyle="danger">Küldés</Button>
                <span className="ForbidFlagCancel">
                    <Button bsSize="xsmall" bsStyle="link" onClick={this.props.onCancel}>mégse</Button>
                </span>
            </form>
        </div>
    }
}

ForbidFlag.propTypes = {
    onCancel: PropTypes.func.isRequired,
}

export default ForbidFlag