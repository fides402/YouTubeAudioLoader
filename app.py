import streamlit as st
import os
from pathlib import Path
import yt_dlp
import time
import shutil

st.set_page_config(
    page_title="YouTube Audio Loader",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%);
        min-height: 100vh;
    }
    .title {
        text-align: center;
        color: #00ff88;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        font-size: 1.1em;
        margin-bottom: 2em;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ff88, #00cc6a);
        color: #000;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 40px;
        font-size: 1.2em;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(0,255,136,0.3);
    }
    .file-card {
        background: linear-gradient(135deg, #333, #2a2a2a);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border: 1px solid #444;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .folder-box {
        background: #252525;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-top: 30px;
        border: 1px dashed #444;
    }
    .success-box {
        background: linear-gradient(135deg, #00ff88, #00cc6a);
        color: #000;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
    }
    div[data-testid="stTextInput"] input {
        background: #333;
        color: white;
        border: 2px solid #444;
        border-radius: 10px;
        padding: 15px;
        font-size: 1.1em;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎵 YouTube Audio Loader</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Download audio from YouTube</p>', unsafe_allow_html=True)

output_dir = Path.home() / "Music" / "YouTubeDownloads"
output_dir.mkdir(parents=True, exist_ok=True)

url = st.text_input("", placeholder="Paste YouTube URL here...", label_visibility="collapsed")

if st.button("⬇️ DOWNLOAD AUDIO", use_container_width=True):
    if url.strip():
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with st.spinner("Downloading..."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                st.markdown('''
                <div class="success-box">
                    ✅ Download Complete!
                </div>
                ''', unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a YouTube URL")

st.markdown("---")
st.markdown("### 📁 Your Downloads")

files = sorted(output_dir.glob("*.*"), key=lambda x: os.path.getmtime(x), reverse=True)
audio_files = [f for f in files if f.suffix.lower() in ['.mp3', '.m4a', '.webm', '.wav', '.ogg']]

if audio_files:
    for f in audio_files:
        size = os.path.getsize(f) / (1024 * 1024)
        st.markdown(f'''
        <div class="file-card">
            <span class="file-icon">🎵</span>
            <span class="file-name">{f.name}</span>
            <span style="color: #888;">{size:.1f} MB</span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown(f'''
    <div class="folder-box">
        <p style="color: #888; margin-bottom: 10px;">📂 Files saved to:</p>
        <code style="color: #00ff88;">{output_dir}</code>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.info("🎵 No downloads yet. Paste a URL above!")

if st.button("📂 Open Downloads Folder"):
    os.startfile(str(output_dir))
