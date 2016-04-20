import React from 'react'

class FileUploadButton extends React.Component {
    render() {
        return <div className="FileUploadButton">
            {this.props.children}
            <input
                className="exclude-from-rest"
                multiple={this.props.multiple}
                name="selected-file"
                onChange={this.upload}
                onBlur={this.upload}
                ref="selectedfile"
                type="file"
            />
        </div>
    }

    reset(e) {
        var elem = jQuery(e)
        elem.wrap('<form>').closest('form').get(0).reset() // FIXME there's no <form>
        elem.unwrap()
    }

    upload = () => {
        let f
        let node = this.refs.selectedfile
        if (this.props.multiple){
            f = node.files
        } else {
            f = node.files[0]
        }
        this.props.upload(f) // this has to be called even if f is null to focus the input field
        this.reset(node)
    }
}

export default FileUploadButton
