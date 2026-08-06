const params = new URLSearchParams(window.location.search);
const videoId = params.get("videoid");

const playerContainer = document.getElementById("player");
const titleElement = document.getElementById("title");


if (!videoId) {
    playerContainer.textContent = "No video selected.";
} else {

    fetch("../videos.json")
        .then(response => response.json())
        .then(videos => {

            const video = videos.find(
                video => video.video_id === videoId
            );

            if (!video) {
                playerContainer.textContent =
                    "Video not found.";
                return;
            }


            titleElement.textContent = video.title;


            const iframe = document.createElement("iframe");

            iframe.width = "854";
            iframe.height = "480";
            iframe.src =
                `https://www.youtube.com/embed/${video.video_id}`;

            iframe.allowFullscreen = true;

            playerContainer.innerHTML = "";
            playerContainer.appendChild(iframe);


            const channel = document.createElement("p");
            channel.textContent =
                video.channel;


            const date = document.createElement("p");

            date.textContent =
                new Date(video.published)
                    .toLocaleDateString(
                        undefined,
                        {
                            year: "numeric",
                            month: "long",
                            day: "numeric"
                        }
                    );


            playerContainer.appendChild(channel);
            playerContainer.appendChild(date);

        })
        .catch(error => {
            playerContainer.textContent =
                "Failed to load video.";

            console.error(error);
        });

}