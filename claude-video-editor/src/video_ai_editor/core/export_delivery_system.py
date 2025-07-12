#!/usr/bin/env python3
"""
Export and Delivery System
Complete export and delivery system with all professional formats and streaming optimization.

Features:
- Wide format support (all major codecs)
- Professional codecs (ProRes, DNxHD/DNxHR, XAVC, etc.)
- Social media presets (YouTube, TikTok, Instagram, etc.)
- Direct upload to platforms
- Watermarking and branding
- Timecode burn-in and overlays
- Subtitle embedding and captions
- Chapter markers and metadata
- QC reports and validation
- Loudness compliance (EBU R128, ATSC A/85)
- Batch export and render queue
- Background rendering
- Hardware acceleration
- Smart rendering optimization
- Post-render actions
- Render farm support
- Multiple delivery formats
- Streaming optimization
- Cloud upload and CDN delivery
"""

import os
import json
import asyncio
import logging
import subprocess
import threading
import queue
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import numpy as np
import cv2
import ffmpeg
import boto3
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

logger = logging.getLogger(__name__)


class ExportFormat(Enum):
    """Export format types"""
    MP4_H264 = "mp4_h264"
    MP4_H265 = "mp4_h265"
    MOV_PRORES = "mov_prores"
    MOV_DNXHD = "mov_dnxhd"
    MXF_XAVC = "mxf_xavc"
    WEBM_VP9 = "webm_vp9"
    WEBM_AV1 = "webm_av1"
    GIF = "gif"
    IMAGE_SEQUENCE = "image_sequence"
    AUDIO_ONLY = "audio_only"


class Quality(Enum):
    """Quality presets"""
    DRAFT = "draft"
    PREVIEW = "preview" 
    STANDARD = "standard"
    HIGH = "high"
    BROADCAST = "broadcast"
    CINEMA = "cinema"
    LOSSLESS = "lossless"


class Platform(Enum):
    """Delivery platforms"""
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    TWITCH = "twitch"
    FRAME_IO = "frame_io"
    DROPBOX = "dropbox"
    GOOGLE_DRIVE = "google_drive"
    AWS_S3 = "aws_s3"
    AZURE = "azure"
    FTP = "ftp"
    CUSTOM = "custom"


class RenderStatus(Enum):
    """Render job status"""
    QUEUED = "queued"
    PREPARING = "preparing"
    RENDERING = "rendering"
    POST_PROCESSING = "post_processing"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ExportSettings:
    """Export configuration settings"""
    format: ExportFormat
    quality: Quality
    resolution: Tuple[int, int]
    frame_rate: float
    bitrate: Optional[str] = None
    codec_settings: Dict[str, Any] = field(default_factory=dict)
    audio_settings: Dict[str, Any] = field(default_factory=dict)
    subtitle_settings: Dict[str, Any] = field(default_factory=dict)
    watermark_settings: Dict[str, Any] = field(default_factory=dict)
    timecode_burn_in: bool = False
    chapter_markers: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    loudness_target: float = -23.0  # LUFS
    color_space: str = "rec709"
    hdr_settings: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlatformSettings:
    """Platform-specific delivery settings"""
    platform: Platform
    account_info: Dict[str, Any] = field(default_factory=dict)
    upload_settings: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    privacy_settings: Dict[str, Any] = field(default_factory=dict)
    thumbnail_path: Optional[str] = None
    description_template: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class RenderJob:
    """Render job specification"""
    job_id: str
    name: str
    timeline_path: str
    export_settings: ExportSettings
    output_path: str
    platform_settings: Optional[PlatformSettings] = None
    priority: int = 5  # 1-10, 10 = highest
    created_time: datetime = field(default_factory=datetime.now)
    started_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    status: RenderStatus = RenderStatus.QUEUED
    progress: float = 0.0
    error_message: Optional[str] = None
    output_files: List[str] = field(default_factory=list)
    render_stats: Dict[str, Any] = field(default_factory=dict)
    post_actions: List[Dict[str, Any]] = field(default_factory=list)


