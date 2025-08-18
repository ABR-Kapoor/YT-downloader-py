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
        
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        
        formats = info.get('formats', [])
        # Relaxed filter as per user request to show more qualities
        valid_formats = [f for f in formats if f.get('url')]

        formats_for_type = []
        options = []

        if download_type == "Video":
            # Show all video formats, including those without audio
            formats_for_type = [f for f in valid_formats if f.get('vcodec') != 'none']
            # Sort by resolution
            formats_for_type.sort(key=lambda f: f.get('height', 0), reverse=True)
            options = [f"{f['format_id']} - {f.get('resolution', 'N/A')} - {f.get('ext','')} - {'video-only (will be merged with best audio)' if f.get('acodec') == 'none' else 'video+audio'}" for f in formats_for_type]
        else: # Audio
            formats_for_type = [f for f in valid_formats if f.get('acodec') != 'none']
            # Sort by bitrate
            formats_for_type.sort(key=lambda f: f.get('abr', 0), reverse=True)
            options = [f"{f['format_id']} - {f.get('format_note','')} - {f.get('ext','')} - {f.get('abr','')}kbps" for f in formats_for_type]

        if options:
            selected_option = st.selectbox("Select available format:", options)
            if st.button("Download"):
                format_id = selected_option.split(' - ')[0]
                
                ydl_opts = {}
                if download_type == "Video":
                    # Find the selected format details
                    selected_format = next((f for f in formats_for_type if f['format_id'] == format_id), None)
                    
                    download_format = format_id
                    # If the selected format is video-only, tell yt-dlp to merge it with the best audio
                    if selected_format and selected_format.get('acodec') == 'none':
                        download_format = f'{format_id}+bestaudio/best'
                    
                    ydl_opts = {
                        'outtmpl': '%(title)s.%(ext)s',
                        'format': download_format,
                        'merge_output_format': 'mp4', # Merge into mp4 container
                    }
                else: # Audio
                    # For audio, just download the selected audio format
                    ydl_opts = {
                        'outtmpl': '%(title)s.%(ext)s',
                        'format': format_id,
                    }

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        
                        # After merging, the filename extension might change
                        if download_type == 'Video' and 'merge_output_format' in ydl_opts:
                            base, _ = os.path.splitext(filename)
                            filename = base + '.' + ydl_opts['merge_output_format']

                    st.success(f"Downloaded as {os.path.basename(filename)}")
                    # Check if file exists before reading
                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            data = f.read()
                        b64 = base64.b64encode(data).decode()
                        href = f'''<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(filename)}">Click to download {os.path.basename(filename)}</a>'''
                        st.markdown(href, unsafe_allow_html=True)
                    else:
                        st.error(f"Could not find downloaded file: {filename}. It may be a permission issue or an error during download/merge process.")

                except Exception as e:
                    st.error(f"Download error: {e}. If you are merging formats, make sure ffmpeg is available.")
        else:
            st.warning("No downloadable formats available for this video/audio. It may be restricted or unavailable.")
    except Exception as e:
        st.error(f"Error: {e}")
