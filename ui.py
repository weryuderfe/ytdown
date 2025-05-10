"""
User interface module for the YouTube Downloader.
Contains functions to handle UI elements, display progress, and get user input.
"""

import os
import sys
import shutil

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display the application banner."""
    terminal_width = shutil.get_terminal_size().columns
    banner = """
 __   __         _____      _          ____                      _                 _           
 \\ \\ / /__  _   |_   _|   _| |__   ___|  _ \\  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
  \\ V / _ \\| | | || || | | | '_ \\ / _ \\ | | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__|
   | | (_) | |_| || || |_| | |_) |  __/ |_| | (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |   
   |_|\\___/ \\__,_||_| \\__,_|_.__/ \\___|____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|   
                                                                                                
    """
    lines = banner.strip().split('\n')
    centered_banner = '\n'.join(line.center(terminal_width) for line in lines)
    print(f"\033[95m{centered_banner}\033[0m")
    print("\033[94m" + "=" * terminal_width + "\033[0m")
    print(f"\033[96m{'Download YouTube Videos as MP3/MP4'.center(terminal_width)}\033[0m")
    print("\033[94m" + "=" * terminal_width + "\033[0m\n")

def display_menu():
    """Display the main menu and return the user's choice."""
    print("\n\033[96mMAIN MENU\033[0m")
    print("\033[97m1. Download Single Video\033[0m")
    print("\033[97m2. Batch Download (from file)\033[0m")
    print("\033[97m3. Exit\033[0m\n")
    return get_user_input("Enter your choice (1-3): ")

def get_user_input(prompt):
    """Get input from the user with a formatted prompt."""
    return input(f"\033[93m{prompt}\033[0m")

def display_progress(stream, chunk, bytes_remaining):
    """Display download progress."""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    
    # Calculate progress bar width based on terminal size
    terminal_width = shutil.get_terminal_size().columns
    bar_width = min(50, terminal_width - 30)  # Ensure it fits in terminal
    
    # Create the progress bar
    filled_width = int(percentage / 100 * bar_width)
    bar = '█' * filled_width + '░' * (bar_width - filled_width)
    
    # Calculate download speed and ETA (simplified)
    # This is a placeholder - actual implementation would track time
    
    # Display progress
    sys.stdout.write(f"\r\033[97mDownloading: [{bar}] {percentage:.1f}% ({bytes_downloaded/1048576:.1f}/{total_size/1048576:.1f} MB)")
    sys.stdout.flush()