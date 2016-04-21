import { combineReducers } from 'redux'
import randomstring from 'random-string'

export const rootReducer = combineReducers({
    posts: posts,
    me: me
})

function posts(state = {}, action) {
    switch (action.type) {
        case 'POST':
            action.post.newComment = {}
            action.post.commenterKey = randomstring(12)
            return Object.assign({}, state, {[action.post.id]: action.post})
        case 'COMMENT_DELETE_START':
        case 'COMMENT_DELETE_END':
        case 'EDIT_POST_END':
        case 'EDIT_POST':
        case 'EDIT_COMMENT':
        case 'EDIT_COMMENT_END':
        case 'ADD_COMMENT_START':
        case 'ADD_COMMENT_END':
        case 'UPLOAD_START':
        case 'UPLOAD_PROGRESS':
        case 'UPLOAD_END':
        case 'DELETE_EDIT_COMMENT_IMAGE':
        case 'DELETE_COMMENT_IMAGE':
            return Object.assign({}, state, {[action.post_id]: post(state[action.post_id], action)})
    default:
        return state
    }
}

function post(state = {}, action) {
    console.log(action.type)
    switch (action.type) {
        case 'EDIT_POST_END':
            return {
                ...state,
                content: action.content
            }
        case 'EDIT_POST':
            return {
                ...state,
                isEditing: true
            }
        case 'COMMENT_DELETE_START':
        case 'COMMENT_DELETE_END':
        case 'DELETE_EDIT_COMMENT_IMAGE':
            return {
                ...state,
                comments: comments(state.comments, action)
            }
        case 'EDIT_COMMENT':
            return {
                ...state,
                comments: comments(state.comments, action),
                isEditingComment: true
            }
        case 'ADD_COMMENT_START':
            return {
                ...state,
                isAddingComment: true
            }
        case 'ADD_COMMENT_END':
        case 'EDIT_COMMENT_END':
            return {
                ...state,
                comments: comments(state.comments, action),
                isAddingComment: false,
                newComment: {},
                commenterKey: randomstring(12)
            }
        case 'UPLOAD_START':
            return {
                ...state,
                newComment: {
                    image: {
                        isUploading: true,
                        percent: 0
                    }
                }
            }
        case 'UPLOAD_PROGRESS':
            return {
                ...state,
                newComment: {
                    image: {
                        ...state.newComment.image,
                        percent: action.percent
                    }
                }
            }
        case 'UPLOAD_END':
            return {
                ...state,
                newComment: {
                    image: {
                        id: action.image_id,
                        thumbnail: action.thumbnail
                    }
                }
            }
        case 'DELETE_COMMENT_IMAGE':
            return {
                ...state,
                newComment: {
                    ...state.newComment,
                    image: {}
                }
            }

        default:
            return state
    }
}

function comments(state = [], action) {
    switch (action.type) {
        case 'COMMENT_DELETE_END':
            return state.filter(comment => comment.id !== action.comment_id)
        case 'COMMENT_DELETE_START':
        case 'EDIT_COMMENT':
        case 'EDIT_COMMENT_END':
        case 'DELETE_EDIT_COMMENT_IMAGE':
            return state.map((comm) => {
                if (comm.id === action.comment_id)
                    return comment(comm, action)
                else
                    return comm
            })
        case 'ADD_COMMENT_END':
            return [...state, action.comment]
        default:
            return state
    }
}

function comment(state = {}, action) {
    switch (action.type) {
        case 'DELETE_EDIT_COMMENT_IMAGE':
        case 'COMMENT_DELETE_START':
            return {
                ...state,
                image: {}
            }
        case 'EDIT_COMMENT':
            return {
                ...state,
                isEditing: true
            }
        case 'EDIT_COMMENT_END':
            return action.comment_data
        default:
            return state
    }
}

function me(state = {}, action) {
    switch (action.type) {
        case 'ME':
            return {...action.user}
        default:
            return state
    }
}
