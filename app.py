import streamlit as st
import yt_dlp
import os

# Title
st.title("YouTube Downloader")

# Step 1: Get YouTube link
url = st.text_input("Enter YouTube video URL:")

if url:
    try:
        st.success(f"URL: {url}")
        download_type = st.radio("Download type:", ["Video", "Audio"])
        # Get available formats
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        if download_type == "Video":
            video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            options = [f"{f['format_id']} - {f.get('format_note','')} - {f.get('ext','')} - {f.get('resolution','')}" for f in video_formats]
        else:
            audio_formats = [f for f in formats if f.get('vcodec') == 'none']
            options = [f"{f['format_id']} - {f.get('format_note','')} - {f.get('ext','')} - {f.get('abr','')}kbps" for f in audio_formats]

        selected = st.selectbox("Select available format:", options)
        if st.button("Download"):
            format_id = selected.split(' - ')[0]
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': format_id,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                st.success(f"Downloaded as {filename}")
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
