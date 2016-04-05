import React from 'react';
import ImageField from './ImageField.jsx';

// old way:
// props: user


// new way:
//props: image, url

var EditProfileImage = React.createClass({
    getInitialState: function() {
        return {};
    },

    render: function() {
        return <div className="EditProfileImage">
            <ImageField image={this.props.image} onChange={this.onChange} ref="imagefield" name="image_id"/>
            {this.state.changed ? <button onClick={this.submit}>Csere</button> : null}
        </div>;
    },

    submit: function(event) {
        event.preventDefault();
        var imagefield = this.refs.imagefield;
        // never be afraid of a tiny boilerplate
        var val = jQuery(imagefield).find('input[name="image_id"]').val();
        IS.submitRest(this.props.url, {image_id: val}, function(){document.reload();});
    },

    onChange: function() {
        this.setState({'changed': true});
    }
});

module.exports = EditProfileImage;
