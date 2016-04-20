import React, { PropTypes } from 'react'

// this class is probably not needed at all
class UploadedImg extends React.Component {

    render() {
        return <span className="UploadedImg">
            <img width="100" height="100" ref="img" src={this.props.thumbnail}/>
        </span>
    }
}

UploadedImg.propTypes = {
    thumbnail: PropTypes.string
}

export default UploadedImg
