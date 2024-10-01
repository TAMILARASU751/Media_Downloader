import streamlit as st
import os
import yt_dlp
import tempfile

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

# Function to download audio or video
def download_media(url, download_type, quality):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Use temporary directory as save path
        file_name = "downloaded_file.mp3" if download_type == 'audio' else "downloaded_file.mp4"
        save_path = os.path.join(temp_dir, file_name)
        
        ydl_opts = {
            'format': 'bestaudio/best' if download_type == 'audio' else f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': save_path,
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
                
                # Provide file for download
                with open(save_path, "rb") as file:
                    st.download_button(
                        label="Download your file",
                        data=file,
                        file_name=file_name,
                        mime="audio/mp3" if download_type == 'audio' else "video/mp4"
                    )
                st.success("Download complete! You can download the file using the button above.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Function to handle download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes is not None:
            percentage = downloaded_bytes / total_bytes
            st.session_state['progress_bar'].progress(percentage)
            st.session_state['status_text'].text(f"Downloaded {format_size(downloaded_bytes)} of {format_size(total_bytes)}")

# Streamlit interface
st.title("Media Downloader")

# Initialize download progress elements
if 'progress_bar' not in st.session_state:
    st.session_state['progress_bar'] = st.empty()
if 'status_text' not in st.session_state:
    st.session_state['status_text'] = st.empty()

# URL input field
url = st.text_input("Enter the URL of the media:", "")

# Download type selection
download_type = st.radio("Select download type:", ('audio', 'video'))

# Quality input based on type
quality = st.selectbox("Select quality:", ["128", "192", "256", "320"]) if download_type == 'audio' else st.selectbox(
    "Select resolution:", ["144", "240", "360", "480", "720", "1080", "1440", "2160"]
)

# Download button
if st.button("Download"):
    if not url:
        st.error("Please enter a URL.")
    else:
        # Clear previous progress and status
        st.session_state['progress_bar'].progress(0)
        st.session_state['status_text'].text("")

        # Start download
        download_media(url, download_type, quality)
