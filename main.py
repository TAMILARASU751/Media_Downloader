import streamlit as st
import os
import yt_dlp
import tempfile

# Function to handle download progress
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes:
            percentage = downloaded_bytes / total_bytes
            st.session_state['progress_bar'].progress(percentage)
            st.session_state['status_text'].text(f"Downloaded {downloaded_bytes / 1024:.2f} KB of {total_bytes / 1024:.2f} KB")

# Function to download audio or video
def download_media(url, file_name, download_type, quality):
    # Use temporary directory for downloads
    with tempfile.TemporaryDirectory() as temp_dir:
        file_extension = "mp3" if download_type == 'audio' else "mp4"
        file_path = os.path.join(temp_dir, f"{file_name}.{file_extension}")
        
        # YDL Options
        ydl_opts = {
            'format': 'bestaudio/best' if download_type == 'audio' else f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': file_path,
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }] if download_type == 'audio' else [],
        }

        # Download the file
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                st.session_state['status_text'].text("Starting download...")
                ydl.extract_info(url, download=True)

                # Show download button after download is complete
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="Download your file",
                        data=file,
                        file_name=f"{file_name}.{file_extension}",
                        mime="audio/mp3" if download_type == 'audio' else "video/mp4"
                    )
                st.success(f"Download complete! File saved in temporary storage.")
                st.info(f"Temporary storage path: {file_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Streamlit UI Elements
st.title("Media Downloader")

# Initialize session state variables
if 'progress_bar' not in st.session_state:
    st.session_state['progress_bar'] = st.empty()
if 'status_text' not in st.session_state:
    st.session_state['status_text'] = st.empty()

# Input fields
url = st.text_input("Enter the URL of the media:", "")
file_name = st.text_input("Enter the custom file name (without extension):", "")
download_type = st.radio("Select download type:", ('audio', 'video'))

# Quality input based on type
if download_type == 'audio':
    quality = st.selectbox("Select audio quality (kbps):", ["128", "192", "256", "320"])
else:
    quality = st.selectbox("Select video resolution (px):", ["144", "240", "360", "480", "720", "1080", "1440", "2160"])

# Download button
if st.button("Download"):
    if not url or not file_name:
        st.error("Please fill in all the fields: URL and file name.")
    else:
        # Clear progress bar and status before starting
        st.session_state['progress_bar'].progress(0)
        st.session_state['status_text'].text("")

        # Start download
        download_media(url, file_name, download_type, quality)

