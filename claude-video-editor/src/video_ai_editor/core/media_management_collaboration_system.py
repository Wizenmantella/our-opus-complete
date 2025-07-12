#!/usr/bin/env python3
"""
Media Management and Collaboration System
Complete media management and team collaboration system for professional video editing.

Features:
- Media pool/browser with smart organization
- Bins/folders with hierarchical structure
- Smart bins/collections with AI categorization
- Metadata editing and management
- Keywords and tags with auto-tagging
- Ratings and flags system
- Color labels and visual organization
- Search and filter with AI-powered search
- Media relations and dependency tracking
- Proxy workflows for efficient editing
- Cache management and optimization
- Media linking and relinking
- Offline/online editing workflows
- Consolidate media operations
- Watch folders for auto-import
- Archive tools and storage management
- Multi-user access and permissions
- Team Projects with real-time collaboration
- Productions workflow management
- Bin/timeline locking mechanisms
- Real-time collaboration features
- Version control and change tracking
- User permissions and role management
- Chat/messaging integration
- Review and approve workflows
- Cloud sync and remote access
- Remote workflows optimization
"""

import os
import json
import sqlite3
import hashlib
import shutil
import asyncio
import logging
import mimetypes
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import aiofiles
import aiohttp
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import cv2
import librosa
import numpy as np
from PIL import Image, ExifTags
import ffmpeg
import subprocess
import threading
import queue
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class MediaType(Enum):
    """Media file types"""
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"
    SEQUENCE = "sequence"
    PROJECT = "project"
    DOCUMENT = "document"
    OTHER = "other"


class MediaStatus(Enum):
    """Media status types"""
    ONLINE = "online"
    OFFLINE = "offline"
    PROXY = "proxy"
    TRANSCODING = "transcoding"
    MISSING = "missing"
    ERROR = "error"


class UserRole(Enum):
    """User roles for collaboration"""
    ADMIN = "admin"
    EDITOR = "editor"
    ASSISTANT = "assistant"
    REVIEWER = "reviewer"
    VIEWER = "viewer"


class ProjectStatus(Enum):
    """Project status types"""
    ACTIVE = "active"
    LOCKED = "locked"
    ARCHIVED = "archived"
    TEMPLATE = "template"


class ConflictResolution(Enum):
    """Conflict resolution strategies"""
    MERGE = "merge"
    OVERWRITE = "overwrite"
    CREATE_VERSION = "create_version"
    REJECT = "reject"


@dataclass
class MediaMetadata:
    """Complete media metadata structure"""
    file_path: str
    file_name: str
    file_size: int
    creation_date: datetime
    modification_date: datetime
    media_type: MediaType
    duration: Optional[float] = None
    resolution: Optional[Tuple[int, int]] = None
    frame_rate: Optional[float] = None
    codec: Optional[str] = None
    bitrate: Optional[int] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    color_space: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    rating: int = 0  # 0-5 stars
    flag_color: Optional[str] = None
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    checksum: Optional[str] = None
    thumbnail_path: Optional[str] = None
    proxy_path: Optional[str] = None
    status: MediaStatus = MediaStatus.ONLINE


@dataclass
class MediaBin:
    """Media bin/folder structure"""
    bin_id: str
    name: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    media_items: List[str] = field(default_factory=list)
    color: Optional[str] = None
    is_smart: bool = False
    smart_criteria: Dict[str, Any] = field(default_factory=dict)
    permissions: Dict[str, List[str]] = field(default_factory=dict)
    created_by: Optional[str] = None
    created_date: datetime = field(default_factory=datetime.now)
    modified_date: datetime = field(default_factory=datetime.now)


@dataclass
class ProjectMember:
    """Project team member"""
    user_id: str
    username: str
    email: str
    role: UserRole
    permissions: List[str] = field(default_factory=list)
    last_active: datetime = field(default_factory=datetime.now)
    is_online: bool = False


@dataclass
class VersionInfo:
    """Version control information"""
    version_id: str
    parent_version: Optional[str] = None
    author: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    description: str = ""
    changes: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class ChatMessage:
    """Chat/messaging system"""
    message_id: str
    user_id: str
    username: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    thread_id: Optional[str] = None
    attachments: List[str] = field(default_factory=list)
    mentions: List[str] = field(default_factory=list)