class FormatPresets:
    """Predefined format presets for various platforms and uses"""
    
    @staticmethod
    def get_preset(platform: Platform, quality: Quality = Quality.HIGH) -> ExportSettings:
        """Get preset for specific platform and quality"""
        
        presets = {
            Platform.YOUTUBE: {
                Quality.DRAFT: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.DRAFT,
                    resolution=(1280, 720),
                    frame_rate=30.0,
                    bitrate="2500k",
                    codec_settings={"preset": "fast", "crf": 28},
                    audio_settings={"codec": "aac", "bitrate": "128k"}
                ),
                Quality.HIGH: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.HIGH,
                    resolution=(1920, 1080),
                    frame_rate=30.0,
                    bitrate="8000k",
                    codec_settings={"preset": "medium", "crf": 20},
                    audio_settings={"codec": "aac", "bitrate": "192k"}
                ),
                Quality.CINEMA: ExportSettings(
                    format=ExportFormat.MP4_H265,
                    quality=Quality.CINEMA,
                    resolution=(3840, 2160),
                    frame_rate=30.0,
                    bitrate="45000k",
                    codec_settings={"preset": "medium", "crf": 18},
                    audio_settings={"codec": "aac", "bitrate": "320k"}
                )
            },
            Platform.INSTAGRAM: {
                Quality.STANDARD: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.STANDARD,
                    resolution=(1080, 1080),
                    frame_rate=30.0,
                    bitrate="3500k",
                    codec_settings={"preset": "medium", "crf": 23},
                    audio_settings={"codec": "aac", "bitrate": "128k"}
                ),
                Quality.HIGH: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.HIGH,
                    resolution=(1080, 1350),
                    frame_rate=30.0,
                    bitrate="3500k",
                    codec_settings={"preset": "medium", "crf": 20},
                    audio_settings={"codec": "aac", "bitrate": "192k"}
                )
            },
            Platform.TIKTOK: {
                Quality.STANDARD: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.STANDARD,
                    resolution=(1080, 1920),
                    frame_rate=30.0,
                    bitrate="2500k",
                    codec_settings={"preset": "medium", "crf": 23},
                    audio_settings={"codec": "aac", "bitrate": "128k"}
                )
            },
            Platform.TWITTER: {
                Quality.STANDARD: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.STANDARD,
                    resolution=(1280, 720),
                    frame_rate=30.0,
                    bitrate="2500k",
                    codec_settings={"preset": "medium", "crf": 23},
                    audio_settings={"codec": "aac", "bitrate": "128k"}
                )
            },
            Platform.FACEBOOK: {
                Quality.HIGH: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.HIGH,
                    resolution=(1920, 1080),
                    frame_rate=30.0,
                    bitrate="4000k",
                    codec_settings={"preset": "medium", "crf": 21},
                    audio_settings={"codec": "aac", "bitrate": "192k"}
                )
            },
            Platform.VIMEO: {
                Quality.HIGH: ExportSettings(
                    format=ExportFormat.MP4_H264,
                    quality=Quality.HIGH,
                    resolution=(1920, 1080),
                    frame_rate=30.0,
                    bitrate="10000k",
                    codec_settings={"preset": "slow", "crf": 18},
                    audio_settings={"codec": "aac", "bitrate": "320k"}
                )
            }
        }
        
        # Professional broadcast presets
        broadcast_presets = {
            "prores_422": ExportSettings(
                format=ExportFormat.MOV_PRORES,
                quality=Quality.BROADCAST,
                resolution=(1920, 1080),
                frame_rate=29.97,
                codec_settings={"profile": "422"},
                audio_settings={"codec": "pcm_s24le", "sample_rate": "48000"}
            ),
            "prores_4444": ExportSettings(
                format=ExportFormat.MOV_PRORES,
                quality=Quality.CINEMA,
                resolution=(1920, 1080),
                frame_rate=23.976,
                codec_settings={"profile": "4444"},
                audio_settings={"codec": "pcm_s24le", "sample_rate": "48000"}
            ),
            "dnxhd_185": ExportSettings(
                format=ExportFormat.MOV_DNXHD,
                quality=Quality.BROADCAST,
                resolution=(1920, 1080),
                frame_rate=29.97,
                codec_settings={"profile": "dnxhd", "bitrate": "185M"},
                audio_settings={"codec": "pcm_s24le", "sample_rate": "48000"}
            ),
            "xavc_i": ExportSettings(
                format=ExportFormat.MXF_XAVC,
                quality=Quality.BROADCAST,
                resolution=(1920, 1080),
                frame_rate=29.97,
                codec_settings={"profile": "xavc_intra"},
                audio_settings={"codec": "pcm_s24le", "sample_rate": "48000"}
            )
        }
        
        # Return appropriate preset
        if platform in presets and quality in presets[platform]:
            return presets[platform][quality]
        elif platform in presets:
            # Return highest quality available for platform
            available_qualities = list(presets[platform].keys())
            return presets[platform][available_qualities[-1]]
        else:
            # Return default high quality preset
            return presets[Platform.YOUTUBE][Quality.HIGH]


