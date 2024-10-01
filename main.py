import streamlit as st
import os
import yt_dlp
import tempfile

# Function to handle download progress (you can customize this for better visuals)
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes is not None:
            percentage = downloaded_bytes / total_bytes
            st.session_state['progress_bar'].progress(percentage)
            st.session_state['status_text'].text(f"Downloaded {downloaded_bytes / 1024:.2f} KB of {total_bytes / 1024:.2f} KB")

# Function to download audio or video
def download_media(url, file_name, download_type, quality):
    # Use the temporary directory for downloads
    with tempfile.TemporaryDirectory() as save_path:
        # Determine file name and extension based on type
        file_extension = "mp3" if download_type == 'audio' else "mp4"
        save_file = os.path.join(save_path, f"{file_name}.{file_extension}")

        ydl_opts = {
            'format': 'bestaudio/best' if download_type == 'audio' else f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': save_file,
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }] if download_type == 'audio' else [],
        }

        try:
            # Start downloading the media using yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.session_state['status_text'].text("Starting download...")
                ydl.extract_info(url, download=True)

                # Show success message and provide the download button
                st.success(f"{download_type.capitalize()} download complete! Click the button below to download your file.")
                
                # Provide file for user download using st.download_button
                with open(save_file, "rb") as file:
                    st.download_button(
                        label="Download your file",
                        data=file,
                        file_name=f"{file_name}.{file_extension}",
                        mime="audio/mp3" if download_type == 'audio' else "video/mp4"
                    )

                # Show the temporary path for user's reference
                st.info(f"File is temporarily stored at: {save_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Streamlit interface
st.title("Media Downloader")

# Initialize download progress elements
if 'progress_bar' not in st.session_state:
    st.session_state['progress_bar'] = st.empty()
if 'status_text' not in st.session_state:
    st.session_state['status_text'] = st.empty()

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
