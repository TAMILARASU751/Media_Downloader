import streamlit as st
import os
import yt_dlp
from time import sleep
from pathlib import Path

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

# Function to update progress bar and display status
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes is not None:
            percentage = downloaded_bytes / total_bytes
            st.session_state['progress_bar'].progress(percentage)
            st.session_state['status_text'].text(f"Downloaded {format_size(downloaded_bytes)} of {format_size(total_bytes)}")

# Function to download audio or video with a progress bar
def download_media(url, file_name, download_type, quality):
    temp_save_path = os.path.join(os.getcwd(), f'{file_name}.{"mp3" if download_type == "audio" else "mp4"}')
    ydl_opts = {
        'format': 'bestaudio/best' if download_type == 'audio' else f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': temp_save_path,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        }] if download_type == 'audio' else [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.session_state['status_text'].text("Starting download...")
            ydl.extract_info(url, download=True)
            st.success(f"{download_type.capitalize()} download complete!")

            # Read the file content for browser download
            with open(temp_save_path, 'rb') as file:
                st.download_button(
                    label=f"Download {file_name}",
                    data=file,
                    file_name=os.path.basename(temp_save_path),
                    mime='audio/mpeg' if download_type == 'audio' else 'video/mp4'
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Initialize Streamlit elements for download progress
if 'progress_bar' not in st.session_state:
    st.session_state['progress_bar'] = st.empty()
if 'status_text' not in st.session_state:
    st.session_state['status_text'] = st.empty()

# Streamlit interface
st.title("Media Downloader")

# URL input field
url = st.text_input("Enter the URL of the media:", "")

# File name input
file_name = st.text_input("Enter the custom file name (without extension):", "")

# Download type selection
download_type = st.radio("Select download type:", ('audio', 'video'))

# Quality input based on type
if download_type == 'audio':
    quality = st.selectbox("Select audio quality (kbps):", ["128", "192", "256", "320"])
else:
    quality = st.selectbox("Select video resolution (px):", ["144", "240", "360", "480", "720", "1080", "1440", "2160"])

# Download button
if st.button("Download"):
    # Check if all required fields are filled
    if not url or not file_name:
        st.error("Please fill in all the fields: URL and file name.")
    else:
        # Clear progress bar and status before starting
        st.session_state['progress_bar'].progress(0)
        st.session_state['status_text'].text("")
        
        # Start download with progress and provide a browser download button
        download_media(url, file_name, download_type, quality)