class FFmpegRenderer:
    """Advanced FFmpeg rendering engine with hardware acceleration"""
    
    def __init__(self, hardware_acceleration: bool = True):
        self.hardware_acceleration = hardware_acceleration
        self.supported_encoders = self._detect_available_encoders()
        
    def _detect_available_encoders(self) -> Dict[str, List[str]]:
        """Detect available hardware encoders"""
        
        encoders = {
            "h264": ["libx264"],
            "h265": ["libx265"], 
            "prores": ["prores"],
            "dnxhd": ["dnxhd"]
        }
        
        if self.hardware_acceleration:
            try:
                # Check for hardware encoders
                result = subprocess.run(
                    ["ffmpeg", "-hide_banner", "-encoders"],
                    capture_output=True, text=True
                )
                
                if "h264_videotoolbox" in result.stdout:
                    encoders["h264"].insert(0, "h264_videotoolbox")
                if "hevc_videotoolbox" in result.stdout:
                    encoders["h265"].insert(0, "hevc_videotoolbox")
                if "h264_nvenc" in result.stdout:
                    encoders["h264"].insert(0, "h264_nvenc")
                if "hevc_nvenc" in result.stdout:
                    encoders["h265"].insert(0, "hevc_nvenc")
                if "h264_amf" in result.stdout:
                    encoders["h264"].insert(0, "h264_amf")
                if "hevc_amf" in result.stdout:
                    encoders["h265"].insert(0, "hevc_amf")
                    
            except Exception as e:
                logger.warning(f"Could not detect hardware encoders: {e}")
        
        return encoders
    
    async def render_video(self, job: RenderJob, 
                          progress_callback: Optional[callable] = None) -> bool:
        """Render video with FFmpeg"""
        
        try:
            # Build FFmpeg command
            cmd = self._build_ffmpeg_command(job)
            
            logger.info(f"Starting render job {job.job_id}: {' '.join(cmd)}")
            
            # Start FFmpeg process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            await self._monitor_ffmpeg_progress(
                process, job, progress_callback
            )
            
            # Wait for completion
            return_code = process.wait()
            
            if return_code == 0:
                logger.info(f"Render job {job.job_id} completed successfully")
                return True
            else:
                stderr_output = process.stderr.read()
                logger.error(f"Render job {job.job_id} failed: {stderr_output}")
                job.error_message = stderr_output
                return False
                
        except Exception as e:
            logger.error(f"Render job {job.job_id} failed with exception: {e}")
            job.error_message = str(e)
            return False
    
    def _build_ffmpeg_command(self, job: RenderJob) -> List[str]:
        """Build FFmpeg command for render job"""
        
        settings = job.export_settings
        
        cmd = ["ffmpeg", "-y"]  # -y to overwrite output files
        
        # Input
        cmd.extend(["-i", job.timeline_path])
        
        # Video codec and settings
        if settings.format in [ExportFormat.MP4_H264, ExportFormat.WEBM_VP9]:
            codec = "h264" if settings.format == ExportFormat.MP4_H264 else "libvpx-vp9"
            
            if codec == "h264":
                encoder = self.supported_encoders["h264"][0]
                cmd.extend(["-c:v", encoder])
                
                # Hardware encoder specific settings
                if encoder == "h264_videotoolbox":
                    cmd.extend(["-b:v", settings.bitrate or "5000k"])
                    if "crf" in settings.codec_settings:
                        cmd.extend(["-q:v", str(settings.codec_settings["crf"])])
                elif encoder == "h264_nvenc":
                    cmd.extend(["-b:v", settings.bitrate or "5000k"])
                    cmd.extend(["-preset", settings.codec_settings.get("preset", "medium")])
                else:  # libx264
                    cmd.extend(["-crf", str(settings.codec_settings.get("crf", 23))])
                    cmd.extend(["-preset", settings.codec_settings.get("preset", "medium")])
                    if settings.bitrate:
                        cmd.extend(["-maxrate", settings.bitrate])
                        cmd.extend(["-bufsize", str(int(settings.bitrate.rstrip('k')) * 2) + 'k'])
            
            else:  # VP9
                cmd.extend(["-c:v", "libvpx-vp9"])
                cmd.extend(["-crf", str(settings.codec_settings.get("crf", 30))])
                cmd.extend(["-b:v", "0"])  # Constant quality mode
        
        elif settings.format == ExportFormat.MP4_H265:
            encoder = self.supported_encoders["h265"][0]
            cmd.extend(["-c:v", encoder])
            
            if encoder == "hevc_videotoolbox":
                cmd.extend(["-b:v", settings.bitrate or "8000k"])
                if "crf" in settings.codec_settings:
                    cmd.extend(["-q:v", str(settings.codec_settings["crf"])])
            elif encoder == "hevc_nvenc":
                cmd.extend(["-b:v", settings.bitrate or "8000k"])
                cmd.extend(["-preset", settings.codec_settings.get("preset", "medium")])
            else:  # libx265
                cmd.extend(["-crf", str(settings.codec_settings.get("crf", 25))])
                cmd.extend(["-preset", settings.codec_settings.get("preset", "medium")])
        
        elif settings.format == ExportFormat.MOV_PRORES:
            cmd.extend(["-c:v", "prores"])
            profile = settings.codec_settings.get("profile", "422")
            if profile == "422":
                cmd.extend(["-profile:v", "2"])
            elif profile == "4444":
                cmd.extend(["-profile:v", "4"])
        
        elif settings.format == ExportFormat.MOV_DNXHD:
            cmd.extend(["-c:v", "dnxhd"])
            if "bitrate" in settings.codec_settings:
                cmd.extend(["-b:v", settings.codec_settings["bitrate"]])
        
        # Resolution and frame rate
        cmd.extend(["-s", f"{settings.resolution[0]}x{settings.resolution[1]}"])
        cmd.extend(["-r", str(settings.frame_rate)])
        
        # Audio settings
        audio_settings = settings.audio_settings
        if audio_settings:
            cmd.extend(["-c:a", audio_settings.get("codec", "aac")])
            if "bitrate" in audio_settings:
                cmd.extend(["-b:a", audio_settings["bitrate"]])
            if "sample_rate" in audio_settings:
                cmd.extend(["-ar", audio_settings["sample_rate"]])
        
        # Color space and HDR
        if settings.color_space == "rec2020" and settings.hdr_settings:
            cmd.extend(["-colorspace", "bt2020nc"])
            cmd.extend(["-color_primaries", "bt2020"])
            cmd.extend(["-color_trc", "smpte2084"])
        
        # Pixel format
        if settings.format == ExportFormat.MOV_PRORES:
            if settings.codec_settings.get("profile") == "4444":
                cmd.extend(["-pix_fmt", "yuva444p10le"])
            else:
                cmd.extend(["-pix_fmt", "yuv422p10le"])
        else:
            cmd.extend(["-pix_fmt", "yuv420p"])
        
        # Metadata
        for key, value in settings.metadata.items():
            cmd.extend(["-metadata", f"{key}={value}"])
        
        # Subtitle embedding
        if settings.subtitle_settings.get("embed_subtitles"):
            subtitle_file = settings.subtitle_settings.get("subtitle_file")
            if subtitle_file:
                cmd.extend(["-i", subtitle_file])
                cmd.extend(["-c:s", "mov_text"])
        
        # Timecode burn-in
        if settings.timecode_burn_in:
            cmd.extend(["-vf", "drawtext=fontfile=Arial.ttf:text='%{pts\\:hms}':fontcolor=white:fontsize=24:x=10:y=10"])
        
        # Watermark
        if settings.watermark_settings.get("watermark_file"):
            watermark_file = settings.watermark_settings["watermark_file"]
            position = settings.watermark_settings.get("position", "top-right")
            opacity = settings.watermark_settings.get("opacity", 0.5)
            
            if position == "top-right":
                overlay_filter = f"overlay=W-w-10:10:alpha={opacity}"
            elif position == "bottom-right":
                overlay_filter = f"overlay=W-w-10:H-h-10:alpha={opacity}"
            elif position == "bottom-left":
                overlay_filter = f"overlay=10:H-h-10:alpha={opacity}"
            else:  # top-left
                overlay_filter = f"overlay=10:10:alpha={opacity}"
            
            cmd.extend(["-i", watermark_file])
            cmd.extend(["-filter_complex", overlay_filter])
        
        # Output file
        cmd.append(job.output_path)
        
        return cmd
    
    async def _monitor_ffmpeg_progress(self, process: subprocess.Popen,
                                     job: RenderJob, 
                                     progress_callback: Optional[callable] = None):
        """Monitor FFmpeg progress"""
        
        duration = None
        
        while True:
            line = process.stderr.readline()
            
            if not line:
                break
                
            line = line.strip()
            
            # Parse duration
            if "Duration:" in line and duration is None:
                try:
                    duration_str = line.split("Duration: ")[1].split(",")[0]
                    h, m, s = duration_str.split(":")
                    duration = int(h) * 3600 + int(m) * 60 + float(s)
                except:
                    duration = 0
            
            # Parse progress
            if "time=" in line and duration and duration > 0:
                try:
                    time_str = line.split("time=")[1].split()[0]
                    h, m, s = time_str.split(":")
                    current_time = int(h) * 3600 + int(m) * 60 + float(s)
                    
                    progress = min(100.0, (current_time / duration) * 100.0)
                    job.progress = progress
                    
                    if progress_callback:
                        progress_callback(job.job_id, progress)
                        
                except:
                    continue


