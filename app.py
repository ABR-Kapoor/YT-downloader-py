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
        st.info("Checking video details...")
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
            selected_option = st.selectbox("Choose a format:", options)
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

                if 'merge_output_format' in ydl_opts:
                    st.info("Please wait, we're preparing your download. This might take a moment...")

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = info.get('_filename')

                    if filename and os.path.exists(filename):
                        st.success("Your download is ready!")
                        with open(filename, "rb") as f:
                            data = f.read()
                        b64 = base64.b64encode(data).decode()
                        button_html = f'''
<style>
    .download-btn {{
        display: inline-block;
        padding: 0.5em 1em;
        color: white;
        background-color: #FF4B4B;
        border-radius: 0.25rem;
        text-decoration: none;
        font-weight: bold;
    }}
    .download-btn:hover {{
        background-color: #FF6B6B;
    }}
</style>
<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(filename)}" class="download-btn">Download {os.path.basename(filename)}</a>
'''
                        st.markdown(button_html, unsafe_allow_html=True)
                        
                        # Clean up the downloaded file from the server
                        try:
                            os.remove(filename)
                        except OSError:
                            # This error is not critical for the user experience, so we can ignore it.
                            pass
                    else:
                        st.error("Sorry, we couldn't prepare your download. Please try a different format or check the URL.")

                except Exception:
                    st.error("Oops, something went wrong. If you chose a 'video-only' format, it may require special tools on our end. Please try a format that includes audio.")
        else:
            st.warning("Sorry, we couldn't find any downloadable formats for this video. It might be private, age-restricted, or unavailable.")
    except Exception:
        st.error("An unexpected error occurred. Please double-check the URL or try again.")