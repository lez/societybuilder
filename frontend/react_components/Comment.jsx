import _ from 'lodash'
import React from 'react'
import UserName from './UserName.jsx'
import UserThumbnail from './UserThumbnail.jsx'
import Thumbnail from './Thumbnail.jsx'
import Commenter from './Commenter.jsx'

class Comment extends React.Component {

    render() {
        return <div className="Comment clearfix">
            <div className="float_left"><UserThumbnail user={this.props.comment.user}/></div>
            <div className="comment_body float_left">
                <UserName user={this.props.comment.user}/>
                {this.props.comment.comment}
                <br/>
                {this.props.comment.image && !_.isEmpty(this.props.comment.image) &&
                    <Thumbnail image={this.props.comment.image.thumbnail} size="large"/>
                }
                {this.props.editable &&
                    <div>
                        <div className="DeleteCommentButton">
                            <a href="#" onClick={this.handleDelete}><i className="icon-cancel"></i></a>
                        </div>
                        <div className="EditCommentButton">
                            <a href="#" onClick={this.handleEdit}><i className="icon-edit"></i></a>
                        </div>
                    </div>
                }
            </div>
        </div>
    }

    handleDelete = (e) => {
        e.preventDefault()
        if (confirm('Are you sure you want to delete this comment?')) {
            this.props.onCommentDelete()
        }
    }

    handleEdit = (e) => {
        e.preventDefault()
        this.props.onEditComment()
    }
}

export default Comment