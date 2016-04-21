import { combineReducers } from 'redux'
import randomstring from 'random-string'

export const rootReducer = combineReducers({
    posts: posts,
    me: me
})

function posts(state = {}, action) {
    switch (action.type) {
        case 'POST':
            return {
                ...state,
                [action.post.id]: {
                    ...action.post,
                    newComment: {},
                    commenterKey: randomstring(12)
                }
            }
        case 'COMMENT_DELETE_START':
        case 'COMMENT_DELETE_END':
        case 'EDIT_POST_END':
        case 'EDIT_POST':
        case 'EDIT_COMMENT':
        case 'CANCEL_EDIT_COMMENT':
        case 'EDIT_COMMENT_END':
        case 'ADD_COMMENT_START':
        case 'ADD_COMMENT_END':
        case 'UPLOAD_START':
        case 'UPLOAD_PROGRESS':
        case 'UPLOAD_END':
        case 'DELETE_IMAGE':
            return {
                ...state,
                [action.post_id]: post(state[action.post_id], action)
            }
    default:
        return state
    }
}

function select_image(obj, selector) {
    let selected = eval(`obj.${selector}`)
    if (!selected.image) {
        selected.image = {}
    }
    return selected.image
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
            return {
                ...state,
                comments: comments(state.comments, action),
                isAddingComment: false,
                newComment: {},
                commenterKey: randomstring(12)
            }
        case 'EDIT_COMMENT_END':
            return {
                ...state,
                comments: comments(state.comments, action),
                isEditingComment: false,
                isAddingComment: false,
                commenterKey: randomstring(12)
            }
        case 'CANCEL_EDIT_COMMENT':
            return {
                ...state,
                comments: comments(state.comments, action),
                isEditingComment: false,
                commenterKey: randomstring(12)
            }
        case 'UPLOAD_START':
            {
                let newstate = {...state}
                let image = select_image(newstate, action.selector)
                image.isUploading = true
                image.percent = 0
                return newstate
            }
        case 'UPLOAD_PROGRESS':
            {
                let newstate = {...state}
                let image = select_image(newstate, action.selector)
                image.percent = action.percent
                return newstate
            }
        case 'UPLOAD_END':
            {
                let newstate = {...state}
                let image = select_image(newstate, action.selector)
                delete image.percent
                delete image.isUploading
                image.id = action.image_id
                image.thumbnail = action.thumbnail
                return newstate
            }
        case 'DELETE_IMAGE':
            {
                let newstate = {...state}
                let image = select_image(newstate, action.selector)
                delete image.percent
                delete image.isUploading
                delete image.id
                delete image.thumbnail
                return newstate
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
        case 'CANCEL_EDIT_COMMENT':
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
        case 'COMMENT_DELETE_START':
            return {
                ...state,
                isDeleting: true
            }
        case 'EDIT_COMMENT':
            if (state.image === null) {
                state.image = {}
            }
            return {
                ...state,
                isEditing: true,
                orig_image: {...state.image}
            }
        case 'EDIT_COMMENT_END':
            return action.comment_data
        case 'CANCEL_EDIT_COMMENT':
            {
                let ret = {
                    ...state,
                    isEditing: false,
                    image: state.orig_image
                }
                delete ret.orig_image
                return ret
            }
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
