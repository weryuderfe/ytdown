"""
Utility functions for the YouTube Downloader.
"""

import os
import re
import string

def validate_url(url):
    """Validate a YouTube URL."""
    # Basic URL validation for YouTube
    youtube_regex = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    return bool(re.match(youtube_regex, url))

def create_output_dir(output_dir):
    """Create the output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"\033[92mCreated output directory: {output_dir}\033[0m")
        except OSError as e:
            print(f"\033[91mError creating directory {output_dir}: {str(e)}\033[0m")
            # Fall back to current directory
            output_dir = os.getcwd()
            print(f"\033[93mFalling back to current directory: {output_dir}\033[0m")
    return output_dir

def sanitize_filename(filename):
    """Sanitize a filename by removing invalid characters."""
    # Replace problematic characters
    invalid_chars = '<>:"/\\|?*'
    
    # First, convert to ASCII and remove invalid characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in filename if c in valid_chars)
    
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    
    # Remove duplicate underscores
    while '__' in sanitized:
        sanitized = sanitized.replace('__', '_')
    
    # Trim to reasonable length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    # Ensure the filename is not empty
    if not sanitized:
        sanitized = "youtube_download"
    
    return sanitized

def get_human_readable_size(size_bytes):
    """Convert size in bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.2f} MB"
    else:
        return f"{size_bytes/(1024**3):.2f} GB"

def is_ffmpeg_available():
    """Check if FFmpeg is installed on the system."""
    try:
        import subprocess
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def suggest_installation():
    """Suggest installation methods for missing dependencies."""
    print("\n\033[93mSome dependencies are missing. Here's how to install them:\033[0m")
    
    # Suggest pytube installation
    print("\n\033[96mInstall pytube:\033[0m")
    print("\033[97mpip install pytube\033[0m")
    
    # Suggest FFmpeg installation
    print("\n\033[96mInstall FFmpeg:\033[0m")
    print("\033[97m- Windows: Download from https://ffmpeg.org/download.html\033[0m")
    print("\033[97m- macOS: brew install ffmpeg\033[0m")
    print("\033[97m- Ubuntu/Debian: sudo apt install ffmpeg\033[0m")
    print("\033[97m- Fedora: sudo dnf install ffmpeg\033[0m")