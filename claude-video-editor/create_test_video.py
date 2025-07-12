#!/usr/bin/env python3
"""
Create a test video to demonstrate the Hollywood Editor
"""

import cv2
import numpy as np
from pathlib import Path
import math

def create_test_video():
    """Create a test video with various scenes"""
    
    # Video properties
    width, height = 1920, 1080
    fps = 30
    duration = 10  # seconds
    output_path = Path("test_video.mp4")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    if not writer.isOpened():
        print("Error: Could not create video writer")
        return None
    
    total_frames = fps * duration
    
    print(f"Creating {duration} second test video...")
    
    for frame_num in range(total_frames):
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Progress
        progress = frame_num / total_frames
        
        # Scene 1: Color gradient (0-3 seconds)
        if frame_num < fps * 3:
            # Animated gradient
            for y in range(height):
                for x in range(width):
                    frame[y, x] = [
                        int(255 * (x / width) * (1 - progress/0.3)),  # Red fades
                        int(255 * (y / height)),  # Green gradient
                        int(255 * progress / 0.3)  # Blue increases
                    ]
            
            # Add text
            cv2.putText(frame, "Scene 1: Color Gradients", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Scene 2: Moving shapes (3-6 seconds)
        elif frame_num < fps * 6:
            scene_progress = (frame_num - fps * 3) / (fps * 3)
            
            # Dark background
            frame[:] = (20, 20, 30)
            
            # Moving circle
            circle_x = int(width * scene_progress)
            circle_y = int(height/2 + 200 * math.sin(scene_progress * math.pi * 4))
            cv2.circle(frame, (circle_x, circle_y), 50, (255, 100, 100), -1)
            
            # Moving rectangle
            rect_x = int(width * (1 - scene_progress))
            cv2.rectangle(frame, (rect_x - 100, 200), (rect_x + 100, 400), 
                         (100, 255, 100), -1)
            
            # Add text
            cv2.putText(frame, "Scene 2: Motion & Shapes", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # Scene 3: Face simulation (6-10 seconds)
        else:
            scene_progress = (frame_num - fps * 6) / (fps * 4)
            
            # Light background
            frame[:] = (200, 180, 160)
            
            # Draw face-like shape
            face_center = (width//2, height//2)
            
            # Face circle
            cv2.circle(frame, face_center, 200, (150, 120, 90), -1)
            
            # Eyes
            eye_y = face_center[1] - 50
            cv2.circle(frame, (face_center[0] - 70, eye_y), 30, (50, 50, 50), -1)
            cv2.circle(frame, (face_center[0] + 70, eye_y), 30, (50, 50, 50), -1)
            
            # Animated smile
            smile_height = int(50 + 30 * math.sin(scene_progress * math.pi))
            cv2.ellipse(frame, (face_center[0], face_center[1] + 50), 
                       (100, smile_height), 0, 0, 180, (50, 50, 50), 3)
            
            # Add text
            cv2.putText(frame, "Scene 3: Face Detection Test", (50, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
        
        # Add frame counter
        cv2.putText(frame, f"Frame {frame_num}/{total_frames}", (width - 300, height - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add quality variations (some noise)
        if frame_num % 60 == 0:  # Every 2 seconds
            noise = np.random.randint(0, 20, frame.shape, dtype=np.uint8)
            frame = cv2.add(frame, noise)
        
        writer.write(frame)
    
    writer.release()
    
    if output_path.exists():
        file_size = output_path.stat().st_size / (1024 * 1024)
        print(f"✅ Test video created: {output_path}")
        print(f"   Size: {file_size:.2f} MB")
        print(f"   Duration: {duration} seconds")
        print(f"   Resolution: {width}x{height}")
        print(f"   FPS: {fps}")
        return str(output_path)
    else:
        print("❌ Failed to create test video")
        return None

if __name__ == "__main__":
    create_test_video()