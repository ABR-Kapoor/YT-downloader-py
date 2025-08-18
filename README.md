# YouTube Downloader Streamlit App

## Overview
This application allows users to download YouTube videos or audio in various formats and qualities using a simple web interface built with Streamlit.

## Features
- Input a YouTube video URL
- Select download type: Video or Audio
- Choose quality (resolution for video, bitrate for audio)
- Select file extension (mp4, mp3, wav)
- Download the selected content

## Technologies Used
- **Streamlit**: For building the interactive web UI
- **pytube**: For downloading YouTube content
- **pydub**: For audio format conversion

## Setup Instructions
1. **Install dependencies**:
   ```powershell
   pip install streamlit pytube pydub
   ```
   - You may also need to install ffmpeg for audio conversion:
     - Windows: Download from https://ffmpeg.org/download.html and add to PATH
     - Linux/Mac: `sudo apt install ffmpeg` or `brew install ffmpeg`

2. **Run the app**:
   ```powershell
   streamlit run app.py
   ```

## Usage
1. Enter a valid YouTube video URL.
2. Select whether you want to download video or audio.
3. Choose the desired quality and file extension.
4. Click the "Download" button to save the file locally.

## File Structure
- `app.py`: Main Streamlit application
- `.env`: (Optional) Environment variables
- `README.md`: Documentation

## Troubleshooting
- If you see `ModuleNotFoundError`, ensure all dependencies are installed.
- For audio conversion, make sure ffmpeg is installed and accessible in your system PATH.

## License
This project is for educational purposes.