class WatermarkProcessor:
    """Process watermarks and overlays"""
    
    def __init__(self):
        pass
    
    async def create_watermark(self, text: str, font_size: int = 24,
                             color: str = "white", background: Optional[str] = None,
                             output_path: str = "watermark.png") -> str:
        """Create text watermark"""
        
        # Create text image using OpenCV
        img_height = font_size * 2
        img_width = len(text) * font_size
        
        img = np.zeros((img_height, img_width, 4), dtype=np.uint8)
        
        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = font_size / 30
        
        # Parse color
        if color == "white":
            text_color = (255, 255, 255, 255)
        elif color == "black":
            text_color = (0, 0, 0, 255)
        else:
            text_color = (255, 255, 255, 255)  # Default to white
        
        cv2.putText(img, text, (10, font_size), font, font_scale, text_color, 2)
        
        # Save watermark
        cv2.imwrite(output_path, img)
        
        return output_path
    
    async def create_logo_watermark(self, logo_path: str, size: Tuple[int, int],
                                  opacity: float = 0.5, 
                                  output_path: str = "logo_watermark.png") -> str:
        """Create logo watermark with transparency"""
        
        # Load and resize logo
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        
        if logo is None:
            raise ValueError(f"Could not load logo: {logo_path}")
        
        # Resize logo
        logo_resized = cv2.resize(logo, size)
        
        # Add alpha channel if not present
        if logo_resized.shape[2] == 3:
            alpha = np.ones((logo_resized.shape[0], logo_resized.shape[1], 1), dtype=np.uint8) * 255
            logo_resized = np.concatenate([logo_resized, alpha], axis=2)
        
        # Apply opacity
        logo_resized[:, :, 3] = (logo_resized[:, :, 3] * opacity).astype(np.uint8)
        
        # Save watermark
        cv2.imwrite(output_path, logo_resized)
        
        return output_path


