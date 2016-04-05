import React from 'react';
import UserName from './UserName.jsx';
import UserThumbnail from './UserThumbnail.jsx';
import Thumbnail from './Thumbnail.jsx';
import Commenter from './Commenter.jsx';

export default React.createClass({
    getInitialState: function () {
        return {}
    },

    render: function () {

        return <div className="Comment clearfix">
            <div className="float_left"><UserThumbnail user={this.props.comment.user}/></div>
            <div className="comment_body float_left">
                <UserName user={this.props.comment.user}/>
                {this.props.comment.comment}
                <br/>
                {this.props.comment.image ? <Thumbnail image={this.props.comment.image.thumbnail} size="large"/> : null}
                {this.props.editable ? <div>
                    <div className="DeleteCommentButton">
                        <a href="#" onClick={this.handleDelete}><i className="icon-cancel"></i></a>
                    </div>
                    <div className="EditCommentButton">
                        <a href="#" onClick={this.handleEdit}><i className="icon-edit"></i></a>
                    </div>
                </div>
                    : null
                }

            </div>
        </div>;
    },

    handleDelete: function (e) {
        e.preventDefault();
        if (confirm('Are you sure you want to delete this comment?')){
            jQuery.ajax({
                url: '/api/comment/' + this.props.comment.id,
                type: 'DELETE',
                success: function(result){
                    document.location.reload();
                },
                error: function(result){
                    alert(Strings.general_error);
                }
            });
        }
    },

    handleEdit: function () {
        alert('edit comment: yess');
    }
});
