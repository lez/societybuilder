import React from 'react'

class SbTextarea extends React.Component {
    render() {
        return <textarea ref="content" onChange={this.handleChange} {...this.props}/>
    }

    handleChange = () => {
        let content = this.refs.content
        if (content.scrollHeight > content.clientHeight) {
            let new_height = content.scrollHeight + 12
            if (new_height > 500) new_height = 500
            content.style.height = new_height + "px"
        }
    }
}

export default SbTextarea