const videosContainer = document.getElementById("videos");

fetch("videos.json")
    .then(response => response.json())
    .then(videos => {

        videosContainer.innerHTML = "";

        videos.forEach(video => {

            const date = new Date(video.published);

            const formattedDate = date.toLocaleDateString(
                undefined,
                {
                    year: "numeric",
                    month: "long",
                    day: "numeric"
                }
            );

            const videoLink = document.createElement("a");
            videoLink.href = `player/?videoid=${video.video_id}`;
            videoLink.style.textDecoration = "none";
            videoLink.style.color = "inherit";

            const table = document.createElement("table");

            const row = document.createElement("tr");

            const thumbnailCell = document.createElement("td");

            const thumbnail = document.createElement("img");
            thumbnail.src = video.thumbnail;
            thumbnail.width = 240;
            thumbnail.alt = video.title;

            thumbnailCell.appendChild(thumbnail);


            const infoCell = document.createElement("td");

            const title = document.createElement("h2");
            title.textContent = video.title;

            const channel = document.createElement("p");
            channel.textContent = video.channel;

            const dateText = document.createElement("p");
            dateText.textContent = formattedDate;

            infoCell.appendChild(title);
            infoCell.appendChild(channel);
            infoCell.appendChild(dateText);


            row.appendChild(thumbnailCell);
            row.appendChild(infoCell);

            table.appendChild(row);

            videoLink.appendChild(table);

            videosContainer.appendChild(videoLink);

            videosContainer.appendChild(
                document.createElement("br")
            );
        });

    })
    .catch(error => {
        videosContainer.textContent =
            "Failed to load videos.";
        console.error(error);
    });