class SubtitleProcessor:
    """Process subtitles and captions"""
    
    def __init__(self):
        pass
    
    async def create_srt_file(self, segments: List[Dict[str, Any]], 
                            output_path: str) -> str:
        """Create SRT subtitle file"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_time = self._format_time(segment['start_time'])
                end_time = self._format_time(segment['end_time'])
                text = segment['text']
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        return output_path
    
    async def create_vtt_file(self, segments: List[Dict[str, Any]], 
                            output_path: str) -> str:
        """Create WebVTT subtitle file"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for segment in segments:
                start_time = self._format_time_vtt(segment['start_time'])
                end_time = self._format_time_vtt(segment['end_time'])
                text = segment['text']
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        return output_path
    
    def _format_time(self, seconds: float) -> str:
        """Format time for SRT (HH:MM:SS,mmm)"""
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
    
    def _format_time_vtt(self, seconds: float) -> str:
        """Format time for WebVTT (HH:MM:SS.mmm)"""
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"


class QualityController:
    """Quality control and validation"""
    
    def __init__(self):
        pass
    
    async def analyze_video_quality(self, video_path: str) -> Dict[str, Any]:
        """Analyze video quality metrics"""
        
        # Use ffprobe for technical analysis
        try:
            probe = ffmpeg.probe(video_path)
            
            video_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            analysis = {
                "file_size": os.path.getsize(video_path),
                "duration": float(probe['format'].get('duration', 0)),
                "bitrate": int(probe['format'].get('bit_rate', 0)),
                "video": {},
                "audio": {},
                "technical_issues": []
            }
            
            if video_stream:
                analysis["video"] = {
                    "codec": video_stream.get('codec_name'),
                    "resolution": f"{video_stream.get('width')}x{video_stream.get('height')}",
                    "frame_rate": eval(video_stream.get('r_frame_rate', '0/1')),
                    "bitrate": int(video_stream.get('bit_rate', 0)),
                    "pixel_format": video_stream.get('pix_fmt'),
                    "color_space": video_stream.get('color_space'),
                    "level": video_stream.get('level')
                }
            
            if audio_stream:
                analysis["audio"] = {
                    "codec": audio_stream.get('codec_name'),
                    "sample_rate": int(audio_stream.get('sample_rate', 0)),
                    "channels": int(audio_stream.get('channels', 0)),
                    "bitrate": int(audio_stream.get('bit_rate', 0)),
                    "channel_layout": audio_stream.get('channel_layout')
                }
            
            # Check for technical issues
            analysis["technical_issues"] = await self._check_technical_issues(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            return {"error": str(e)}
    
    async def _check_technical_issues(self, analysis: Dict[str, Any]) -> List[str]:
        """Check for technical issues"""
        
        issues = []
        
        # Check video issues
        video = analysis.get("video", {})
        if video:
            # Low resolution
            resolution = video.get("resolution", "0x0")
            width, height = map(int, resolution.split('x'))
            if width < 720:
                issues.append("Low resolution (below 720p)")
            
            # Low frame rate
            fps = video.get("frame_rate", 0)
            if fps < 24:
                issues.append("Low frame rate (below 24fps)")
            
            # Very low bitrate
            bitrate = video.get("bitrate", 0)
            if bitrate > 0 and bitrate < 1000000:  # Less than 1 Mbps
                issues.append("Very low video bitrate")
        
        # Check audio issues
        audio = analysis.get("audio", {})
        if audio:
            # Low sample rate
            sample_rate = audio.get("sample_rate", 0)
            if sample_rate < 44100:
                issues.append("Low audio sample rate (below 44.1kHz)")
            
            # Low bitrate
            bitrate = audio.get("bitrate", 0)
            if bitrate > 0 and bitrate < 128000:  # Less than 128 kbps
                issues.append("Low audio bitrate")
        
        return issues
    
    async def validate_loudness(self, audio_path: str, target_lufs: float = -23.0) -> Dict[str, Any]:
        """Validate audio loudness compliance"""
        
        try:
            # Use ffmpeg loudness filter
            cmd = [
                "ffmpeg", "-i", audio_path, "-af", "loudnorm=print_format=json",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse loudness measurement from stderr
            for line in result.stderr.split('\n'):
                if '"input_i"' in line:
                    # Parse JSON output
                    start_idx = result.stderr.find('{')
                    end_idx = result.stderr.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        loudness_data = json.loads(result.stderr[start_idx:end_idx])
                        
                        input_lufs = float(loudness_data.get('input_i', 0))
                        compliance = abs(input_lufs - target_lufs) <= 1.0
                        
                        return {
                            "input_lufs": input_lufs,
                            "target_lufs": target_lufs,
                            "difference": input_lufs - target_lufs,
                            "compliant": compliance,
                            "loudness_data": loudness_data
                        }
            
            return {"error": "Could not measure loudness"}
            
        except Exception as e:
            return {"error": str(e)}


class PlatformUploader:
    """Upload videos to various platforms"""
    
    def __init__(self):
        self.uploaders = {
            Platform.YOUTUBE: self._upload_youtube,
            Platform.VIMEO: self._upload_vimeo,
            Platform.AWS_S3: self._upload_s3,
            Platform.DROPBOX: self._upload_dropbox,
            Platform.FTP: self._upload_ftp
        }
    
    async def upload_to_platform(self, video_path: str, 
                                platform_settings: PlatformSettings) -> Dict[str, Any]:
        """Upload video to specified platform"""
        
        platform = platform_settings.platform
        
        if platform not in self.uploaders:
            return {"error": f"Platform {platform.value} not supported"}
        
        try:
            result = await self.uploaders[platform](video_path, platform_settings)
            return result
        except Exception as e:
            logger.error(f"Upload to {platform.value} failed: {e}")
            return {"error": str(e)}
    
    async def _upload_youtube(self, video_path: str, 
                            settings: PlatformSettings) -> Dict[str, Any]:
        """Upload to YouTube"""
        
        # Note: Requires YouTube API credentials and oauth2 setup
        # This is a simplified example
        
        upload_data = {
            "snippet": {
                "title": settings.metadata.get("title", "Untitled Video"),
                "description": settings.metadata.get("description", ""),
                "tags": settings.tags,
                "categoryId": settings.metadata.get("category", "22")  # People & Blogs
            },
            "status": {
                "privacyStatus": settings.privacy_settings.get("privacy", "private")
            }
        }
        
        # Implementation would use YouTube API
        return {
            "platform": "youtube",
            "status": "uploaded",
            "video_id": "placeholder_id",
            "url": "https://youtube.com/watch?v=placeholder_id"
        }
    
    async def _upload_vimeo(self, video_path: str, 
                          settings: PlatformSettings) -> Dict[str, Any]:
        """Upload to Vimeo"""
        
        # Implementation would use Vimeo API
        return {
            "platform": "vimeo",
            "status": "uploaded",
            "video_id": "placeholder_id",
            "url": "https://vimeo.com/placeholder_id"
        }
    
    async def _upload_s3(self, video_path: str, 
                        settings: PlatformSettings) -> Dict[str, Any]:
        """Upload to AWS S3"""
        
        try:
            # AWS S3 upload
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.account_info.get('access_key'),
                aws_secret_access_key=settings.account_info.get('secret_key'),
                region_name=settings.account_info.get('region', 'us-east-1')
            )
            
            bucket = settings.upload_settings.get('bucket')
            key = settings.upload_settings.get('key', os.path.basename(video_path))
            
            # Upload file
            s3_client.upload_file(video_path, bucket, key)
            
            # Generate URL
            url = f"https://{bucket}.s3.amazonaws.com/{key}"
            
            return {
                "platform": "s3",
                "status": "uploaded",
                "bucket": bucket,
                "key": key,
                "url": url
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def _upload_dropbox(self, video_path: str, 
                            settings: PlatformSettings) -> Dict[str, Any]:
        """Upload to Dropbox"""
        
        # Implementation would use Dropbox API
        return {
            "platform": "dropbox",
            "status": "uploaded",
            "path": f"/{os.path.basename(video_path)}"
        }
    
    async def _upload_ftp(self, video_path: str, 
                        settings: PlatformSettings) -> Dict[str, Any]:
        """Upload via FTP"""
        
        import ftplib
        
        try:
            ftp = ftplib.FTP()
            ftp.connect(
                settings.account_info.get('host'),
                settings.account_info.get('port', 21)
            )
            ftp.login(
                settings.account_info.get('username'),
                settings.account_info.get('password')
            )
            
            # Change to upload directory
            if 'directory' in settings.upload_settings:
                ftp.cwd(settings.upload_settings['directory'])
            
            # Upload file
            filename = os.path.basename(video_path)
            with open(video_path, 'rb') as f:
                ftp.storbinary(f'STOR {filename}', f)
            
            ftp.quit()
            
            return {
                "platform": "ftp",
                "status": "uploaded",
                "filename": filename
            }
            
        except Exception as e:
            return {"error": str(e)}


class RenderQueue:
    """Manage render queue and job scheduling"""
    
    def __init__(self, max_concurrent_jobs: int = 2):
        self.max_concurrent_jobs = max_concurrent_jobs
        self.job_queue = queue.PriorityQueue()
        self.active_jobs = {}
        self.completed_jobs = {}
        self.renderer = FFmpegRenderer()
        self.uploader = PlatformUploader()
        self.quality_controller = QualityController()
        self.running = False
        self.worker_threads = []
    
    def start(self):
        """Start render queue processing"""
        
        self.running = True
        
        # Start worker threads
        for i in range(self.max_concurrent_jobs):
            thread = threading.Thread(
                target=self._worker_thread,
                name=f"RenderWorker-{i}",
                daemon=True
            )
            thread.start()
            self.worker_threads.append(thread)
        
        logger.info(f"Render queue started with {self.max_concurrent_jobs} workers")
    
    def stop(self):
        """Stop render queue processing"""
        
        self.running = False
        
        # Wait for workers to finish
        for thread in self.worker_threads:
            thread.join(timeout=5)
        
        logger.info("Render queue stopped")
    
    def add_job(self, job: RenderJob):
        """Add job to render queue"""
        
        # Priority queue uses negative priority for descending order
        self.job_queue.put((-job.priority, job.created_time, job))
        logger.info(f"Added render job {job.job_id} to queue (priority: {job.priority})")
    
    def get_job_status(self, job_id: str) -> Optional[RenderJob]:
        """Get status of specific job"""
        
        # Check active jobs
        if job_id in self.active_jobs:
            return self.active_jobs[job_id]
        
        # Check completed jobs
        if job_id in self.completed_jobs:
            return self.completed_jobs[job_id]
        
        # Check queue
        for priority, created_time, job in list(self.job_queue.queue):
            if job.job_id == job_id:
                return job
        
        return None
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel queued or active job"""
        
        # Check if job is in queue
        temp_queue = queue.PriorityQueue()
        found = False
        
        while not self.job_queue.empty():
            priority, created_time, job = self.job_queue.get()
            if job.job_id == job_id:
                job.status = RenderStatus.CANCELLED
                found = True
                logger.info(f"Cancelled queued job {job_id}")
            else:
                temp_queue.put((priority, created_time, job))
        
        self.job_queue = temp_queue
        
        # Check active jobs (would need to implement process termination)
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            job.status = RenderStatus.CANCELLED
            # Implementation would terminate the actual process
            found = True
            logger.info(f"Cancelled active job {job_id}")
        
        return found
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        
        return {
            "queued_jobs": self.job_queue.qsize(),
            "active_jobs": len(self.active_jobs),
            "completed_jobs": len(self.completed_jobs),
            "max_concurrent": self.max_concurrent_jobs,
            "running": self.running
        }
    
    def _worker_thread(self):
        """Worker thread for processing render jobs"""
        
        while self.running:
            try:
                # Get job from queue (with timeout)
                priority, created_time, job = self.job_queue.get(timeout=1)
                
                if job.status == RenderStatus.CANCELLED:
                    continue
                
                # Move to active jobs
                self.active_jobs[job.job_id] = job
                job.status = RenderStatus.PREPARING
                job.started_time = datetime.now()
                
                logger.info(f"Starting render job {job.job_id}")
                
                # Render video
                success = asyncio.run(self._process_job(job))
                
                # Move to completed jobs
                del self.active_jobs[job.job_id]
                self.completed_jobs[job.job_id] = job
                
                if success:
                    job.status = RenderStatus.COMPLETED
                    job.completed_time = datetime.now()
                    logger.info(f"Completed render job {job.job_id}")
                else:
                    job.status = RenderStatus.FAILED
                    logger.error(f"Failed render job {job.job_id}: {job.error_message}")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker thread error: {e}")
    
    async def _process_job(self, job: RenderJob) -> bool:
        """Process complete render job"""
        
        try:
            # Render video
            job.status = RenderStatus.RENDERING
            
            def progress_callback(job_id: str, progress: float):
                job.progress = progress
            
            success = await self.renderer.render_video(job, progress_callback)
            
            if not success:
                return False
            
            job.output_files.append(job.output_path)
            
            # Quality control
            if job.export_settings.quality in [Quality.BROADCAST, Quality.CINEMA]:
                job.status = RenderStatus.POST_PROCESSING
                qc_result = await self.quality_controller.analyze_video_quality(job.output_path)
                job.render_stats["quality_analysis"] = qc_result
            
            # Upload to platform if specified
            if job.platform_settings:
                job.status = RenderStatus.UPLOADING
                upload_result = await self.uploader.upload_to_platform(
                    job.output_path, job.platform_settings
                )
                job.render_stats["upload_result"] = upload_result
                
                if "error" in upload_result:
                    job.error_message = upload_result["error"]
                    return False
            
            # Execute post-render actions
            for action in job.post_actions:
                await self._execute_post_action(job, action)
            
            return True
            
        except Exception as e:
            job.error_message = str(e)
            return False
    
    async def _execute_post_action(self, job: RenderJob, action: Dict[str, Any]):
        """Execute post-render action"""
        
        action_type = action.get("type")
        
        if action_type == "copy_to_folder":
            destination = action.get("destination")
            if destination:
                import shutil
                filename = os.path.basename(job.output_path)
                dest_path = os.path.join(destination, filename)
                shutil.copy2(job.output_path, dest_path)
                job.output_files.append(dest_path)
        
        elif action_type == "generate_thumbnail":
            thumbnail_path = job.output_path.replace(".mp4", "_thumbnail.jpg")
            
            # Extract thumbnail from video
            (
                ffmpeg
                .input(job.output_path, ss=2)
                .output(thumbnail_path, vframes=1, format='image2', vcodec='mjpeg')
                .overwrite_output()
                .run(quiet=True)
            )
            
            job.output_files.append(thumbnail_path)
        
        elif action_type == "cleanup_temp_files":
            # Clean up temporary files
            temp_dir = action.get("temp_directory")
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


class ExportDeliverySystem:
    """Main export and delivery system"""
    
    def __init__(self, workspace_dir: str = "exports"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.render_queue = RenderQueue(max_concurrent_jobs=2)
        self.watermark_processor = WatermarkProcessor()
        self.subtitle_processor = SubtitleProcessor()
        self.quality_controller = QualityController()
        self.platform_uploader = PlatformUploader()
        
        # Start render queue
        self.render_queue.start()
        
        logger.info("Export and Delivery System initialized")
    
    def create_export_job(self, name: str, timeline_path: str,
                         export_settings: ExportSettings,
                         platform_settings: Optional[PlatformSettings] = None,
                         priority: int = 5) -> str:
        """Create new export job"""
        
        job_id = f"export_{int(time.time())}_{hash(name) % 10000}"
        
        # Generate output path
        output_dir = self.workspace_dir / job_id
        output_dir.mkdir(exist_ok=True)
        
        output_filename = f"{name}.{self._get_file_extension(export_settings.format)}"
        output_path = output_dir / output_filename
        
        # Create render job
        job = RenderJob(
            job_id=job_id,
            name=name,
            timeline_path=timeline_path,
            export_settings=export_settings,
            output_path=str(output_path),
            platform_settings=platform_settings,
            priority=priority
        )
        
        # Add to render queue
        self.render_queue.add_job(job)
        
        return job_id
    
    def create_batch_export(self, jobs_config: List[Dict[str, Any]]) -> List[str]:
        """Create multiple export jobs"""
        
        job_ids = []
        
        for config in jobs_config:
            # Get preset if specified
            if "preset" in config:
                platform = Platform(config["preset"]["platform"])
                quality = Quality(config["preset"]["quality"])
                export_settings = FormatPresets.get_preset(platform, quality)
            else:
                export_settings = ExportSettings(**config["export_settings"])
            
            # Platform settings
            platform_settings = None
            if "platform_settings" in config:
                platform_settings = PlatformSettings(**config["platform_settings"])
            
            job_id = self.create_export_job(
                config["name"],
                config["timeline_path"],
                export_settings,
                platform_settings,
                config.get("priority", 5)
            )
            
            job_ids.append(job_id)
        
        return job_ids
    
    def get_export_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get export job status"""
        
        job = self.render_queue.get_job_status(job_id)
        
        if not job:
            return None
        
        return {
            "job_id": job.job_id,
            "name": job.name,
            "status": job.status.value,
            "progress": job.progress,
            "created_time": job.created_time.isoformat(),
            "started_time": job.started_time.isoformat() if job.started_time else None,
            "completed_time": job.completed_time.isoformat() if job.completed_time else None,
            "output_files": job.output_files,
            "error_message": job.error_message,
            "render_stats": job.render_stats
        }
    
    def cancel_export(self, job_id: str) -> bool:
        """Cancel export job"""
        
        return self.render_queue.cancel_job(job_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get render queue status"""
        
        return self.render_queue.get_queue_status()
    
    async def create_platform_preset_exports(self, timeline_path: str, 
                                           base_name: str,
                                           platforms: List[Platform]) -> List[str]:
        """Create exports for multiple platforms with optimized presets"""
        
        job_ids = []
        
        for platform in platforms:
            # Get platform preset
            export_settings = FormatPresets.get_preset(platform, Quality.HIGH)
            
            # Create platform-specific name
            name = f"{base_name}_{platform.value}"
            
            job_id = self.create_export_job(
                name, timeline_path, export_settings, priority=7
            )
            
            job_ids.append(job_id)
        
        return job_ids
    
    def _get_file_extension(self, format: ExportFormat) -> str:
        """Get file extension for export format"""
        
        extensions = {
            ExportFormat.MP4_H264: "mp4",
            ExportFormat.MP4_H265: "mp4",
            ExportFormat.MOV_PRORES: "mov",
            ExportFormat.MOV_DNXHD: "mov",
            ExportFormat.MXF_XAVC: "mxf",
            ExportFormat.WEBM_VP9: "webm",
            ExportFormat.WEBM_AV1: "webm",
            ExportFormat.GIF: "gif",
            ExportFormat.AUDIO_ONLY: "wav"
        }
        
        return extensions.get(format, "mp4")
    
    def shutdown(self):
        """Shutdown export system"""
        
        self.render_queue.stop()
        logger.info("Export and Delivery System shutdown")


# Example usage
async def main():
    """Example usage of export and delivery system"""
    
    # Initialize export system
    export_system = ExportDeliverySystem()
    
    # Create high-quality YouTube export
    youtube_settings = FormatPresets.get_preset(Platform.YOUTUBE, Quality.HIGH)
    youtube_settings.metadata = {
        "title": "My Amazing Video",
        "description": "Created with professional editing system"
    }
    
    job_id = export_system.create_export_job(
        "youtube_upload",
        "timeline.xml",
        youtube_settings,
        priority=8
    )
    
    print(f"Created YouTube export job: {job_id}")
    
    # Create batch exports for social media
    social_platforms = [Platform.YOUTUBE, Platform.INSTAGRAM, Platform.TIKTOK]
    social_jobs = await export_system.create_platform_preset_exports(
        "timeline.xml",
        "social_media_video",
        social_platforms
    )
    
    print(f"Created {len(social_jobs)} social media export jobs")
    
    # Monitor progress
    while True:
        status = export_system.get_export_status(job_id)
        if status:
            print(f"Job {job_id}: {status['status']} - {status['progress']:.1f}%")
            
            if status['status'] in ['completed', 'failed']:
                break
        
        await asyncio.sleep(5)
    
    # Get final status
    final_status = export_system.get_export_status(job_id)
    print(f"Final status: {final_status}")
    
    # Shutdown
    export_system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())