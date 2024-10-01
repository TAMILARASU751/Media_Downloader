import streamlit as st
import os
import yt_dlp
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import warnings

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
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality,
        }],
        'outtmpl': f'{save_path}/{file_name}.mp3',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            file_path = f"{save_path}/{file_name}.mp3"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                st.success(f"Audio download complete! File size: {format_size(file_size)}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Function to download video
def download_video(url, save_path, file_name, video_resolution):
    ydl_opts = {
        'format': f'bestvideo[height<={video_resolution}]+bestaudio/best',
        'outtmpl': f'{save_path}/{file_name}.mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            file_path = f"{save_path}/{file_name}.mp4"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                st.success(f"Video download complete! File size: {format_size(file_size)}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Streamlit UI Setup
st.title("Media Downloader")

url = st.text_input("Enter the URL of the video:")

file_name = st.text_input("Enter the custom file name:")

download_type = st.radio("Select download type:", ('audio', 'video'))

if download_type == 'audio':
    quality = st.selectbox("Select audio quality (kbps):", options=["128", "192", "256", "320"])
else:
    resolution = st.selectbox("Select video resolution (px):", options=["144", "240", "360", "480", "720", "1080", "1440", "2160"])

# Directory picker: use current working directory as default
save_path = st.text_input("Enter the save directory path:", value=os.getcwd())

if st.button("Download"):
    if not url:
        st.error("Please enter a URL.")
    elif not save_path.strip():  # Check if path is empty or whitespace
        st.error("Please enter a save directory path.")
    elif not os.path.exists(save_path):  # Check if the path exists
        try:
            os.makedirs(save_path)  # Create the directory if it doesn't exist
            st.warning(f"Directory did not exist. Created new directory at: {save_path}")
        except Exception as e:
            st.error(f"Could not create directory: {e}")
    elif not file_name.strip():
        st.error("Please enter a custom file name.")
    else:
        if download_type == 'audio':
            download_audio(url, save_path, file_name, quality)
        elif download_type == 'video':
            download_video(url, save_path, file_name, resolution)
