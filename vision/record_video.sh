#!/bin/bash

mkdir -p ~/Programs/Karen/Recordings

FILENAME="/home/ryn007/Programs/Karen/Recordings/video_$(date +%Y%m%d_%H%M%S).mp4"

# Record 10 seconds of video + audio
ffmpeg -f v4l2 -video_size 640x480 -framerate 25 -i /dev/video0 \
       -f alsa -i default \
       -t 10 -vcodec libx264 -preset ultrafast -acodec aac "$FILENAME"

echo "[Karen] Video saved to: $FILENAME"
