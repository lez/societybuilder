var React = require('react');
var ImgUp = require('./ImgUp.jsx');
var FileInputButton = require('./FileInputButton.jsx');

var ImageField = React.createClass({
    getInitialState: function() {
        return {
        };
    },

    render: function() {
        var x, image;

        if (this.props.image) {
            image = this.props.image;
        } else if (this.state.image) {
            image = this.state.image;
        }

        if (this.state.file) {
            x =  <ImgUp file={this.state.file} onImageDelete={null} onUploadComplete={this.onUploadComplete} />
        }
        else if (image){
            x = <img src={image.thumbnail} width="100" height="100" />;
        }
        else
        {
            x = <div><i className="demo-icon icon-user-add"></i><div className="kepalairas">Add Profile Photo</div></div>
        }
        return <div className="ImageField">
                    <FileInputButton>
                        {x}
                    </FileInputButton>
                    <input type="hidden" name="image_id" value={this.field_value()}/>
               </div>;
    },

    field_value: function () {
        if (this.state.image)
            return this.state.image.id;
        return '';
    },

    onUploadComplete: function(image, thumbnail, image_id) {
        var img = {'thumbnail':thumbnail, 'id': image_id};
        this.setState({'image': img, 'file': null});
    },

});

module.exports = ImageField;
