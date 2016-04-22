import React, { PropTypes } from 'react'
import Upload from '../components/upload.js'
import UploadedImg from './UploadedImg.jsx'
import Strings from '../common_js/Strings.js'

// show an image being uploaded or already uploaded
class ImgUp extends React.Component {

    render() {
        let image = this.props.image
        let thumb

        if (image.thumbnail)
            thumb = <UploadedImg thumbnail={image.thumbnail}/>
        else if (image.isUploading)
            thumb = <canvas width="60" height="60" ref="canvas"/>
        else
            console.log('programing error')

        return <div className="ImgUp">
            {image.isUploading && Math.round(image.percent)}
            
            <a href="#" onClick={this.handleImageDelete} className="delete_button"><i className="icon-cancel"></i></a>
            <span id="preview" ref="preview" className="thumb">
                {thumb}
            </span>
        </div>
    }

    handleImageDelete = (e) => {
        e.preventDefault()
        // if (this.upload) {
        //     this.upload.abort() // TODO: this.upload is not here anymore, but we should call abort on it.
        // }
        this.props.onImageDelete(this.props.image)
    }
}

ImgUp.propTypes = {
    image: PropTypes.object,
    onImageDelete: PropTypes.func

}
export default ImgUp