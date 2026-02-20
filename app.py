import streamlit as st
import subprocess
import threading
import os
from pathlib import Path
import time

st.set_page_config(
    page_title="YouTube Audio Loader",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
    }
    .title {
        text-align: center;
        color: #00ff88;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .stButton>button {
        background: #00ff88;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        font-size: 1.2em;
        width: 100%;
    }
    .stButton>button:hover {
        background: #00cc6a;
    }
    .file-item {
        background: #333;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .download-folder {
        text-align: center;
        margin-top: 20px;
        padding: 20px;
        background: #252525;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎵 YouTube Audio Loader</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Download MP3 from YouTube and drag to your DAW</p>', unsafe_allow_html=True)

output_dir = Path.home() / "Music" / "YouTubeDownloads"
output_dir.mkdir(parents=True, exist_ok=True)

url = st.text_input("", placeholder="Paste YouTube URL here...", help="Enter the YouTube video URL")

col1, col2 = st.columns([2, 1])
with col1:
    if st.button("⬇️ DOWNLOAD MP3", use_container_width=True):
        if url.strip():
            with st.spinner("Downloading... Please wait..."):
                try:
                    cmd = [
                        "yt-dlp", "-f", "bastaudio",
                        "--extract-audio", "--audio-format", "mp3", "--audio-quality", "0",
                        "-o", str(output_dir / "%(title)s.%(ext)s"), url
                    ]
                    subprocess.run(cmd, capture_output=True, check=True)
                    st.success("✅ Download complete!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a YouTube URL")

st.markdown("---")

st.markdown("### 📁 Downloaded Files")

files = sorted(output_dir.glob("*.mp3"), key=lambda x: os.path.getmtime(x), reverse=True)

if files:
    for f in files:
        col_file, col_btn = st.columns([3, 1])
        with col_file:
            st.markdown(f"""
            <div class="file-item">
                <span>🎵 {f.name}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            pass
    
    st.markdown(f"""
    <div class="download-folder">
        <p>📂 Files saved to:</p>
        <code>{output_dir}</code>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No files downloaded yet")

if st.button("📂 Open Downloads Folder"):
    os.startfile(str(output_dir))
