import tkinter as tk
from tkinter import messagebox, filedialog
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
            info_dict = ydl.extract_info(url, download=True)
            file_path = f"{save_path}/{file_name}.mp3"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                messagebox.showinfo("Success", f"Audio download complete! File size: {format_size(file_size)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to download video
def download_video(url, save_path, file_name, video_resolution):
    ydl_opts = {
        'format': f'bestvideo[height<={video_resolution}]+bestaudio/best',
        'outtmpl': f'{save_path}/{file_name}.mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = f"{save_path}/{file_name}.mp4"
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                messagebox.showinfo("Success", f"Video download complete! File size: {format_size(file_size)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to start the download process
def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    save_path = filedialog.askdirectory()
    if not save_path:
        messagebox.showerror("Error", "Please select a save directory.")
        return

    # Ask for custom file name
    file_name = file_name_entry.get().strip()
    if not file_name:
        messagebox.showerror("Error", "Please enter a custom file name.")
        return

    download_type = download_type_var.get()

    if download_type == 'audio':
        quality = audio_quality_var.get()
        download_audio(url, save_path, file_name, quality)
    elif download_type == 'video':
        resolution = video_resolution_var.get()
        download_video(url, save_path, file_name, resolution)
    else:
        messagebox.showerror("Error", "Invalid download type selected.")

# GUI setup
root = tk.Tk()
root.title("Media Downloader")

tk.Label(root, text="Enter the URL of the video:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter the custom file name:").grid(row=1, column=0, padx=10, pady=10)
file_name_entry = tk.Entry(root, width=50)
file_name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Select download type:").grid(row=2, column=0, padx=10, pady=10)
download_type_var = tk.StringVar(value="audio")
tk.Radiobutton(root, text="Audio", variable=download_type_var, value="audio").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Video", variable=download_type_var, value="video").grid(row=2, column=1, sticky="e")

# Audio quality options
tk.Label(root, text="Select audio quality (kbps):").grid(row=3, column=0, padx=10, pady=10)
audio_quality_var = tk.StringVar(value="192")
audio_quality_menu = tk.OptionMenu(root, audio_quality_var, "128", "192", "256", "320")
audio_quality_menu.grid(row=3, column=1, padx=10, pady=10)

# Video resolution options
tk.Label(root, text="Select video resolution (px):").grid(row=4, column=0, padx=10, pady=10)
video_resolution_var = tk.StringVar(value="720")
video_resolution_menu = tk.OptionMenu(root, video_resolution_var, "144", "240", "360", "480", "720", "1080", "1440", "2160")
video_resolution_menu.grid(row=4, column=1, padx=10, pady=10)

download_button = tk.Button(root, text="Download", command=start_download)
download_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()