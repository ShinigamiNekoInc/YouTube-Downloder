const urlParams = new URLSearchParams(window.location.search);
const statusDiv = document.getElementById('status');
const type = urlParams.get('type');
const taskId = urlParams.get('task_id');

// Fetch folder size and update UI
async function updateDownloadSize() {
    try {
        const response = await fetch('php/get_folder_size.php');
        const data = await response.json();
        const sizeDisplay = document.getElementById('download_size');
        if (sizeDisplay) {
            let sizeStr = "";
            if (data.bytes > 1024 * 1024 * 1024) {
                sizeStr = (data.bytes / (1024 * 1024 * 1024)).toFixed(2) + " GB";
            } else {
                sizeStr = (data.bytes / (1024 * 1024)).toFixed(2) + " MB";
            }
            sizeDisplay.innerText = sizeStr;
        }
    } catch (e) {
        console.error("Error fetching folder size:", e);
    }
}

if (document.getElementById('download_size')) {
    updateDownloadSize();
}

if (type === 'started' && taskId) {
    statusDiv.style.display = 'block';
    const statusMsg = document.getElementById('status_msg');
    const downloadLink = document.getElementById('download_link');
    const successIcon = document.getElementById('success_icon');
    if (statusMsg) statusMsg.innerText = "Download started. Please wait...";
    if (downloadLink) downloadLink.style.visibility = 'hidden';
    if (successIcon) successIcon.style.display = 'none';
    statusDiv.className = 'success';

    const pollStatus = setInterval(async () => {
        try {
            const response = await fetch(`php/status.php?task_id=${taskId}`);
            const data = await response.json();

            if (data.status === 'completed') {
                clearInterval(pollStatus);
                const statusMsg = document.getElementById('status_msg');
                const downloadLink = document.getElementById('download_link');
                const successIcon = document.getElementById('success_icon');
                if (statusMsg) statusMsg.innerText = "Download Complete!";
                if (successIcon) successIcon.style.display = 'block';
                if (downloadLink) {
                    downloadLink.href = `php/stream_download.php?file=${encodeURIComponent(data.filename)}`;
                    downloadLink.style.visibility = 'visible';
                    downloadLink.innerText = "Download File";
                }
            } else if (data.status === 'error') {
                clearInterval(pollStatus);
                const statusMsg = document.getElementById('status_msg');
                if (statusMsg) statusMsg.innerText = "Error: " + data.message;
                statusDiv.className = 'error';
            }
        } catch (e) {
            console.error("Polling error:", e);
        }
    }, 3000);

} else if (type === 'update_started' && taskId) {
    statusDiv.style.display = 'block';
    const statusMsg = document.getElementById('status_msg');
    const downloadLink = document.getElementById('download_link');
    const successIcon = document.getElementById('success_icon');
    if (statusMsg) statusMsg.innerText = "Updating yt-dlp, please wait...";
    if (downloadLink) downloadLink.style.visibility = 'hidden';
    if (successIcon) successIcon.style.display = 'none';
    statusDiv.className = 'success';

    const pollStatus = setInterval(async () => {
        try {
            const response = await fetch(`php/status.php?task_id=${taskId}`);
            const data = await response.json();

             if (data.status === 'completed') {
                 clearInterval(pollStatus);
                 const statusMsg = document.getElementById('status_msg');
                 const successIcon = document.getElementById('success_icon');
                 if (statusMsg) statusMsg.innerText = "Update Complete!";
                 if (successIcon) successIcon.style.display = 'block';
             } else if (data.status === 'error') {
                 clearInterval(pollStatus);
                 const statusMsg = document.getElementById('status_msg');
                 if (statusMsg) statusMsg.innerText = "Update Error: " + data.message;
                 statusDiv.className = 'error';
             }
        } catch (e) {
            console.error("Polling error:", e);
        }
    }, 3000);

} else if (type === 'success') {
    statusDiv.style.display = 'block';
    const message = urlParams.get('message');
    const downloadUrl = urlParams.get('download');
    const statusMsg = document.getElementById('status_msg');
    const downloadLink = document.getElementById('download_link');
    const successIcon = document.getElementById('success_icon');
    if (statusMsg) statusMsg.innerText = message;
    if (successIcon) successIcon.style.display = 'block';
    if (downloadLink && downloadUrl) {
        downloadLink.href = downloadUrl;
        downloadLink.style.visibility = 'visible';
        downloadLink.innerText = "Download File";
    }
    statusDiv.className = 'success';

} else if (type === 'error') {
    statusDiv.style.display = 'block';
    const message = urlParams.get('message');
    const statusMsg = document.getElementById('status_msg');
    if (statusMsg) statusMsg.innerText = message;
    else statusDiv.innerText = message;
    statusDiv.className = 'error';
}
