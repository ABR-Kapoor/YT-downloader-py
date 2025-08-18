import streamlit as st
import yt_dlp
import os
from pydub import AudioSegment

# Title
st.title("YouTube Downloader")

# Step 1: Get YouTube link
url = st.text_input("Enter YouTube video URL:")

if url:
    try:
        st.success(f"URL: {url}")
        download_type = st.radio("Download type:", ["Video", "Audio"])
        if download_type == "Video":
            quality = st.selectbox("Select video quality:", ["best", "1080p", "720p", "480p", "360p"])
            extension = st.selectbox("Select extension:", ["mp4", "webm"])
        else:
            quality = st.selectbox("Select audio quality:", ["best", "128k", "64k"])
            extension = st.selectbox("Select extension:", ["mp3", "wav", "m4a"])

        if st.button("Download"):
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
            }
            if download_type == "Video":
                ydl_opts.update({
                    'format': f'bestvideo[height<={quality.replace("p","")}]+bestaudio/best[height<={quality.replace("p","")}]',
                    'merge_output_format': extension,
                })
            else:
                ydl_opts.update({
                    'format': f'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': extension,
                        'preferredquality': quality.replace('k',''),
                    }],
                })
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                st.success(f"Downloaded as {filename}")
                # Offer file for user download
                with open(filename, "rb") as f:
                    st.download_button(
                        label=f"Click to download {filename}",
                        data=f.read(),
                        file_name=filename,
                        mime="application/octet-stream"
                    )
            except Exception as e:
                st.error(f"Download error: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
