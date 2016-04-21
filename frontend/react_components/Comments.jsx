import React from 'react'
import Comment from './Comment.jsx'
import Commenter from './Commenter.jsx'

export default React.createClass({
    render: function () {
        return <div className="Comments">
            {this.props.comments.map(comment => {
                if (comment.isEditing){
                    return <Commenter
                        key={this.props.post.commenterKey}
                        user={this.props.user}
                        isActive={!this.props.post.isAddingComment} // TODO rename to isSubmittingComment
                        onUpload={this.props.onUpload}
                        onDeleteImage={this.props.onDeleteImage}
                        onAddComment={this.props.onAddComment}
                        comment={comment}
                        onFinishEditComment={this.props.onFinishEditComment}
                        onCancelEditComment={this.props.onCancelEditComment}
                    />
                }
                let editable = (this.props.user && comment.user.id == this.props.user.id)
                return <Comment comment={comment} key={comment.id} editable={editable} onCommentDelete={() => this.props.onCommentDelete(comment.id)} onEditComment={() => this.props.onEditComment(comment.id)}/>
            })}
        </div>
    }

});
