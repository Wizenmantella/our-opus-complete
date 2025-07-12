#!/bin/bash
# Fix all videos for QuickTime compatibility

echo "🎬 Converting all videos to QuickTime format..."

# Convert showcase videos
for video in showcase_output/*.mp4 viral_showcase/*.mp4 viral_final/*.mp4; do
    if [ -f "$video" ]; then
        echo "Converting $video..."
        python3 quicktime_convert.py "$video"
    fi
done

# Convert desktop videos
for video in ~/Desktop/Videos/*.mp4; do
    if [ -f "$video" ]; then
        echo "Converting $video..."
        python3 quicktime_convert.py "$video"
    fi
done

echo "✅ Conversion complete!"
