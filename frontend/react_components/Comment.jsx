import _ from 'lodash'
import React, { PropTypes } from 'react'
import RoleLink from './RoleLink.jsx'
import FlagMenu from './FlagMenu.jsx'
import EditMenu from './EditMenu.jsx'
import UserThumbnail from './UserThumbnail.jsx'
import Thumbnail from './Thumbnail.jsx'
import Commenter from './Commenter.jsx'
import MedicFlag from './MedicFlag.jsx'
import ForbidFlag from './ForbidFlag.jsx'
import CreatedModified from './CreatedModified.jsx'

class Comment extends React.Component {

    render() {
        let flag_button_active = this.props.comment.isFlagging && ! this.props.comment.flag  // TODO multiple flags

        return <div className="Comment clearfix">
            {this.props.comment.isFlagging == 'medic' &&
                <MedicFlag
                    active={flag_button_active}
                    content_type="comment"
                    content_id={this.props.comment.id}
                    content={this.props.comment.comment}
                    onCancel={this.handleCancelFlagging}
                    onSubmit={this.props.onSubmitFlag}
                />
            }
            {this.props.comment.isFlagging == 'forbid' &&
                <ForbidFlag
                    active={flag_button_active}
                    content_type="comment"
                    content_id={this.props.comment.id}
                    onCancel={this.handleCancelFlagging}
                    onSubmit={this.props.onSubmitFlag}
                />
            }
            <div className="float_left"><UserThumbnail user={this.props.comment.user}/></div>
            <div className="comment_body">
                <RoleLink user={this.props.comment.user}/>
                {this.props.comment.comment}

                {this.props.comment.image && !_.isEmpty(this.props.comment.image) && <br/>}
                {this.props.comment.image && !_.isEmpty(this.props.comment.image) && <Thumbnail image={this.props.comment.image.thumbnail} size="large"/>}

                <br/>
                <CreatedModified created={this.props.comment.created} modified={this.props.comment.modified}/>
            </div>

            {this.props.editable &&
                <EditMenu
                    onClickEdit={this.handleEdit}
                    onClickDelete={this.handleDelete}
                />
            }

            {this.props.flaggable &&
                <FlagMenu
                    onClickMedic={this.handleMedic}
                    onClickForbid={this.handleForbid}
                />
            }

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

    handleMedic = (e) => {
        e.preventDefault()
        this.props.onFlagContent('comment', 'medic', this.props.comment.id)
    }

    handleForbid = (e) => {
        e.preventDefault()
        this.props.onFlagContent('comment', 'forbid', this.props.comment.id)
    }

    handleCancelFlagging = (e) => {
        e.preventDefault()
        this.props.onFlagContent('comment', null, this.props.comment.id)
    }
}

Comment.propTypes = {
    editable: PropTypes.bool.isRequired,
    flaggable: PropTypes.bool.isRequired,
    comment: PropTypes.object.isRequired,
    onCommentDelete: PropTypes.func.isRequired,
    onEditComment: PropTypes.func.isRequired,
    onFlagContent: PropTypes.func.isRequired,
    onSubmitFlag: PropTypes.func.isRequired,
}

export default Comment