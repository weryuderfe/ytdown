# YouTube Downloader

A Python script to download YouTube videos as MP3 or MP4 files.

## Features

- Download YouTube videos as MP4 files (video)
- Convert YouTube videos to MP3 files (audio)
- Custom file naming and destination folder selection
- Progress tracking during download
- Input validation and error handling
- Support for various video qualities
- History of downloaded videos
- Batch download support (multiple URLs)

## Installation

1. Clone this repository or download the files.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For MP3 conversion, install FFmpeg (optional but recommended):
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - Fedora: `sudo dnf install ffmpeg`

## Usage

### Interactive Mode

Run the script without arguments to use the interactive mode:

```bash
python ytdl.py
```

Follow the on-screen prompts to download videos.

### Command Line Mode

You can also use command line arguments:

```bash
python ytdl.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -f mp4 -o "/path/to/save" -q high
```

#### Available Arguments

- `-u, --url`: YouTube video URL
- `-f, --format`: Download format (mp3 or mp4)
- `-o, --output`: Output directory
- `-q, --quality`: Video quality (for MP4) or audio bitrate (for MP3)
- `-b, --batch`: File containing list of YouTube URLs

### Batch Download

Create a text file with one YouTube URL per line, then use:

```bash
python ytdl.py -b urls.txt -f mp3 -o "/path/to/save"
```

## Quality Options

### MP4 Quality

- `low`: 360p
- `medium`: 720p
- `high`: 1080p
- `best`: Highest available

### MP3 Quality

- `low`: 128kbps
- `medium`: 192kbps
- `high`: 256kbps
- `best`: 320kbps

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for personal use only. Please respect copyright laws and YouTube's Terms of Service when downloading videos.