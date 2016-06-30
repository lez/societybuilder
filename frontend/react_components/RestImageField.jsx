import React from 'react'
import ImageField from './ImageField.jsx'

class RestImageField extends React.Component {

    state = {}

    // props: url, field, initial value (image), reload (bool)
    render() {
        console.log(this.props)
        return <div className="RestImageField" ref="main">
            <ImageField image={this.props.image} onChange={this.onChange} name="image_id"/>
            {this.state.changed ? <button onClick={this.submit}>Csere</button> : null}
        </div>
    }

    reload_after_edit() {
        return (this.props.reload === true)
    }

    submit(event) {
        event.preventDefault()
        var restimagefield = this.refs.main

        // never be afraid of a tiny boilerplate
        var val = jQuery(restimagefield).find('input[name="image_id"]').val()
        var data = {}
        data[this.props.field] = val
        IS.submitRest(this.props.url, data, this.reload_after_edit() ? null : this.done)
    }

    onChange = () => {
        this.setState({changed: true})
    }

    done = () => {
        this.setState({changed: false})
    }

}

// const mapStateToProps = (state, ownProps) => {
//     console.log(state.me)
//     return {
//         image: state.me.image
//     }
// }

// const mapDispatchToProps = (dispatch, ownProps) => {
//     return {}
// }

// RestImageField = connect(
//     mapStateToProps,
//     mapDispatchToProps
// )(RestImageField)

export default RestImageField



