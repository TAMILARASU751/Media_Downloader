import streamlit as st
import os
import yt_dlp

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
def download_media(url, save_path, file_name, download_type, quality):
    # Ensure the directory exists, create it if it does not
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        'format': 'bestaudio/best' if download_type == 'audio' else f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': os.path.join(save_path, f'{file_name}.{"mp3" if download_type == "audio" else "mp4"}'),
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
            st.success(f"{download_type.capitalize()} download complete! Saved at {save_path}.")
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

# Directory selection input - set default to a downloads folder in user's home directory
default_path = os.path.join(os.path.expanduser("~"), "downloads")
save_path = st.text_input("Enter the directory path to save the file:", default_path)

# Create the directory if it doesn't exist
if not os.path.exists(save_path):
    os.makedirs(save_path)

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
    if not url or not save_path or not file_name:
        st.error("Please fill in all the fields: URL, save path, and file name.")
    else:
        # Clear progress bar and status before starting
        st.session_state['progress_bar'].progress(0)
        st.session_state['status_text'].text("")
        
        # Start download with progress
        download_media(url, save_path, file_name, download_type, quality)
