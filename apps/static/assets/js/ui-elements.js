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

function renderUploader_single(accessToken, container, folder_id, documentType, booking_diver_id, callback, url_event, url_refresh, element) {
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
        callback('close', e, documentType, booking_diver_id, url_event, element, url_refresh);
    }

    function uploaderComplete(e) {
        console.log('complete:', e);
        callback('complete', e, documentType, booking_diver_id, url_event, element, url_refresh);
    }

    function uploaderUpload(e) {
        console.log('upload:', e);
        callback('upload', e, documentType, booking_diver_id, url_event, element, url_refresh);
    }

    function uploaderError(e) {
        console.log('error:', e);
        callback('error', e, documentType, booking_diver_id, url_event, element, url_refresh);
    }

    

    contentUploader.show(folder_id, accessToken, options);

}

function uploaderSendEventToServer(eventType, e, documentType, booking_diver_id, url_event, element, url_refresh) {

    var localData = {
        eventType: eventType,
        documentType: documentType,
        booking_diver_id: booking_diver_id,
        e: e
    };

    // TODO Add ajax refresh to the page element
    if (eventType == 'complete')
        $.ajax({
            url: url_event,
            type: 'POST',
            data: JSON.stringify(localData),
            contentType: 'application/json;charset=UTF-8',
        })
            .then((data) => {
                console.log('Posted file upload',data);
                // location.reload(true);
                $.ajax({
                    url: url_refresh,
                    type: 'GET',
                })
                .then((data) => {
                    location.reload(true)
                    // var parsed = $.parseHTML(data);
                    // var divElement = $(parsed).find('#'+element.id)[0];
                    // $(element).replaceWith(divElement);
                    // var accessToken = divElement.dataset.token
                    // var file_id = divElement.dataset.file_id
                    // var container = divElement.className
                    // renderPreview_single(accessToken,container , file_id)

                })
                .catch((error) => {
                    console.log('Error refreshing booking',error);
                });
            })
            .catch((err) => {
                console.log('File upload error',err);
            });
};