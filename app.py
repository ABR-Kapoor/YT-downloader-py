import streamlit as st
import yt_dlp
import os
import base64

# Title
st.title("YouTube Downloader")
st.markdown("Download videos and audio from YouTube with ease.")

# --- Helper Functions ---
def get_video_info(url):
    """Extracts video information using yt-dlp."""
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            return ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            st.error(f"Error: Could not retrieve video information. Please check the URL. Details: {e}")
            return None

# --- Main App Logic ---
url = st.text_input("Enter YouTube video URL:")

if url:
    info = get_video_info(url)
    if info:
        st.info("Video found! Please choose your download options below.")
        download_type = st.radio("Download type:", ["Video", "Audio"], horizontal=True)
        
        options = []
        if download_type == "Video":
            # Filter for formats that have both video and audio
            video_formats = [f for f in info.get('formats', []) if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
            video_formats.sort(key=lambda f: f.get('height', 0), reverse=True)
            options = [f"{f['format_id']} - {f.get('resolution', 'N/A')} ({f.get('ext')})" for f in video_formats]
        else: # Audio
            audio_formats = [f for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            audio_formats.sort(key=lambda f: f.get('abr', 0), reverse=True)
            options = [f"{f['format_id']} - {f.get('format_note','')} ({f.get('ext')}) - {f.get('abr',0)}kbps" for f in audio_formats]

        if options:
            selected_option = st.selectbox("Choose a format:", options)
            
            if st.button("Prepare Download"):
                format_id = selected_option.split(' - ')[0]
                
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'format': format_id,
                }

                try:
                    with st.spinner("Downloading and preparing your file..."):
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            download_info = ydl.extract_info(url, download=True)
                            filename = ydl.prepare_filename(download_info)

                    if filename and os.path.exists(filename):
                        st.success("Your download is ready!")
                        with open(filename, "rb") as f:
                            data = f.read()
                        
                        # Create the download button
                        st.download_button(
                            label=f"Click to download {os.path.basename(filename)}",
                            data=data,
                            file_name=os.path.basename(filename),
                            mime="application/octet-stream"
                        )
                        
                        # Clean up the downloaded file from the server
                        try:
                            os.remove(filename)
                        except OSError:
                            pass # Non-critical error
                    else:
                        st.error("Sorry, we couldn't prepare your download. Please try again.")

                except Exception as e:
                    st.error(f"Oops, something went wrong during the download. Details: {e}")
        else:
            st.warning("Sorry, we couldn't find any suitable download formats for this video.")
