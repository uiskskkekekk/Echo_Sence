// 獲取 URL 中的參數
const urlParams = new URLSearchParams(window.location.search);
const ytLink = urlParams.get('yt_link');  // 這裡取得的是 "yt_link" 的參數值

const data = {
    yt_link: ytLink,
}


$.ajax({
    url: "http://127.0.0.1:8000/music/get_similiar_musics",
    method: "POST",
    data: data,
    success: (res) => {
        console.log(res);
    },
    error: (res) => {
        console.error("Error:", res);
    },
})