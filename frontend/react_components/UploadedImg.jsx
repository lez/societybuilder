import React from 'react';

export default React.createClass({

    render: function () {
        return <span className="UploadedImg">
            <img width="100" height="100" ref="img" src={this.props.thumbnail}/>
        </span>;
    }
});
