document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".url-form");
    const urlInput = document.querySelector("#url-input");
    const submitBtn = document.querySelector(".url-submit-btn");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const youtubeUrl = urlInput.value;

        if (!youtubeUrl) {
            alert("Please enter a valid YouTube URL.");
            return;
        }

        const data = {
            yt_link: youtubeUrl,
        }

        const LoadingContainer = document.querySelector('.loading-mask');
        const loading = document.createElement('div');
        loading.classList.add('loading-container');

        LoadingContainer.appendChild(loading);

        $.ajax({
            url: "http://127.0.0.1:8000/music/upload_music",
            method: "POST",
            data: data,
            success: (res) => {
                console.log(res);

                window.location.href = "../analyze?yt_link=" + encodeURIComponent(youtubeUrl);
            },
            error: (res) => {
                console.error("Error:", res);
            },
        })
    });

});
