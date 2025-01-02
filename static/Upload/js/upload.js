document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".url-form");
    const urlInput = document.querySelector("#url-input");
    const submitBtn = document.querySelector(".url-submit-btn");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // 防止表單的默認提交行為

        const youtubeUrl = urlInput.value;

        // 檢查是否輸入 URL
        if (!youtubeUrl) {
            alert("Please enter a valid YouTube URL.");
            return;
        }

        // 發送 AJAX 請求
        fetch("/music/upload_music", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(), // 添加 CSRF Token
            },
            body: JSON.stringify({ yt_link: youtubeUrl }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                // 處理服務器的回應
                console.log(data);
                alert("YouTube URL has been successfully submitted!");
            })
            .catch((error) => {
                console.error("There was a problem with the fetch operation:", error);
                alert("An error occurred while submitting the URL.");
            });
    });

    // Helper function to get CSRF token
    function getCsrfToken() {
        const csrfCookie = document.cookie
            .split("; ")
            .find((row) => row.startsWith("csrftoken="));
        return csrfCookie ? csrfCookie.split("=")[1] : "";
    }
});
