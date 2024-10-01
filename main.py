import streamlit as st
import os
import yt_dlp
import tempfile

# Function to download audio or video with a progress bar
def download_media(url, file_name, download_type, quality):
    # Use the temporary directory for downloads to avoid path issues
    with tempfile.TemporaryDirectory() as save_path:
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
                
                # Show success message and provide the download path
                st.success(f"{download_type.capitalize()} download complete! Saved at {save_path}.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Sample Streamlit interface for testing
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

        # Start download with progress
        download_media(url, file_name, download_type, quality)
