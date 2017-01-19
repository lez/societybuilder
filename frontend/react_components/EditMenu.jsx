import React, { PropTypes } from 'react'

import { DropdownButton, MenuItem } from 'react-bootstrap'

class EditMenu extends React.Component {

    render() {
        return <div className="EditMenu">
            <DropdownButton bsSize="small" pullRight bsStyle="link" title="*" id="edit">
                <MenuItem eventKey="1" onClick={this.props.onClickEdit}><i className="icon-medkit"></i> Módosítás</MenuItem>
                <MenuItem eventKey="2" onClick={this.props.onClickDelete}><i className="icon-hand-paper-o"></i> Törlés</MenuItem>
                <MenuItem divider />
                <MenuItem eventKey="3">Segítség</MenuItem>
            </DropdownButton>
        </div>
    }
}

EditMenu.propTypes = {
    onClickEdit: PropTypes.func.isRequired,
    onClickDelete: PropTypes.func.isRequired,
}

export default EditMenu