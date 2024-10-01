import streamlit as st
import yt_dlp
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Function to format file size
def format_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"

# Function to download audio
def download_audio(url, save_path, file_name, audio_quality):
    ydl_opts = {
        'format': f'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': audio_quality}],
        'outtmpl': os.path.join(save_path, f'{file_name}.mp3'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(save_path, f'{file_name}.mp3')
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                st.success(f"Audio download complete! File size: {format_size(file_size)}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to download video
def download_video(url, save_path, file_name, video_resolution):
    ydl_opts = {
        'format': f'bestvideo[height<={video_resolution}]+bestaudio/best',
        'outtmpl': os.path.join(save_path, f'{file_name}.mp4'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(save_path, f'{file_name}.mp4')
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                st.success(f"Video download complete! File size: {format_size(file_size)}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit GUI setup
st.title("Media Downloader")

# URL input field
url = st.text_input("Enter the URL of the video:", "")

# Directory selection
save_path = st.text_input("Enter the path to save the file (e.g., C:\\Downloads):", "")

# Custom file name input
file_name = st.text_input("Enter the custom file name (without extension):", "")

# Select download type (Audio/Video)
download_type = st.radio("Select download type:", ('audio', 'video'))

# Audio quality options (Only shown if 'audio' is selected)
if download_type == 'audio':
    audio_quality = st.selectbox("Select audio quality (kbps):", ["128", "192", "256", "320"])

# Video resolution options (Only shown if 'video' is selected)
if download_type == 'video':
    video_resolution = st.selectbox("Select video resolution (px):", ["144", "240", "360", "480", "720", "1080", "1440", "2160"])

# Download button
if st.button("Download"):
    if not url or not save_path or not file_name:
        st.error("Please fill in all the fields: URL, save path, and file name.")
    else:
        if not os.path.exists(save_path):
            st.error(f"The directory '{save_path}' does not exist. Please enter a valid path.")
        else:
            if download_type == 'audio':
                download_audio(url, save_path, file_name, audio_quality)
            elif download_type == 'video':
                download_video(url, save_path, file_name, video_resolution)
