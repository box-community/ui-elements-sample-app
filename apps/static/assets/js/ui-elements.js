function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

function renderPreview_single(accessToken, container, file_id) {
    var options = {
        'container': container,

        'collection': [file_id],
    }

    // console.log('options:', options);

    var contentPreviewer = new Box.ContentPreview();
    console.log('Content Previewer:', contentPreviewer);

    contentPreviewer.show(file_id, accessToken, options);
}

function renderUploader_single(accessToken, container, folder_id, documentType, booking_diver_id) {
    var options = {
        "container": container,
        "fileLimit": 1,
    }

    // console.log('options:', options);

    var contentUploader = new Box.ContentUploader();
    console.log('Content Uploader:', contentUploader);

    contentUploader.addListener('close', uploaderClose);
    contentUploader.addListener('complete', uploaderComplete);
    contentUploader.addListener('upload', uploaderUpload);
    contentUploader.addListener('error', uploaderError);

    function uploaderClose(e) {
        console.log('close:', e);
        // sendEventToServer('close', e);
    }

    function uploaderComplete(e) {
        console.log('complete:', e);
        sendEventToServer('complete', e);
    }

    function uploaderUpload(e) {
        console.log('upload:', e);
        // sendEventToServer('upload', e);
    }

    function uploaderError(e) {
        console.log('error:', e);
        // sendEventToServer('error', e);
    }

    function sendEventToServer(eventType, e) {

        var localData = {
            eventType: eventType,
            documentType: documentType,
            booking_diver_id: booking_diver_id,
            e: e
        };

        // TODO Add ajax refresh to the page element

        $.ajax({
            url: "{{ url_for('booking_blueprint.event') }}",
            type: 'POST',
            data: JSON.stringify(localData),
            contentType: 'application/json;charset=UTF-8',
        });
    };

    contentUploader.show(folder_id, accessToken, options);

}