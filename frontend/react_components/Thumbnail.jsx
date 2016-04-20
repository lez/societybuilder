import React, { PropTypes } from 'react'
import Util from '../common_js/util.js'

let dimensions = {
    micro: '15x15',
    small: '30x30',
    medium: '60x60',
    large: '100x100'
};

class Thumbnail extends React.Component {

    render() {
        let content
        let size = this.props.size ? this.props.size : 'small' // TODO use defaultProps
        let dimension = dimensions[size]

        if (this.props.image.startsWith('icon-')) {
            // fontello icon
            content = <i className={this.props.image}/>
        } else {
            let thumbnail = Util.get_thumbnail(this.props.image, dimension)
            content = <img src={thumbnail}/>
        }

        return <div className={"Thumbnail " + size}>
            {content}
        </div>
    }
}

Thumbnail.propTypes = {
    size: PropTypes.string,
    image: PropTypes.string.required
}

export default Thumbnail