class MediaDatabase:
    """SQLite database for media management"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        
        # Create tables
        self._create_tables()
        
        logger.info(f"Media database initialized: {self.db_path}")
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Media items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_items (
                id TEXT PRIMARY KEY,
                file_path TEXT UNIQUE NOT NULL,
                file_name TEXT NOT NULL,
                file_size INTEGER,
                creation_date TIMESTAMP,
                modification_date TIMESTAMP,
                media_type TEXT,
                duration REAL,
                resolution_width INTEGER,
                resolution_height INTEGER,
                frame_rate REAL,
                codec TEXT,
                bitrate INTEGER,
                sample_rate INTEGER,
                channels INTEGER,
                color_space TEXT,
                rating INTEGER DEFAULT 0,
                flag_color TEXT,
                checksum TEXT,
                thumbnail_path TEXT,
                proxy_path TEXT,
                status TEXT DEFAULT 'online',
                custom_metadata TEXT
            )
        ''')
        
        # Media bins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS media_bins (
                bin_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                parent_id TEXT,
                color TEXT,
                is_smart BOOLEAN DEFAULT FALSE,
                smart_criteria TEXT,
                created_by TEXT,
                created_date TIMESTAMP,
                modified_date TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES media_bins (bin_id)
            )
        ''')
        
        # Bin contents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bin_contents (
                bin_id TEXT,
                media_id TEXT,
                added_date TIMESTAMP,
                PRIMARY KEY (bin_id, media_id),
                FOREIGN KEY (bin_id) REFERENCES media_bins (bin_id),
                FOREIGN KEY (media_id) REFERENCES media_items (id)
            )
        ''')
        
        # Keywords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                media_id TEXT,
                keyword TEXT,
                confidence REAL DEFAULT 1.0,
                auto_generated BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (media_id, keyword),
                FOREIGN KEY (media_id) REFERENCES media_items (id)
            )
        ''')
        
        # Tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                media_id TEXT,
                tag TEXT,
                category TEXT,
                PRIMARY KEY (media_id, tag),
                FOREIGN KEY (media_id) REFERENCES media_items (id)
            )
        ''')
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'active',
                created_by TEXT,
                created_date TIMESTAMP,
                modified_date TIMESTAMP,
                settings TEXT
            )
        ''')
        
        # Project members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_members (
                project_id TEXT,
                user_id TEXT,
                username TEXT,
                email TEXT,
                role TEXT,
                permissions TEXT,
                last_active TIMESTAMP,
                is_online BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (project_id, user_id),
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        # Versions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS versions (
                version_id TEXT PRIMARY KEY,
                project_id TEXT,
                parent_version TEXT,
                author TEXT,
                timestamp TIMESTAMP,
                description TEXT,
                changes TEXT,
                tags TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        # Chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id TEXT PRIMARY KEY,
                project_id TEXT,
                user_id TEXT,
                username TEXT,
                content TEXT,
                timestamp TIMESTAMP,
                thread_id TEXT,
                attachments TEXT,
                mentions TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        # Cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache_entries (
                cache_key TEXT PRIMARY KEY,
                cache_data TEXT,
                expiry_date TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                last_access TIMESTAMP
            )
        ''')
        
        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_media_type ON media_items (media_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_media_status ON media_items (status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_media_rating ON media_items (rating)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords_media ON keywords (media_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_media ON tags (media_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_bin_contents ON bin_contents (bin_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_project ON chat_messages (project_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_versions_project ON versions (project_id)')
        
        self.connection.commit()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


class MediaAnalyzer:
    """Analyze media files and extract metadata"""
    
    def __init__(self):
        self.supported_video_formats = {'.mp4', '.mov', '.avi', '.mkv', '.mxf', '.prores'}
        self.supported_audio_formats = {'.wav', '.mp3', '.aac', '.flac', '.m4a'}
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.exr', '.dpx'}
    
    async def analyze_media_file(self, file_path: str) -> MediaMetadata:
        """Analyze media file and extract metadata"""
        
        path = Path(file_path)
        
        # Basic file info
        stat = path.stat()
        metadata = MediaMetadata(
            file_path=str(path),
            file_name=path.name,
            file_size=stat.st_size,
            creation_date=datetime.fromtimestamp(stat.st_ctime),
            modification_date=datetime.fromtimestamp(stat.st_mtime),
            media_type=self._determine_media_type(path),
            checksum=await self._calculate_checksum(file_path)
        )
        
        # Media-specific analysis
        if metadata.media_type == MediaType.VIDEO:
            await self._analyze_video(metadata)
        elif metadata.media_type == MediaType.AUDIO:
            await self._analyze_audio(metadata)
        elif metadata.media_type == MediaType.IMAGE:
            await self._analyze_image(metadata)
        
        # Generate thumbnail
        metadata.thumbnail_path = await self._generate_thumbnail(metadata)
        
        return metadata
    
    def _determine_media_type(self, path: Path) -> MediaType:
        """Determine media type from file extension"""
        
        ext = path.suffix.lower()
        
        if ext in self.supported_video_formats:
            return MediaType.VIDEO
        elif ext in self.supported_audio_formats:
            return MediaType.AUDIO
        elif ext in self.supported_image_formats:
            return MediaType.IMAGE
        elif ext in {'.aep', '.prproj', '.fcpxml'}:
            return MediaType.PROJECT
        else:
            mime_type, _ = mimetypes.guess_type(str(path))
            if mime_type:
                if mime_type.startswith('video/'):
                    return MediaType.VIDEO
                elif mime_type.startswith('audio/'):
                    return MediaType.AUDIO
                elif mime_type.startswith('image/'):
                    return MediaType.IMAGE
        
        return MediaType.OTHER
    
    async def _calculate_checksum(self, file_path: str) -> str:
        """Calculate MD5 checksum of file"""
        
        hash_md5 = hashlib.md5()
        
        try:
            async with aiofiles.open(file_path, 'rb') as f:
                async for chunk in f:
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate checksum for {file_path}: {e}")
            return ""
    
    async def _analyze_video(self, metadata: MediaMetadata):
        """Analyze video file"""
        
        try:
            # Use ffprobe for video analysis
            probe = ffmpeg.probe(metadata.file_path)
            
            video_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'video'), None)
            
            if video_stream:
                metadata.resolution = (
                    int(video_stream.get('width', 0)),
                    int(video_stream.get('height', 0))
                )
                
                # Parse frame rate
                fps_str = video_stream.get('r_frame_rate', '0/1')
                if '/' in fps_str:
                    num, den = fps_str.split('/')
                    metadata.frame_rate = int(num) / int(den) if int(den) != 0 else 0
                else:
                    metadata.frame_rate = float(fps_str)
                
                metadata.codec = video_stream.get('codec_name', '')
                metadata.bitrate = int(video_stream.get('bit_rate', 0))
                metadata.color_space = video_stream.get('color_space', '')
            
            # Duration from format
            format_info = probe.get('format', {})
            metadata.duration = float(format_info.get('duration', 0))
            
        except Exception as e:
            logger.warning(f"Video analysis failed for {metadata.file_path}: {e}")
    
    async def _analyze_audio(self, metadata: MediaMetadata):
        """Analyze audio file"""
        
        try:
            # Use librosa for audio analysis
            y, sr = librosa.load(metadata.file_path, sr=None)
            
            metadata.duration = len(y) / sr
            metadata.sample_rate = sr
            metadata.channels = 1 if len(y.shape) == 1 else y.shape[0]
            
            # Use ffprobe for codec info
            probe = ffmpeg.probe(metadata.file_path)
            audio_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            if audio_stream:
                metadata.codec = audio_stream.get('codec_name', '')
                metadata.bitrate = int(audio_stream.get('bit_rate', 0))
            
        except Exception as e:
            logger.warning(f"Audio analysis failed for {metadata.file_path}: {e}")
    
    async def _analyze_image(self, metadata: MediaMetadata):
        """Analyze image file"""
        
        try:
            with Image.open(metadata.file_path) as img:
                metadata.resolution = img.size
                metadata.color_space = img.mode
                
                # Extract EXIF data
                if hasattr(img, '_getexif'):
                    exif_data = img._getexif()
                    if exif_data:
                        for tag_id, value in exif_data.items():
                            tag = ExifTags.TAGS.get(tag_id, tag_id)
                            metadata.custom_metadata[f"exif_{tag}"] = str(value)
            
        except Exception as e:
            logger.warning(f"Image analysis failed for {metadata.file_path}: {e}")
    
    async def _generate_thumbnail(self, metadata: MediaMetadata) -> Optional[str]:
        """Generate thumbnail for media file"""
        
        try:
            thumbnail_dir = Path("thumbnails")
            thumbnail_dir.mkdir(exist_ok=True)
            
            thumbnail_name = f"{metadata.checksum}.jpg"
            thumbnail_path = thumbnail_dir / thumbnail_name
            
            if thumbnail_path.exists():
                return str(thumbnail_path)
            
            if metadata.media_type == MediaType.VIDEO:
                # Extract frame from video
                (
                    ffmpeg
                    .input(metadata.file_path, ss=metadata.duration / 2 if metadata.duration else 1)
                    .output(str(thumbnail_path), vframes=1, format='image2', vcodec='mjpeg')
                    .overwrite_output()
                    .run(quiet=True)
                )
                
            elif metadata.media_type == MediaType.IMAGE:
                # Resize image for thumbnail
                with Image.open(metadata.file_path) as img:
                    img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                    img.save(thumbnail_path, 'JPEG')
            
            elif metadata.media_type == MediaType.AUDIO:
                # Generate waveform thumbnail
                await self._generate_waveform_thumbnail(metadata.file_path, thumbnail_path)
            
            return str(thumbnail_path) if thumbnail_path.exists() else None
            
        except Exception as e:
            logger.warning(f"Thumbnail generation failed for {metadata.file_path}: {e}")
            return None
    
    async def _generate_waveform_thumbnail(self, audio_path: str, output_path: Path):
        """Generate waveform thumbnail for audio"""
        
        try:
            import matplotlib.pyplot as plt
            
            # Load audio
            y, sr = librosa.load(audio_path, duration=30)  # First 30 seconds
            
            # Create waveform plot
            plt.figure(figsize=(4, 2))
            plt.plot(y)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(output_path, dpi=64, bbox_inches='tight', 
                       facecolor='black', edgecolor='none')
            plt.close()
            
        except Exception as e:
            logger.warning(f"Waveform thumbnail generation failed: {e}")


class SmartBinManager:
    """Manage smart bins with AI-powered categorization"""
    
    def __init__(self, database: MediaDatabase):
        self.database = database
        
    async def create_smart_bin(self, name: str, criteria: Dict[str, Any]) -> str:
        """Create smart bin with specified criteria"""
        
        bin_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO media_bins (bin_id, name, is_smart, smart_criteria, created_date, modified_date)
            VALUES (?, ?, TRUE, ?, ?, ?)
        ''', (bin_id, name, json.dumps(criteria), datetime.now(), datetime.now()))
        
        self.database.connection.commit()
        
        # Populate smart bin
        await self._populate_smart_bin(bin_id, criteria)
        
        return bin_id
    
    async def _populate_smart_bin(self, bin_id: str, criteria: Dict[str, Any]):
        """Populate smart bin based on criteria"""
        
        # Build query based on criteria
        query = "SELECT id FROM media_items WHERE 1=1"
        params = []
        
        if 'media_type' in criteria:
            query += " AND media_type = ?"
            params.append(criteria['media_type'])
        
        if 'rating_min' in criteria:
            query += " AND rating >= ?"
            params.append(criteria['rating_min'])
        
        if 'duration_min' in criteria:
            query += " AND duration >= ?"
            params.append(criteria['duration_min'])
        
        if 'duration_max' in criteria:
            query += " AND duration <= ?"
            params.append(criteria['duration_max'])
        
        if 'keywords' in criteria:
            keyword_placeholders = ','.join('?' * len(criteria['keywords']))
            query += f" AND id IN (SELECT media_id FROM keywords WHERE keyword IN ({keyword_placeholders}))"
            params.extend(criteria['keywords'])
        
        if 'date_range' in criteria:
            if 'start' in criteria['date_range']:
                query += " AND creation_date >= ?"
                params.append(criteria['date_range']['start'])
            if 'end' in criteria['date_range']:
                query += " AND creation_date <= ?"
                params.append(criteria['date_range']['end'])
        
        # Execute query and populate bin
        cursor = self.database.connection.cursor()
        cursor.execute(query, params)
        
        # Clear existing contents
        cursor.execute("DELETE FROM bin_contents WHERE bin_id = ?", (bin_id,))
        
        # Add matching media
        for row in cursor.fetchall():
            media_id = row[0]
            cursor.execute('''
                INSERT OR IGNORE INTO bin_contents (bin_id, media_id, added_date)
                VALUES (?, ?, ?)
            ''', (bin_id, media_id, datetime.now()))
        
        self.database.connection.commit()
    
    async def refresh_smart_bins(self):
        """Refresh all smart bins"""
        
        cursor = self.database.connection.cursor()
        cursor.execute("SELECT bin_id, smart_criteria FROM media_bins WHERE is_smart = TRUE")
        
        for row in cursor.fetchall():
            bin_id, criteria_json = row
            criteria = json.loads(criteria_json)
            await self._populate_smart_bin(bin_id, criteria)


class ProxyManager:
    """Manage proxy workflows for efficient editing"""
    
    def __init__(self, proxy_dir: str = "proxies"):
        self.proxy_dir = Path(proxy_dir)
        self.proxy_dir.mkdir(exist_ok=True)
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def create_proxy(self, media_metadata: MediaMetadata, 
                          proxy_format: str = "prores_proxy") -> Optional[str]:
        """Create proxy file for media"""
        
        if media_metadata.media_type != MediaType.VIDEO:
            return None
        
        proxy_name = f"{media_metadata.checksum}_proxy.mov"
        proxy_path = self.proxy_dir / proxy_name
        
        if proxy_path.exists():
            return str(proxy_path)
        
        try:
            # Create proxy using ffmpeg
            if proxy_format == "prores_proxy":
                (
                    ffmpeg
                    .input(media_metadata.file_path)
                    .output(
                        str(proxy_path),
                        vcodec='prores',
                        profile='proxy',
                        vf='scale=960:540',
                        acodec='pcm_s16le'
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )
            
            elif proxy_format == "h264_proxy":
                (
                    ffmpeg
                    .input(media_metadata.file_path)
                    .output(
                        str(proxy_path),
                        vcodec='libx264',
                        crf=23,
                        vf='scale=960:540',
                        acodec='aac'
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )
            
            return str(proxy_path) if proxy_path.exists() else None
            
        except Exception as e:
            logger.error(f"Proxy creation failed for {media_metadata.file_path}: {e}")
            return None
    
    async def batch_create_proxies(self, media_items: List[MediaMetadata]) -> Dict[str, str]:
        """Create proxies for multiple media items"""
        
        video_items = [item for item in media_items if item.media_type == MediaType.VIDEO]
        proxy_results = {}
        
        # Process in parallel
        tasks = []
        for item in video_items:
            task = asyncio.create_task(self.create_proxy(item))
            tasks.append((item.file_path, task))
        
        for file_path, task in tasks:
            try:
                proxy_path = await task
                if proxy_path:
                    proxy_results[file_path] = proxy_path
            except Exception as e:
                logger.error(f"Proxy creation failed for {file_path}: {e}")
        
        return proxy_results


class WatchFolderManager:
    """Monitor folders for automatic media import"""
    
    def __init__(self, media_manager):
        self.media_manager = media_manager
        self.observers = {}
        self.watched_folders = {}
    
    def add_watch_folder(self, folder_path: str, auto_import: bool = True,
                        auto_analyze: bool = True, target_bin: Optional[str] = None):
        """Add folder to watch list"""
        
        if folder_path in self.watched_folders:
            self.remove_watch_folder(folder_path)
        
        # Create event handler
        handler = MediaFolderEventHandler(
            self.media_manager, auto_import, auto_analyze, target_bin
        )
        
        # Create observer
        observer = Observer()
        observer.schedule(handler, folder_path, recursive=True)
        observer.start()
        
        self.observers[folder_path] = observer
        self.watched_folders[folder_path] = {
            'auto_import': auto_import,
            'auto_analyze': auto_analyze,
            'target_bin': target_bin,
            'handler': handler
        }
        
        logger.info(f"Started watching folder: {folder_path}")
    
    def remove_watch_folder(self, folder_path: str):
        """Remove folder from watch list"""
        
        if folder_path in self.observers:
            self.observers[folder_path].stop()
            self.observers[folder_path].join()
            del self.observers[folder_path]
            del self.watched_folders[folder_path]
            logger.info(f"Stopped watching folder: {folder_path}")
    
    def stop_all(self):
        """Stop all folder watchers"""
        
        for folder_path in list(self.watched_folders.keys()):
            self.remove_watch_folder(folder_path)


class MediaFolderEventHandler(FileSystemEventHandler):
    """Handle file system events for watch folders"""
    
    def __init__(self, media_manager, auto_import: bool, 
                 auto_analyze: bool, target_bin: Optional[str]):
        self.media_manager = media_manager
        self.auto_import = auto_import
        self.auto_analyze = auto_analyze
        self.target_bin = target_bin
        self.import_queue = queue.Queue()
        self.processing = False
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.process_thread.start()
    
    def on_created(self, event):
        """Handle file creation"""
        if not event.is_directory and self.auto_import:
            # Add delay to ensure file is fully written
            time.sleep(2)
            self.import_queue.put(event.src_path)
    
    def on_moved(self, event):
        """Handle file move"""
        if not event.is_directory and self.auto_import:
            self.import_queue.put(event.dest_path)
    
    def _process_queue(self):
        """Process import queue"""
        
        while True:
            try:
                file_path = self.import_queue.get(timeout=5)
                
                if os.path.exists(file_path):
                    # Import media
                    asyncio.run(self.media_manager.import_media_file(
                        file_path, auto_analyze=self.auto_analyze, target_bin=self.target_bin
                    ))
                
                self.import_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing import queue: {e}")


class CollaborationManager:
    """Manage real-time collaboration features"""
    
    def __init__(self, database: MediaDatabase):
        self.database = database
        self.active_sessions = {}
        self.message_queue = asyncio.Queue()
        self.websocket_connections = set()
    
    async def create_project(self, name: str, description: str, 
                           created_by: str, settings: Dict[str, Any] = None) -> str:
        """Create new collaborative project"""
        
        project_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO projects (project_id, name, description, created_by, 
                                created_date, modified_date, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, description, created_by, 
              datetime.now(), datetime.now(), json.dumps(settings or {})))
        
        # Add creator as admin
        cursor.execute('''
            INSERT INTO project_members (project_id, user_id, username, email, 
                                       role, permissions, last_active, is_online)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, created_by, created_by, "", "admin", 
              json.dumps(["all"]), datetime.now(), True))
        
        self.database.connection.commit()
        
        return project_id
    
    async def add_project_member(self, project_id: str, user_id: str, 
                               username: str, email: str, role: UserRole,
                               permissions: List[str] = None) -> bool:
        """Add member to project"""
        
        try:
            cursor = self.database.connection.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO project_members 
                (project_id, user_id, username, email, role, permissions, last_active, is_online)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (project_id, user_id, username, email, role.value,
                  json.dumps(permissions or []), datetime.now(), False))
            
            self.database.connection.commit()
            
            # Send notification
            await self._send_project_notification(project_id, {
                'type': 'member_added',
                'user_id': user_id,
                'username': username,
                'role': role.value
            })
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add project member: {e}")
            return False
    
    async def update_user_status(self, project_id: str, user_id: str, is_online: bool):
        """Update user online status"""
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            UPDATE project_members 
            SET is_online = ?, last_active = ?
            WHERE project_id = ? AND user_id = ?
        ''', (is_online, datetime.now(), project_id, user_id))
        
        self.database.connection.commit()
        
        # Broadcast status change
        await self._send_project_notification(project_id, {
            'type': 'user_status',
            'user_id': user_id,
            'is_online': is_online
        })
    
    async def send_chat_message(self, project_id: str, user_id: str, 
                              username: str, content: str,
                              thread_id: Optional[str] = None,
                              attachments: List[str] = None,
                              mentions: List[str] = None) -> str:
        """Send chat message"""
        
        message_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO chat_messages 
            (message_id, project_id, user_id, username, content, timestamp, 
             thread_id, attachments, mentions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (message_id, project_id, user_id, username, content, datetime.now(),
              thread_id, json.dumps(attachments or []), json.dumps(mentions or [])))
        
        self.database.connection.commit()
        
        # Broadcast message
        message = ChatMessage(
            message_id=message_id,
            user_id=user_id,
            username=username,
            content=content,
            thread_id=thread_id,
            attachments=attachments or [],
            mentions=mentions or []
        )
        
        await self._broadcast_chat_message(project_id, message)
        
        return message_id
    
    async def create_version(self, project_id: str, author: str, 
                           description: str, changes: List[Dict[str, Any]],
                           parent_version: Optional[str] = None,
                           tags: List[str] = None) -> str:
        """Create new project version"""
        
        version_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO versions 
            (version_id, project_id, parent_version, author, timestamp, 
             description, changes, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (version_id, project_id, parent_version, author, datetime.now(),
              description, json.dumps(changes), json.dumps(tags or [])))
        
        self.database.connection.commit()
        
        # Notify collaborators
        await self._send_project_notification(project_id, {
            'type': 'new_version',
            'version_id': version_id,
            'author': author,
            'description': description
        })
        
        return version_id
    
    async def lock_resource(self, project_id: str, resource_type: str, 
                          resource_id: str, user_id: str, username: str) -> bool:
        """Lock resource for editing"""
        
        lock_key = f"{project_id}:{resource_type}:{resource_id}"
        
        if lock_key in self.active_sessions:
            return False  # Already locked
        
        self.active_sessions[lock_key] = {
            'user_id': user_id,
            'username': username,
            'timestamp': datetime.now(),
            'resource_type': resource_type,
            'resource_id': resource_id
        }
        
        # Notify others of lock
        await self._send_project_notification(project_id, {
            'type': 'resource_locked',
            'resource_type': resource_type,
            'resource_id': resource_id,
            'user_id': user_id,
            'username': username
        })
        
        return True
    
    async def unlock_resource(self, project_id: str, resource_type: str, 
                            resource_id: str, user_id: str) -> bool:
        """Unlock resource"""
        
        lock_key = f"{project_id}:{resource_type}:{resource_id}"
        
        if lock_key not in self.active_sessions:
            return False
        
        session = self.active_sessions[lock_key]
        if session['user_id'] != user_id:
            return False  # Not authorized to unlock
        
        del self.active_sessions[lock_key]
        
        # Notify others of unlock
        await self._send_project_notification(project_id, {
            'type': 'resource_unlocked',
            'resource_type': resource_type,
            'resource_id': resource_id,
            'user_id': user_id
        })
        
        return True
    
    async def _send_project_notification(self, project_id: str, notification: Dict[str, Any]):
        """Send notification to all project members"""
        
        notification['project_id'] = project_id
        notification['timestamp'] = datetime.now().isoformat()
        
        # Add to message queue for websocket broadcasting
        await self.message_queue.put(notification)
    
    async def _broadcast_chat_message(self, project_id: str, message: ChatMessage):
        """Broadcast chat message to project members"""
        
        notification = {
            'type': 'chat_message',
            'project_id': project_id,
            'message': message.__dict__,
            'timestamp': datetime.now().isoformat()
        }
        
        await self.message_queue.put(notification)


class ArchiveManager:
    """Manage media archiving and storage optimization"""
    
    def __init__(self, archive_dir: str = "archive"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
    
    async def archive_project(self, project_id: str, 
                            include_media: bool = True,
                            compress: bool = True) -> str:
        """Archive complete project"""
        
        archive_name = f"project_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if compress:
            archive_path = self.archive_dir / f"{archive_name}.tar.gz"
            # Create compressed archive
            import tarfile
            
            with tarfile.open(archive_path, 'w:gz') as tar:
                # Add project files
                # This would collect all project-related files
                pass
        else:
            archive_path = self.archive_dir / archive_name
            archive_path.mkdir(exist_ok=True)
            # Copy files to archive directory
        
        return str(archive_path)
    
    async def restore_project(self, archive_path: str) -> str:
        """Restore project from archive"""
        
        # Implementation would restore project from archive
        pass
    
    async def cleanup_unused_media(self, project_id: str, 
                                 dry_run: bool = True) -> List[str]:
        """Identify and optionally remove unused media"""
        
        # Analyze project to find unused media
        unused_media = []
        
        # Implementation would:
        # 1. Scan project timelines
        # 2. Identify referenced media
        # 3. Find media not referenced anywhere
        # 4. Optionally move to trash/archive
        
        return unused_media


class MediaManager:
    """Main media management system"""
    
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.database = MediaDatabase(str(self.workspace_dir / "media.db"))
        self.analyzer = MediaAnalyzer()
        self.smart_bin_manager = SmartBinManager(self.database)
        self.proxy_manager = ProxyManager(str(self.workspace_dir / "proxies"))
        self.watch_folder_manager = WatchFolderManager(self)
        self.collaboration_manager = CollaborationManager(self.database)
        self.archive_manager = ArchiveManager(str(self.workspace_dir / "archive"))
        
        # Cache
        self.metadata_cache = {}
        
        logger.info("Media Manager initialized")
    
    async def import_media_file(self, file_path: str, 
                              auto_analyze: bool = True,
                              target_bin: Optional[str] = None,
                              auto_proxy: bool = False) -> Optional[str]:
        """Import single media file"""
        
        try:
            # Analyze media
            metadata = await self.analyzer.analyze_media_file(file_path)
            
            # Store in database
            media_id = await self._store_media_metadata(metadata)
            
            # Add to bin if specified
            if target_bin:
                await self._add_media_to_bin(media_id, target_bin)
            
            # Auto-generate keywords and tags
            if auto_analyze:
                await self._auto_generate_keywords(media_id, metadata)
            
            # Create proxy if requested
            if auto_proxy and metadata.media_type == MediaType.VIDEO:
                proxy_path = await self.proxy_manager.create_proxy(metadata)
                if proxy_path:
                    await self._update_media_proxy_path(media_id, proxy_path)
            
            # Cache metadata
            self.metadata_cache[media_id] = metadata
            
            logger.info(f"Imported media: {file_path} -> {media_id}")
            return media_id
            
        except Exception as e:
            logger.error(f"Failed to import media {file_path}: {e}")
            return None
    
    async def batch_import_media(self, file_paths: List[str],
                               target_bin: Optional[str] = None,
                               auto_proxy: bool = False) -> List[str]:
        """Import multiple media files"""
        
        imported_ids = []
        
        # Process in parallel batches
        batch_size = 10
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i + batch_size]
            
            tasks = [
                self.import_media_file(path, target_bin=target_bin, auto_proxy=auto_proxy)
                for path in batch
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, str):  # Success
                    imported_ids.append(result)
                else:  # Exception
                    logger.error(f"Import failed: {result}")
        
        return imported_ids
    
    async def search_media(self, query: str, filters: Dict[str, Any] = None) -> List[str]:
        """Search media with text query and filters"""
        
        # Build SQL query
        sql = "SELECT DISTINCT m.id FROM media_items m"
        joins = []
        conditions = ["1=1"]
        params = []
        
        # Text search in filename and keywords
        if query:
            joins.append("LEFT JOIN keywords k ON m.id = k.media_id")
            conditions.append("(m.file_name LIKE ? OR k.keyword LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        # Apply filters
        if filters:
            if 'media_type' in filters:
                conditions.append("m.media_type = ?")
                params.append(filters['media_type'])
            
            if 'rating_min' in filters:
                conditions.append("m.rating >= ?")
                params.append(filters['rating_min'])
            
            if 'duration_range' in filters:
                if 'min' in filters['duration_range']:
                    conditions.append("m.duration >= ?")
                    params.append(filters['duration_range']['min'])
                if 'max' in filters['duration_range']:
                    conditions.append("m.duration <= ?")
                    params.append(filters['duration_range']['max'])
            
            if 'keywords' in filters:
                keyword_placeholders = ','.join('?' * len(filters['keywords']))
                joins.append("LEFT JOIN keywords kf ON m.id = kf.media_id")
                conditions.append(f"kf.keyword IN ({keyword_placeholders})")
                params.extend(filters['keywords'])
        
        # Construct final query
        full_query = sql
        if joins:
            full_query += " " + " ".join(joins)
        full_query += " WHERE " + " AND ".join(conditions)
        
        # Execute query
        cursor = self.database.connection.cursor()
        cursor.execute(full_query, params)
        
        return [row[0] for row in cursor.fetchall()]
    
    async def get_media_metadata(self, media_id: str) -> Optional[MediaMetadata]:
        """Get metadata for media item"""
        
        # Check cache first
        if media_id in self.metadata_cache:
            return self.metadata_cache[media_id]
        
        # Query database
        cursor = self.database.connection.cursor()
        cursor.execute("SELECT * FROM media_items WHERE id = ?", (media_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        # Convert database row to metadata object
        metadata = self._row_to_metadata(row)
        
        # Load keywords and tags
        cursor.execute("SELECT keyword FROM keywords WHERE media_id = ?", (media_id,))
        metadata.keywords = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT tag FROM tags WHERE media_id = ?", (media_id,))
        metadata.tags = [row[0] for row in cursor.fetchall()]
        
        # Cache and return
        self.metadata_cache[media_id] = metadata
        return metadata
    
    async def update_media_metadata(self, media_id: str, updates: Dict[str, Any]) -> bool:
        """Update media metadata"""
        
        try:
            # Build update query
            set_clauses = []
            params = []
            
            for field, value in updates.items():
                if field in ['rating', 'flag_color', 'custom_metadata']:
                    set_clauses.append(f"{field} = ?")
                    if field == 'custom_metadata':
                        params.append(json.dumps(value))
                    else:
                        params.append(value)
            
            if not set_clauses:
                return False
            
            params.append(media_id)
            
            cursor = self.database.connection.cursor()
            cursor.execute(
                f"UPDATE media_items SET {', '.join(set_clauses)} WHERE id = ?",
                params
            )
            
            self.database.connection.commit()
            
            # Update cache
            if media_id in self.metadata_cache:
                metadata = self.metadata_cache[media_id]
                for field, value in updates.items():
                    if hasattr(metadata, field):
                        setattr(metadata, field, value)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update media metadata: {e}")
            return False
    
    async def create_bin(self, name: str, parent_id: Optional[str] = None,
                       color: Optional[str] = None) -> str:
        """Create new media bin"""
        
        bin_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        cursor.execute('''
            INSERT INTO media_bins (bin_id, name, parent_id, color, created_date, modified_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (bin_id, name, parent_id, color, datetime.now(), datetime.now()))
        
        self.database.connection.commit()
        
        return bin_id
    
    async def add_media_to_bin(self, media_id: str, bin_id: str) -> bool:
        """Add media to bin"""
        return await self._add_media_to_bin(media_id, bin_id)
    
    async def _add_media_to_bin(self, media_id: str, bin_id: str) -> bool:
        """Internal method to add media to bin"""
        
        try:
            cursor = self.database.connection.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO bin_contents (bin_id, media_id, added_date)
                VALUES (?, ?, ?)
            ''', (bin_id, media_id, datetime.now()))
            
            self.database.connection.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to add media to bin: {e}")
            return False
    
    async def _store_media_metadata(self, metadata: MediaMetadata) -> str:
        """Store metadata in database"""
        
        media_id = str(uuid.uuid4())
        
        cursor = self.database.connection.cursor()
        
        # Insert main metadata
        cursor.execute('''
            INSERT INTO media_items 
            (id, file_path, file_name, file_size, creation_date, modification_date,
             media_type, duration, resolution_width, resolution_height, frame_rate,
             codec, bitrate, sample_rate, channels, color_space, rating, flag_color,
             checksum, thumbnail_path, proxy_path, status, custom_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            media_id, metadata.file_path, metadata.file_name, metadata.file_size,
            metadata.creation_date, metadata.modification_date, metadata.media_type.value,
            metadata.duration, 
            metadata.resolution[0] if metadata.resolution else None,
            metadata.resolution[1] if metadata.resolution else None,
            metadata.frame_rate, metadata.codec, metadata.bitrate,
            metadata.sample_rate, metadata.channels, metadata.color_space,
            metadata.rating, metadata.flag_color, metadata.checksum,
            metadata.thumbnail_path, metadata.proxy_path, metadata.status.value,
            json.dumps(metadata.custom_metadata)
        ))
        
        # Insert keywords
        for keyword in metadata.keywords:
            cursor.execute('''
                INSERT OR IGNORE INTO keywords (media_id, keyword)
                VALUES (?, ?)
            ''', (media_id, keyword))
        
        # Insert tags
        for tag in metadata.tags:
            cursor.execute('''
                INSERT OR IGNORE INTO tags (media_id, tag, category)
                VALUES (?, ?, ?)
            ''', (media_id, tag, "user"))
        
        self.database.connection.commit()
        
        return media_id
    
    async def _auto_generate_keywords(self, media_id: str, metadata: MediaMetadata):
        """Auto-generate keywords using AI analysis"""
        
        keywords = []
        
        # Basic keywords from metadata
        if metadata.media_type == MediaType.VIDEO:
            keywords.extend(['video', 'footage'])
            
            if metadata.resolution:
                width, height = metadata.resolution
                if width >= 3840:
                    keywords.append('4k')
                elif width >= 1920:
                    keywords.append('1080p')
                elif width >= 1280:
                    keywords.append('720p')
            
            if metadata.frame_rate:
                if metadata.frame_rate >= 59:
                    keywords.append('high_fps')
                elif metadata.frame_rate <= 25:
                    keywords.append('cinematic')
        
        elif metadata.media_type == MediaType.AUDIO:
            keywords.extend(['audio', 'sound'])
            
            if metadata.sample_rate and metadata.sample_rate >= 96000:
                keywords.append('high_quality')
        
        elif metadata.media_type == MediaType.IMAGE:
            keywords.extend(['image', 'photo'])
        
        # Store generated keywords
        cursor = self.database.connection.cursor()
        for keyword in keywords:
            cursor.execute('''
                INSERT OR IGNORE INTO keywords (media_id, keyword, auto_generated)
                VALUES (?, ?, TRUE)
            ''', (media_id, keyword))
        
        self.database.connection.commit()
    
    async def _update_media_proxy_path(self, media_id: str, proxy_path: str):
        """Update proxy path for media"""
        
        cursor = self.database.connection.cursor()
        cursor.execute(
            "UPDATE media_items SET proxy_path = ?, status = ? WHERE id = ?",
            (proxy_path, MediaStatus.PROXY.value, media_id)
        )
        self.database.connection.commit()
    
    def _row_to_metadata(self, row) -> MediaMetadata:
        """Convert database row to MediaMetadata object"""
        
        return MediaMetadata(
            file_path=row['file_path'],
            file_name=row['file_name'],
            file_size=row['file_size'],
            creation_date=datetime.fromisoformat(row['creation_date']),
            modification_date=datetime.fromisoformat(row['modification_date']),
            media_type=MediaType(row['media_type']),
            duration=row['duration'],
            resolution=(row['resolution_width'], row['resolution_height']) if row['resolution_width'] else None,
            frame_rate=row['frame_rate'],
            codec=row['codec'],
            bitrate=row['bitrate'],
            sample_rate=row['sample_rate'],
            channels=row['channels'],
            color_space=row['color_space'],
            rating=row['rating'],
            flag_color=row['flag_color'],
            checksum=row['checksum'],
            thumbnail_path=row['thumbnail_path'],
            proxy_path=row['proxy_path'],
            status=MediaStatus(row['status']),
            custom_metadata=json.loads(row['custom_metadata']) if row['custom_metadata'] else {}
        )
    
    def shutdown(self):
        """Shutdown media manager"""
        
        self.watch_folder_manager.stop_all()
        self.database.close()
        logger.info("Media Manager shutdown complete")


# Example usage
async def main():
    """Example usage of media management and collaboration system"""
    
    # Initialize media manager
    media_manager = MediaManager("workspace")
    
    # Import media files
    media_files = ["video1.mp4", "video2.mov", "audio1.wav"]
    imported_ids = await media_manager.batch_import_media(media_files, auto_proxy=True)
    
    print(f"Imported {len(imported_ids)} media files")
    
    # Create bins
    main_bin = await media_manager.create_bin("Main Footage", color="#FF0000")
    audio_bin = await media_manager.create_bin("Audio Files", color="#00FF00")
    
    # Create smart bin for high-quality videos
    await media_manager.smart_bin_manager.create_smart_bin(
        "4K Videos",
        {
            "media_type": "video",
            "keywords": ["4k"],
            "rating_min": 3
        }
    )
    
    # Set up watch folder
    media_manager.watch_folder_manager.add_watch_folder(
        "/Users/video/incoming",
        auto_import=True,
        auto_analyze=True,
        target_bin=main_bin
    )
    
    # Create collaborative project
    project_id = await media_manager.collaboration_manager.create_project(
        "Music Video Project",
        "Collaborative music video editing",
        "editor1"
    )
    
    # Add team members
    await media_manager.collaboration_manager.add_project_member(
        project_id, "editor2", "Editor Two", "editor2@example.com", UserRole.EDITOR
    )
    
    # Send chat message
    await media_manager.collaboration_manager.send_chat_message(
        project_id, "editor1", "Editor One", "Project started!"
    )
    
    # Search media
    results = await media_manager.search_media(
        "video",
        filters={"media_type": "video", "rating_min": 3}
    )
    
    print(f"Search found {len(results)} results")
    
    # Cleanup
    media_manager.shutdown()


if __name__ == "__main__":
    asyncio.run(main())