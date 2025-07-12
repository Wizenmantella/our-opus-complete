#!/usr/bin/env python3
"""
Create Real Demo Video - Generate realistic content for viral editing
Creates a video with a person speaking (simulated) for viral content demonstration
"""

import cv2
import numpy as np
import subprocess
from pathlib import Path
import time

def create_speaking_demo_video():
    """Create a realistic demo video simulating someone speaking"""
    
    output_path = "raw_content.mp4"
    fps = 30
    duration = 45  # 45 seconds of content
    width, height = 1920, 1080
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Simulate different scenes
    scenes = [
        {"type": "intro", "duration": 5, "text": "The Secret Nobody Tells You"},
        {"type": "main_point_1", "duration": 10, "text": "First, you need to understand this..."},
        {"type": "main_point_2", "duration": 10, "text": "Here's what changed everything for me"},
        {"type": "main_point_3", "duration": 10, "text": "This one trick will blow your mind"},
        {"type": "outro", "duration": 10, "text": "Now you know the secret"}
    ]
    
    frame_count = 0
    
    for scene in scenes:
        scene_frames = int(scene["duration"] * fps)
        
        for i in range(scene_frames):
            # Create frame
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            
            # Background gradient
            for y in range(height):
                intensity = int(50 + (y / height) * 50)
                frame[y, :] = [intensity, intensity + 20, intensity + 10]
            
            # Add simulated face area (circle)
            face_center = (width // 2, height // 2 - 100)
            face_radius = 150
            
            # Animate face slightly (simulate talking)
            offset = int(10 * np.sin(frame_count * 0.3))
            cv2.circle(frame, (face_center[0], face_center[1] + offset), face_radius, (200, 180, 160), -1)
            
            # Add eyes
            eye_offset = int(5 * np.sin(frame_count * 0.5))
            cv2.circle(frame, (face_center[0] - 50, face_center[1] - 30 + eye_offset), 20, (50, 50, 50), -1)
            cv2.circle(frame, (face_center[0] + 50, face_center[1] - 30 + eye_offset), 20, (50, 50, 50), -1)
            
            # Add mouth (animated for talking effect)
            mouth_height = int(20 + 10 * np.sin(frame_count * 0.8))
            cv2.ellipse(frame, (face_center[0], face_center[1] + 50), (60, mouth_height), 0, 0, 180, (100, 50, 50), -1)
            
            # Add scene indicator
            cv2.putText(frame, f"Scene: {scene['type'].upper()}", (50, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add timestamp
            current_time = frame_count / fps
            cv2.putText(frame, f"{current_time:.1f}s", (width - 150, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add subtle motion
            if scene["type"] == "main_point_1":
                # Hand gesture simulation
                hand_x = int(width // 2 + 200 * np.sin(frame_count * 0.1))
                hand_y = int(height // 2 + 50 * np.cos(frame_count * 0.1))
                cv2.circle(frame, (hand_x, hand_y), 40, (200, 180, 160), -1)
            
            out.write(frame)
            frame_count += 1
    
    out.release()
    
    # Add audio track (sine wave speech simulation)
    audio_cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=200:duration={duration}",
        "-i", output_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest",
        "raw_content_with_audio.mp4"
    ]
    
    subprocess.run(audio_cmd, capture_output=True)
    
    # Clean up
    Path(output_path).unlink()
    Path("raw_content_with_audio.mp4").rename(output_path)
    
    print(f"✅ Created demo video: {output_path}")
    return output_path

if __name__ == "__main__":
    create_speaking_demo_video()