"""
YouTube Downloader core functionality module.
Handles the actual downloading of videos using pytube.
"""

import os
import shutil
import subprocess
from pytube import YouTube
from pytube.exceptions import PytubeError
from ui import display_progress
from utils import sanitize_filename

class YouTubeDownloader:
    """Class to handle YouTube video downloads."""
    
    def __init__(self, url, format_type="mp4", output_dir="./downloads", quality=None, filename=None):
        """
        Initialize the downloader.
        
        Args:
            url (str): YouTube video URL
            format_type (str): 'mp3' or 'mp4'
            output_dir (str): Directory to save the downloads
            quality (str): Video quality or audio bitrate
            filename (str): Custom filename for the download
        """
        self.url = url
        self.format_type = format_type.lower()
        self.output_dir = output_dir
        self.quality = quality
        self.custom_filename = filename
        
        # Initialize YouTube object
        self.yt = None
        
        # Quality settings
        self.quality_settings = {
            "mp4": {
                "low": "360p",
                "medium": "720p",
                "high": "1080p",
                "best": None  # Will select highest available
            },
            "mp3": {
                "low": "128kbps",
                "medium": "192kbps",
                "high": "256kbps",
                "best": "320kbps"
            }
        }
    
    def _initialize_youtube(self):
        """Initialize the YouTube object with progress callback."""
        try:
            self.yt = YouTube(
                self.url,
                on_progress_callback=display_progress,
                on_complete_callback=lambda stream, file_path: print(f"\n\033[92mDownload completed: {file_path}\033[0m")
            )
            return True
        except PytubeError as e:
            print(f"\033[91mError initializing YouTube: {str(e)}\033[0m")
            return False
    
    def _get_safe_filename(self):
        """Get a safe filename for the download."""
        if self.custom_filename:
            return sanitize_filename(self.custom_filename)
        
        # Get title from YouTube and sanitize it
        video_title = sanitize_filename(self.yt.title)
        return video_title
    
    def _download_mp4(self):
        """Download the video in MP4 format."""
        try:
            # Determine resolution based on quality
            resolution = None
            if self.quality and self.quality in self.quality_settings["mp4"]:
                resolution = self.quality_settings["mp4"][self.quality]
            
            # If resolution is specified, try to get that specific stream
            if resolution:
                stream = self.yt.streams.filter(
                    progressive=True,
                    file_extension="mp4",
                    resolution=resolution
                ).first()
            else:
                # Otherwise get the highest resolution
                stream = self.yt.streams.filter(
                    progressive=True,
                    file_extension="mp4"
                ).order_by('resolution').desc().first()
            
            if not stream:
                print(f"\033[93mCould not find {resolution} stream, downloading best available...\033[0m")
                stream = self.yt.streams.filter(
                    progressive=True,
                    file_extension="mp4"
                ).order_by('resolution').desc().first()
            
            if not stream:
                raise PytubeError("No suitable video stream found")
            
            # Get filename
            filename = self._get_safe_filename()
            
            # Download the video
            output_path = stream.download(
                output_path=self.output_dir,
                filename=f"{filename}.mp4"
            )
            
            return output_path
        
        except PytubeError as e:
            print(f"\033[91mError downloading MP4: {str(e)}\033[0m")
            return None
    
    def _download_mp3(self):
        """Download the video as MP3 (audio only)."""
        try:
            # Get the audio stream
            stream = self.yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            
            if not stream:
                raise PytubeError("No suitable audio stream found")
            
            # Get filename
            filename = self._get_safe_filename()
            temp_file = os.path.join(self.output_dir, f"{filename}.{stream.subtype}")
            
            # Download the audio stream
            stream.download(
                output_path=self.output_dir,
                filename=f"{filename}.{stream.subtype}"
            )
            
            # Convert to MP3 using FFmpeg if available
            mp3_file = os.path.join(self.output_dir, f"{filename}.mp3")
            
            # First try using FFmpeg
            try:
                bitrate = "256k"  # Default bitrate
                if self.quality and self.quality in self.quality_settings["mp3"]:
                    bitrate_value = self.quality_settings["mp3"][self.quality].replace("kbps", "k")
                    bitrate = bitrate_value
                
                subprocess.run(
                    ["ffmpeg", "-i", temp_file, "-b:a", bitrate, "-vn", mp3_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                
                # Remove the temporary file
                os.remove(temp_file)
                
                return mp3_file
            
            except (subprocess.SubprocessError, FileNotFoundError):
                # If FFmpeg is not available or fails, just rename the file
                print("\033[93mFFmpeg not found or failed. Converting by renaming file extension.\033[0m")
                print("\033[93mNote: For better quality conversions, install FFmpeg.\033[0m")
                
                shutil.move(temp_file, mp3_file)
                return mp3_file
        
        except PytubeError as e:
            print(f"\033[91mError downloading MP3: {str(e)}\033[0m")
            return None
    
    def download(self):
        """Download the video in the specified format."""
        print(f"\n\033[94mInitializing download from: {self.url}\033[0m")
        
        if not self._initialize_youtube():
            return False
        
        print(f"\033[94mVideo Title: {self.yt.title}\033[0m")
        print(f"\033[94mAuthor: {self.yt.author}\033[0m")
        print(f"\033[94mLength: {self.yt.length} seconds\033[0m")
        print(f"\033[94mFormat: {self.format_type.upper()}\033[0m")
        
        try:
            if self.format_type == "mp4":
                output_file = self._download_mp4()
            elif self.format_type == "mp3":
                output_file = self._download_mp3()
            else:
                print(f"\033[91mUnsupported format: {self.format_type}\033[0m")
                return False
            
            if output_file:
                file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
                print(f"\033[92mDownload successful! File saved to: {output_file} ({file_size:.2f} MB)\033[0m")
                return True
            return False
        
        except Exception as e:
            print(f"\033[91mError during download: {str(e)}\033[0m")
            return False