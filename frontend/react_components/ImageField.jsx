import React from 'react';
import FileUploadButton from './FileUploadButton.jsx';
import { connect } from 'react-redux'
import { uploadAny } from '../actions'
class ImageField extends React.Component {
    render() {
        let x
        if (!this.props.image) {
            x = <div><i className="demo-icon icon-user-add"></i><div className="kepalairas">Kép feltöltése</div></div>
        }
        else if (this.props.image.isUploading) {
            x =  <span>upload percent {this.props.image.percent}</span>
        }
        else {
            x = <img src={this.props.image.thumbnail} width="100" height="100" />
        }

        return <div className="ImageField">
            <FileUploadButton upload={this.upload}>
                {x}
            </FileUploadButton>
            <input type="hidden" name={this.props.name} value={this.field_value()}/>
        </div>
    }

    field_value = () => {
        if (this.props.image)
            return this.props.image.id;
        return ''
    }

    upload = (file) => {
        if (file) {
            this.props.onUploadAny(this.props.name, file)
            this.props.onChange()  // FIXME: too early, but it will do for now
        }
    }
}

const mapStateToProps = (state, ownProps) => {
    let name = ownProps.name
    let ret
    if (state.upload && state.upload[name]){
        ret = state.upload[name]
    } else {
        if (ownProps.image)
            ret = ownProps.image
        else
            ret = null
    }
    return {
        image: ret
    }
}

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        onUploadAny: (selector, file_input) => {
            dispatch(uploadAny(selector, file_input))
        },
    }
}

ImageField = connect(
    mapStateToProps,
    mapDispatchToProps
)(ImageField)

export default ImageField