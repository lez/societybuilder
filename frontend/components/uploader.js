import Upload from './upload'

class Uploader {
    constructor (file, uploadProgress, uploadEnd) {
        this.uploadProgress = uploadProgress
        this.uploadEnd = uploadEnd
        this.upload = new Upload(file)
        this.upload.to('/upload')
        this.upload.on('progress', this.progress)
        this.upload.on('error', this.error)
        this.upload.on('end', this.finished)
    }

    progress = (progress) => {
        this.uploadProgress(progress.percent)
    }

    error (a, b) {
        alert('error') // TODO
    }

    finished = (a, b) => {
        let resp = JSON.parse(a.responseText)
        if (!resp.success) {
            alert('server error') // TODO
            return
        }
        this.uploadEnd(resp.image_id, resp.thumbnail)
    }
}

export default Uploader