import React from 'react'
import Comments from './Comments.jsx'
import Commenter from './Commenter.jsx'

class CommentPanel extends React.Component {
    render() {
        return <div className="CommentPanel">
            <Comments
                comments={this.props.comments}
                user={this.props.user}
                onCommentDelete={this.props.onCommentDelete}
                onAddComment={this.props.onAddComment}
                isActive={!this.props.post.isAddingComment}
                onUpload={this.props.onUpload}
                onDeleteCommentImage={this.props.onDeleteCommentImage}
                onEditComment={this.props.onEditComment}
                onFinishEditComment={this.props.onFinishEditComment}
                post={this.props.post}
                onDeleteEditCommentImage={this.props.onDeleteEditCommentImage}
            />
            {!this.props.post.isEditingComment &&
                <Commenter
                    key={this.props.post.commenterKey}
                    user={this.props.user}
                    onAddComment={this.props.onAddComment}
                    isActive={!this.props.post.isAddingComment}
                    onUpload={this.props.onUpload}
                    comment={this.props.post.newComment}
                    onDeleteCommentImage={this.props.onDeleteCommentImage}
               />
            }
        </div>
    }
}

export default CommentPanel