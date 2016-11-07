import { combineReducers } from 'redux'
import randomstring from 'random-string'

export const rootReducer = combineReducers({
    posts: posts,
    me: me,
    upload: upload,
})

function upload(state = {}, action) {
    switch (action.type) {
        case 'UPLOAD_ANY_START':
            {
                let newstate = {...state}
                newstate[action.selector] = {
                    isUploading: true,
                    percent: 0
                }
                return newstate
            }
        case 'UPLOAD_ANY_PROGRESS':
            {
                let newstate = {...state}
                newstate[action.selector] = {
                    ...newstate[action.selector],
                    percent: action.percent,
                }
                return newstate
            }
        case 'UPLOAD_ANY_END':
            {
                let newstate = {...state}
                newstate[action.selector] = {
                    id: action.image_id,
                    thumbnail: action.thumbnail
                }
                return newstate
            }
    default:
        return state
    }
}

function posts(state = {}, action) {
    switch (action.type) {
        case 'POST':
            return {
                ...state,
                [action.post.id]: {
                    ...action.post,
                    newComment: {
                        image: {}
                    },
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
        case 'DELETE_POST_IMAGE':
        case 'INIT_POST_IMAGE':
        case 'FLAG_CONTENT':
        case 'ADD_FLAG_START':
        case 'ADD_FLAG_END':
            return {
                ...state,
                [action.post_id]: post(state[action.post_id], action)
            }
        case 'INIT_POSTER':
            return {
                ...state,
                new: {
                    images: [],
                    id: 'new'
                }
            }
        default:
            return state
    }
}

function select_image(obj, selector) {
    return eval(`obj.${selector}`)
}

function post(state = {}, action) {
    console.log(action.type)
    switch (action.type) {
        case 'ADD_FLAG_END':
            if (action.content_type == 'post')
                return {
                    ...state,
                    isFlagging: false,
                }
            else if (action.content_type == 'comment')
                return {
                    ...state,
                    comments: comments(state.comments, action),
                }
            else
                alert('programming error: not a valid content type: ' + action.content_type)

        case 'ADD_FLAG_START':
            console.log('well here, ', action)
            if (action.content_type == 'post')
                return {
                    ...state,
                    flag: action.flag_data,
                }
            else if (action.content_type == 'comment')
                return {
                    ...state,
                    comments: comments(state.comments, action),
                }
            else
                alert('programming error: not a valid content type: ' + action.content_type)

        case 'FLAG_CONTENT':
            if (action.content_type == 'post')
                return {
                    ...state,
                    isFlagging: action.flag_type,
                }
            else if (action.content_type == 'comment')
                return {
                    ...state,
                    comments: comments(state.comments, action),
                }
            else
                alert('programming error: not a valid content type: ' + action.content_type)

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
                newComment: {
                    image: {}
                },
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
        case 'DELETE_POST_IMAGE':
            {
                return {
                    ...state,
                    images: state.images.filter(img=>img.key!==action.key)
                }
            }
        case 'INIT_POST_IMAGE':
            return {
                ...state,
                images: [
                    ...state.images,
                    {
                        isUploading: true,
                        percent: 0,
                        key: action.key // if this is not here, a key element will appear anyway... wtf. so it seems better to provide it
                    }
                ]
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
        case 'FLAG_CONTENT':
            return state.map((comm) => {
                if (comm.id === action.comment_id)
                    return comment(comm, action)
                else
                    return comm
            })
        case 'ADD_FLAG_START':
        case 'ADD_FLAG_END':
            return state.map((comm) => {
                if (comm.id === action.content_id)
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
        case 'FLAG_CONTENT':
            return {
                ...state,
                isFlagging: action.flag_type,
            }
        case 'ADD_FLAG_START':
            console.log('well, ', action)
            return {
                ...state,
                flag: action.flag_data,
            }
        case 'ADD_FLAG_END':
            return {
                ...state,
                isFlagging: false,
            }
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
