import streamlit as st
import yt_dlp
import os
import base64

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
        # Only show formats with valid download URLs
        valid_formats = [f for f in formats if f.get('url') and not f.get('downloader_options', {}).get('forbidden', False)]
        if download_type == "Video":
            video_formats = [f for f in valid_formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            options = [f"{f['format_id']} - {f.get('format_note','')} - {f.get('ext','')} - {f.get('resolution','')}" for f in video_formats]
        else:
            audio_formats = [f for f in valid_formats if f.get('vcodec') == 'none']
            options = [f"{f['format_id']} - {f.get('format_note','')} - {f.get('ext','')} - {f.get('abr','')}kbps" for f in audio_formats]

        if options:
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
                        data = f.read()
                    b64 = base64.b64encode(data).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Click to download {filename}</a>'
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    if '403' in str(e):
                        st.error("Download forbidden by YouTube (HTTP 403). This may be due to copyright, region, or age restrictions.")
                    else:
                        st.error(f"Download error: {e}")
        else:
            st.warning("No downloadable formats available for this video/audio. It may be restricted or unavailable.")
    except Exception as e:
        st.error(f"Error: {e}")