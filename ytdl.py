#!/usr/bin/env python3
"""
YouTube Downloader
A script to download YouTube videos as MP3 or MP4 files.
"""

import os
import sys
import argparse
from downloader import YouTubeDownloader
from ui import display_banner, display_progress, clear_screen, display_menu, get_user_input
from utils import validate_url, create_output_dir, sanitize_filename

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download YouTube videos as MP3 or MP4")
    parser.add_argument("-u", "--url", help="YouTube video URL")
    parser.add_argument("-f", "--format", choices=["mp3", "mp4"], help="Download format (mp3 or mp4)")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("-q", "--quality", help="Video quality (for MP4) or audio bitrate (for MP3)")
    parser.add_argument("-b", "--batch", help="File containing list of YouTube URLs")
    args = parser.parse_args()
    return args

def interactive_mode():
    """Run the downloader in interactive mode with a user-friendly menu."""
    clear_screen()
    display_banner()
    
    while True:
        choice = display_menu()
        
        if choice == "1":  # Download single video
            url = get_user_input("Enter YouTube URL: ")
            if not validate_url(url):
                print("\033[91mInvalid YouTube URL! Please try again.\033[0m")
                continue
            
            format_choice = get_user_input("Choose format (mp3/mp4): ").lower()
            if format_choice not in ["mp3", "mp4"]:
                print("\033[91mInvalid format! Please enter mp3 or mp4.\033[0m")
                continue
            
            output_dir = get_user_input("Enter output directory (press Enter for current directory): ")
            if not output_dir:
                output_dir = os.getcwd()
            
            output_dir = create_output_dir(output_dir)
            
            quality = None
            if format_choice == "mp4":
                quality = get_user_input("Choose quality (low/medium/high/best): ").lower()
                if quality not in ["low", "medium", "high", "best"]:
                    quality = "high"
            
            filename = get_user_input("Enter filename (without extension, press Enter for default): ")
            
            downloader = YouTubeDownloader(url, format_choice, output_dir, quality, filename)
            downloader.download()
        
        elif choice == "2":  # Batch download
            batch_file = get_user_input("Enter path to file containing URLs: ")
            if not os.path.exists(batch_file):
                print("\033[91mFile not found! Please check the path and try again.\033[0m")
                continue
            
            format_choice = get_user_input("Choose format (mp3/mp4): ").lower()
            if format_choice not in ["mp3", "mp4"]:
                print("\033[91mInvalid format! Please enter mp3 or mp4.\033[0m")
                continue
            
            output_dir = get_user_input("Enter output directory (press Enter for current directory): ")
            if not output_dir:
                output_dir = os.getcwd()
            
            output_dir = create_output_dir(output_dir)
            
            quality = None
            if format_choice == "mp4":
                quality = get_user_input("Choose quality (low/medium/high/best): ").lower()
                if quality not in ["low", "medium", "high", "best"]:
                    quality = "high"
            
            try:
                with open(batch_file, 'r') as f:
                    urls = [line.strip() for line in f if line.strip() and validate_url(line.strip())]
                
                if not urls:
                    print("\033[91mNo valid URLs found in the file!\033[0m")
                    continue
                
                print(f"\033[92mFound {len(urls)} valid URLs. Starting download...\033[0m")
                
                for i, url in enumerate(urls):
                    print(f"\n\033[94m[{i+1}/{len(urls)}] Processing: {url}\033[0m")
                    downloader = YouTubeDownloader(url, format_choice, output_dir, quality)
                    downloader.download()
            
            except Exception as e:
                print(f"\033[91mError processing batch file: {str(e)}\033[0m")
        
        elif choice == "3":  # Exit
            print("\n\033[92mThank you for using YouTube Downloader. Goodbye!\033[0m")
            sys.exit(0)
        
        input("\n\033[94mPress Enter to continue...\033[0m")
        clear_screen()
        display_banner()

def main():
    """Main function to run the script."""
    args = parse_args()
    
    # If command line arguments are provided, use them
    if args.url or args.batch:
        # Process batch file if provided
        if args.batch:
            if not os.path.exists(args.batch):
                print(f"\033[91mBatch file not found: {args.batch}\033[0m")
                sys.exit(1)
            
            output_dir = args.output if args.output else os.getcwd()
            output_dir = create_output_dir(output_dir)
            
            try:
                with open(args.batch, 'r') as f:
                    urls = [line.strip() for line in f if line.strip() and validate_url(line.strip())]
                
                if not urls:
                    print("\033[91mNo valid URLs found in the batch file!\033[0m")
                    sys.exit(1)
                
                print(f"\033[92mFound {len(urls)} valid URLs. Starting download...\033[0m")
                
                for i, url in enumerate(urls):
                    print(f"\n\033[94m[{i+1}/{len(urls)}] Processing: {url}\033[0m")
                    downloader = YouTubeDownloader(
                        url, 
                        args.format or "mp4", 
                        output_dir, 
                        args.quality
                    )
                    downloader.download()
            
            except Exception as e:
                print(f"\033[91mError processing batch file: {str(e)}\033[0m")
                sys.exit(1)
        
        # Process single URL
        elif args.url:
            if not validate_url(args.url):
                print("\033[91mInvalid YouTube URL!\033[0m")
                sys.exit(1)
            
            output_dir = args.output if args.output else os.getcwd()
            output_dir = create_output_dir(output_dir)
            
            downloader = YouTubeDownloader(
                args.url, 
                args.format or "mp4", 
                output_dir, 
                args.quality
            )
            downloader.download()
    
    # If no arguments provided, start interactive mode
    else:
        interactive_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[92mDownload canceled. Exiting...\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[91mAn unexpected error occurred: {str(e)}\033[0m")
        sys.exit(1)