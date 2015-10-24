// all kinds of helper functions

var Util = {
    get_thumbnail: function (image, size) {
        // converts the image URL to a thumbnail URL

        var last_dot = image.lastIndexOf('.');
        return image.substring(0, last_dot) + '.' + size + image.substring(last_dot);
    }
};

module.exports = Util;
