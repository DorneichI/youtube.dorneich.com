# youtube.dorneich.com

A tiny personal site that shows new videos from a handful of YouTube
channels, in plain chronological order, with no recommendations, no
autoplay, and no algorithm deciding what I should watch next.

The point is to break loose from the YouTube algorithm — to browse
the channels I actually chose, on my terms, instead of getting pulled
into whatever the recommendation engine (and the platform's slow
enshittification) wants me to watch next.

A GitHub Action periodically pulls each channel's RSS feed and
regenerates the video list; the site itself is just static HTML/CSS/JS
serving that data.

## Disclaimer

This project is completely vibecoded — built by prompting an AI
coding assistant rather than hand-crafted. Expect rough edges.
