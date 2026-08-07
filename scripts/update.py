import feedparser
import json
import re
import urllib.request
from datetime import datetime


HANDLES_FILE = "data/handles.txt"
CHANNEL_ID_CACHE_FILE = "data/channel_ids.json"
OUTPUT_FILE = "videos.json"


def load_channel_id_cache():
    try:
        with open(CHANNEL_ID_CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_channel_id_cache(cache):
    with open(CHANNEL_ID_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)
        f.write("\n")


def get_channel_id(handle):
    if not handle.startswith("@"):
        handle = "@" + handle

    url = f"https://www.youtube.com/{handle}"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    patterns = [
        r'"browseId":"(UC[a-zA-Z0-9_-]+)"',
        r'"channelId":"(UC[a-zA-Z0-9_-]+)"',
        r'"externalId":"(UC[a-zA-Z0-9_-]+)"'
    ]

    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)

    raise Exception(f"Could not resolve {handle}")


def get_videos(channel_id):
    """
    Get videos from a YouTube RSS feed.
    """

    rss_url = (
        "https://www.youtube.com/feeds/videos.xml"
        f"?channel_id={channel_id}"
    )

    feed = feedparser.parse(rss_url)

    videos = []

    for entry in feed.entries:
        video_id = entry.yt_videoid

        videos.append({
            "video_id": video_id,
            "channel": entry.author,
            "title": entry.title,
            "url": entry.link,
            "published": entry.published,
            "thumbnail": (
                f"https://i.ytimg.com/vi/"
                f"{video_id}/hqdefault.jpg"
            )
        })

    return videos


def main():

    with open(HANDLES_FILE, encoding="utf-8") as f:
        handles = [
            line.strip()
            for line in f
            if line.strip()
        ]

    channel_id_cache = load_channel_id_cache()

    all_videos = []

    for handle in handles:

        print(f"Processing {handle}")

        try:
            channel_id = channel_id_cache.get(handle)
            if channel_id is None:
                channel_id = get_channel_id(handle)
                channel_id_cache[handle] = channel_id

            videos = get_videos(channel_id)
        except Exception as error:
            print(f"Skipping {handle}: {error}")
            continue

        all_videos.extend(videos)

    save_channel_id_cache(channel_id_cache)


    all_videos.sort(
        key=lambda video: datetime.fromisoformat(
            video["published"].replace("Z", "+00:00")
        ),
        reverse=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            all_videos,
            f,
            indent=2,
            ensure_ascii=False
        )


    print(
        f"Wrote {len(all_videos)} videos to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()