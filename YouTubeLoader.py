import sys
import subprocess
import threading
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QListWidget, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer

class YouTubeLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Loader")
        self.setGeometry(100, 100, 400, 440)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        
        layout = QVBoxLayout()
        
        self.title = QLabel("YouTube Loader")
        self.title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff88;")
        layout.addWidget(self.title)
        
        self.url = QLineEdit()
        self.url.setPlaceholderText("Paste YouTube URL here...")
        self.url.setStyleSheet("background: #333; color: white; padding: 8px; border: none;")
        layout.addWidget(self.url)
        
        self.download_btn = QPushButton("DOWNLOAD MP3")
        self.download_btn.setStyleSheet("background: #00ff88; color: black; padding: 10px; font-weight: bold; border: none;")
        self.download_btn.clicked.connect(self.download)
        layout.addWidget(self.download_btn)
        
        self.status = QLabel("Ready")
        self.status.setStyleSheet("color: #888;")
        layout.addWidget(self.status)
        
        self.files = QListWidget()
        self.files.setStyleSheet("background: #252525; color: white; border: none;")
        self.files.itemDoubleClicked.connect(self.open_folder)
        layout.addWidget(self.files)
        
        self.out = Path.home() / "Music" / "YouTubeDownloads"
        self.out.mkdir(parents=True, exist_ok=True)
        
        self.load_files()
        self.open_folder()
        
        self.setLayout(layout)
        
    def load_files(self):
        self.files.clear()
        for f in sorted(self.out.glob("*.mp3"), key=lambda x: os.path.getmtime(x), reverse=True):
            self.files.addItem(f.name)
            
    def open_folder(self, item=None):
        # Open folder and keep it open
        subprocess.Popen(f'explorer "{self.out}"')
        
    def download(self):
        url = self.url.text().strip()
        if not url:
            self.status.setText("Enter URL!")
            self.status.setStyleSheet("color: red;")
            return
            
        self.status.setText("Downloading... folder will open when done")
        self.status.setStyleSheet("color: yellow;")
        self.download_btn.setEnabled(False)
        
        thread = threading.Thread(target=self._download, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _download(self, url):
        cmd = [
            "yt-dlp", "-f", "bestaudio",
            "--extract-audio", "--audio-format", "mp3", "--audio-quality", "0",
            "-o", str(self.out / "%(title)s.%(ext)s"), url
        ]
        
        try:
            subprocess.run(cmd, capture_output=True)
            QTimer.singleShot(100, self.download_done)
        except Exception as e:
            QTimer.singleShot(100, lambda: self.download_error(str(e)))
            
    def download_done(self):
        self.status.setText("Done! Folder open - drag file to DAW")
        self.status.setStyleSheet("color: #00ff88;")
        self.download_btn.setEnabled(True)
        self.url.clear()
        self.load_files()
        
        # Open folder and keep it open
        self.open_folder()
        
    def download_error(self, err):
        self.status.setText(f"Error: {err}")
        self.status.setStyleSheet("color: red;")
        self.download_btn.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = YouTubeLoader()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
