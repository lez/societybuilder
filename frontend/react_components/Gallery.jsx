var randomString = require('random-string');
var React = require('react');
var Commenter = require('./Commenter.jsx');

var Gallery = React.createClass({
  MIN_WIDTH: 800,
  MIN_HEIGHT: 520,
  COMMENTS_WIDTH: 310,

  componentWillMount: function () {
    jQuery('body').css('overflow', 'hidden');
    jQuery(window).resize(this.resizeHandler);
    jQuery(document).keyup(this.keyupHandler);
    jQuery('#gallery_container').css('z-index', 10);
  },

  componentWillUnmount: function () {
    jQuery('body').css('overflow', '');
    jQuery(window).off('resize', this.resizeHandler);
    jQuery(document).off('keyup', this.keyupHandler);
    jQuery('#gallery_container').css('z-index', '');
  },

  getInitialState: function () {
    return {resize_counter: 0};
  },

  render: function () {
    var image = this.props.image;
    var user = this.props.current_user;

    // non-optimal code warning
    var width = Math.max(this.MIN_WIDTH, Math.min(image.width + this.COMMENTS_WIDTH, jQuery(window).width() - 40));
    var height = Math.max(this.MIN_HEIGHT, Math.min(image.height, jQuery(window).height() - 40));

    var canvaswidth = width - this.COMMENTS_WIDTH;

    var scaledwidth;
    var scaledheight;

    if (image.width > canvaswidth || image.height > height) {
      var scale_w = (canvaswidth / image.width);
      var scale_h = (height / image.height);
      var scale = Math.min(scale_w, scale_h);

      scaledwidth = Math.ceil(scale * image.width) - 1; // this -1 was added to fix broken layout of comment column. (sometimes comment column appeared below the image)
      scaledheight = Math.ceil(scale * image.height);

      // in case the pic is too tall, thighten the canvas
      canvaswidth = Math.max(Math.min(scaledwidth, canvaswidth), this.MIN_WIDTH - this.COMMENTS_WIDTH);
      width = canvaswidth + this.COMMENTS_WIDTH;

      // too wide pic? lower the height
      height = Math.max(Math.min(scaledheight, height), this.MIN_HEIGHT);
    } else {
      scaledwidth = image.width;
      scaledheight = image.height;
    }

    var imgwidth = width - this.COMMENTS_WIDTH;

    return (
      <div className="Gallery">
        <div className="overlay" onClick={this.close}>
          <div className="gallery_outer">
            <div className="gallery" style={{height: height, width: width}}>
              <div className="gallery_inner" style={{height: height, width: width}} onClick={this.doNothing}>
                <div className="image_outer" style={{width: canvaswidth}}>
                  <div className="image">
                    <img src={image.src} style={{width: scaledwidth, height: scaledheight}}/>
                  </div>
                </div>
                <div className="comment_column" style={{height: height}}>
                  <div className="close_button">
                    <a href="#" onClick={this.close} className="close_button">
                      <img src="/images/icons/close.png" />
                    </a>
                  </div>
                  <div id="user_header"/>
                  <div className="comments" id="comments" style={{maxHeight: height - 160}}/>
                  {user ? <Commenter
                    thumbnail={user.thumbnail}
                    user_id={user.user_id}
                    item_type="img"
                    item_id={image.image_id}
                    appendto="comments"
                  /> : null}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  },

  doNothing: function (e) {
    e.stopPropagation();
  },

  close: function (e) {
    React.unmountComponentAtNode(this.parentNode);
    e.preventDefault();
  },

  resizeHandler: function (e) {
    this.setState({'resize_counter': this.state.resize_counter + 1});
  },

  keyupHandler: function (e) {
    if (e.keyCode == 27) this.close(e); // ESC
  }
});

module.exports = Gallery;