import React, { PropTypes } from 'react'

import { DropdownButton, MenuItem } from 'react-bootstrap'

class FlagMenu extends React.Component {

    render() {
        return <div className="FlagMenu">
            <DropdownButton bsSize="small" pullRight bsStyle="link" title="" id="flag">
                <MenuItem eventKey="1" onClick={this.props.onClickMedic}><i className="icon-medkit"></i> Javítás</MenuItem>
                <MenuItem eventKey="2" onClick={this.props.onClickForbid}><i className="icon-hand-paper-o"></i> Tiltás</MenuItem>
                <MenuItem divider />
                <MenuItem eventKey="3">Segítség</MenuItem>
            </DropdownButton>
        </div>
    }
}

FlagMenu.propTypes = {
    onClickMedic: PropTypes.func.isRequired,
    onClickForbid: PropTypes.func.isRequired,
}

export default FlagMenu