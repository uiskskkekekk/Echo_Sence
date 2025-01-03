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

        // 清空現有的相似音樂區域
        const MusicContainer = document.querySelector('.music-section .your-music')
        MusicContainer.innerHTML = "";
        const similarMusicContainer = document.querySelector('.similar-section .similar-music');

        if (res.original_data) {
            const originalMusic = res.original_data
            const musicItem = document.createElement('div');
            musicItem.classList.add('music-item');

            // 設置內部HTML
            musicItem.innerHTML = `
                <div class="thumbnail-placeholder">
                    <img src="${originalMusic.cover_url}" alt="${originalMusic.title}" />
                </div>
                <div class="music-info">
                    <p><strong>${originalMusic.title}</strong></p>
                    <p>${originalMusic.artist_name}</p>
                    <p>URL: <a href="${originalMusic.youtube_url}" target="_blank">${originalMusic.youtube_url}</a></p>
                </div>
            `;

            MusicContainer.appendChild(musicItem);
        }

        res.data.forEach((music) => {
            // 創建音樂項目元素
            const musicItem = document.createElement('div');
            musicItem.classList.add('music-item');

            // 設置內部HTML
            musicItem.innerHTML = `
                        <div class="thumbnail-placeholder">
                            <img src="${music.cover_url}" alt="${music.title}" />
                        </div>
                        <div class="music-info">
                            <p><strong>${music.title}</strong></p>
                            <p>${music.artist_name}</p>
                            <p>URL: <a href="${music.youtube_url}" target="_blank">${music.youtube_url}</a></p>
                        </div>
                        <div class="music-control">
                            <audio controls>
                                <source src="${music.preview_url}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                `;

            // 將新創建的音樂項目加入到相似音樂容器中
            similarMusicContainer.appendChild(musicItem);
        });
    },
    error: (res) => {
        console.error("Error:", res);
    },
})