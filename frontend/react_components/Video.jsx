var React = require('react');

var Images = React.createClass({

  render: function() {
    var remove_video = this.props.onRemoveVideo;
    var video = this.props.video;

    return (
      <div id="video_wrapper">
        <table>
          <tr>
            <td>
              <div className="video_img">
                <img id="thumbnail" src={video.thumbnail} />
                <a href="#" onClick={remove_video} className="delete_button"><img src="/images/icons/discrete_delete.png" /></a>
              </div>
            </td>
            <td>
              <span className="video_name">{video.name}</span>
            </td>
          </tr>
        </table>
      </div>
    );
  }

});


module.exports = Images;