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
                onDeleteImage={this.props.onDeleteImage}
                onEditComment={this.props.onEditComment}
                onFinishEditComment={this.props.onFinishEditComment}
                post={this.props.post}
                onCancelEditComment={this.props.onCancelEditComment}
                onFlagContent={this.props.onFlagContent}
            />
            {!this.props.post.isEditingComment &&
                <Commenter
                    key={this.props.post.commenterKey}
                    user={this.props.user}
                    onAddComment={this.props.onAddComment}
                    isActive={!this.props.post.isAddingComment}
                    onUpload={this.props.onUpload}
                    comment={this.props.post.newComment}
                    onDeleteImage={this.props.onDeleteImage}
               />
            }
        </div>
    }
}

export default CommentPanel