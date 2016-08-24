import randomstring from 'random-string'
import Uploader from '../components/uploader'

export function commentDeleteStart(post_id, comment_id) {
    return {
        type: 'COMMENT_DELETE_START',
        comment_id: comment_id,
        post_id: post_id
    }
}

export function commentDeleteEnd(post_id, comment_id) {
    return {
        type: 'COMMENT_DELETE_END',
        comment_id: comment_id,
        post_id: post_id
    }
}

export function commentDelete(post_id, comment_id) {

    return (dispatch) => {
        dispatch(commentDeleteStart(post_id, comment_id))

        return jQuery.ajax({
            url: `/api/comment/${comment_id}`,
            type: 'DELETE'
        })
        .then((result) => {
            dispatch(commentDeleteEnd(post_id, comment_id))
        })
    }
}

export function addCommentStart(post_id) {
    return {
        type: 'ADD_COMMENT_START',
        post_id: post_id
    }
}

export function addCommentEnd(comment, post_id) {
    return {
        type: 'ADD_COMMENT_END',
        comment: comment,
        post_id: post_id
    }
}

export function addComment(comment_data, post_id) {

    return (dispatch) => {
        dispatch(addCommentStart(post_id))

        let data = {
            ...comment_data,
            item_type: 'post',
            item_id: post_id
        }

        return jQuery.ajax({
            url: '/api/comment',
            type: 'POST',
            data: data
        })
        .then((result) => {
            dispatch(addCommentEnd(result, post_id))
        })
        // TODO error handling
    }
}

export function finishEditComment(post_id, comment_id, comment_data) {

    return (dispatch) => {
        dispatch(addCommentStart(post_id))

        return jQuery.ajax({
            url: `/api/comment/${comment_id}`,
            type: 'PUT',
            data: comment_data
        })
        .then((result) => {
            dispatch(editCommentEnd(result, post_id, comment_id))
        })
        // TODO error handling
    }
}

export function editCommentEnd(result, post_id, comment_id){
    return {
        type: 'EDIT_COMMENT_END',
        comment_id: comment_id,
        post_id: post_id,
        comment_data: result
    }
}

export function editPost(post_id) {
    return {
        type: 'EDIT_POST',
        post_id: post_id
    }
}

export function editComment(post_id, comment_id) {
    return {
        type: 'EDIT_COMMENT',
        post_id: post_id,
        comment_id: comment_id
    }
}

export function uploadStart(post_id, selector, file_input) {
    return {
        type: 'UPLOAD_START',
        file_input: file_input,
        post_id: post_id,
        selector: selector
    }
}

export function uploadProgress(post_id, selector, percent) {
    return {
        type: 'UPLOAD_PROGRESS',
        percent: percent,
        post_id: post_id,
        selector: selector
    }
}

export function uploadEnd(post_id, selector, image_id, thumbnail) {
    return {
        type: 'UPLOAD_END',
        image_id: image_id,
        thumbnail: thumbnail,
        post_id: post_id,
        selector: selector
    }
}

export function uploadAnyStart(selector, file_input) {
    return {
        type: 'UPLOAD_ANY_START',
        file_input: file_input,
        selector: selector
    }
}

export function uploadAnyProgress(selector, percent) {
    return {
        type: 'UPLOAD_ANY_PROGRESS',
        percent: percent,
        selector: selector
    }
}

export function uploadAnyEnd(selector, image_id, thumbnail) {
    return {
        type: 'UPLOAD_ANY_END',
        image_id: image_id,
        thumbnail: thumbnail,
        selector: selector
    }
}

export function upload(post_id, selector, file_input) {
    return dispatch => {
        dispatch(uploadStart(post_id, selector, file_input))

        let onUploadProgress = (percent) => dispatch(uploadProgress(post_id, selector, percent))
        let onUploadEnd = (image_id, thumbnail) => dispatch(uploadEnd(post_id, selector, image_id, thumbnail))
        let uploader = new Uploader(file_input, onUploadProgress, onUploadEnd)
        // todo: upload should be cancellable
    }
}

export function uploadAny(selector, file_input) {
    return dispatch => {
        dispatch(uploadAnyStart(selector, file_input))

        let onUploadProgress = (percent) => dispatch(uploadAnyProgress(selector, percent))
        let onUploadEnd = (image_id, thumbnail) => dispatch(uploadAnyEnd(selector, image_id, thumbnail))
        let uploader = new Uploader(file_input, onUploadProgress, onUploadEnd)
        // todo: upload should be cancellable
    }
}

export function initPostImage(post_id, key) {
    return {
        type: 'INIT_POST_IMAGE',
        post_id: post_id,
        key: key
    }
}

export function addPostImage(post_id, file) {
    return dispatch => {
        let key = randomstring(12)
        dispatch(initPostImage(post_id, key))
        let selector = `images.find(function(img){return img.key==='${key}'})`
        let onUploadProgress = (percent) => dispatch(uploadProgress(post_id, selector, percent))
        let onUploadEnd = (image_id, thumbnail) => dispatch(uploadEnd(post_id, selector, image_id, thumbnail))
        let uploader = new Uploader(file, onUploadProgress, onUploadEnd)
        // todo: upload should be cancellable
    }
}

export function deleteImage(post_id, selector){
    return {
        type: 'DELETE_IMAGE',
        post_id: post_id,
        selector: selector
    }
}

export function deletePostImage(post_id, key){
    return {
        type: 'DELETE_POST_IMAGE',
        post_id: post_id,
        key: key
    }
}

export function cancelEditComment(post_id, comment_id){
    return {
        type: 'CANCEL_EDIT_COMMENT',
        post_id: post_id,
        comment_id: comment_id
    }
}
