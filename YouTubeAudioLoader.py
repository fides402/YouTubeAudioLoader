import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
from pathlib import Path

class YouTubeLoader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Loader")
        self.root.geometry("380x320")
        self.root.attributes('-topmost', True)
        
        self.bg = "#1e1e1e"
        self.root.configure(bg=self.bg)
        
        tk.Label(root, text="YouTube Loader", font=("Arial", 12, "bold"),
                bg=self.bg, fg="#00ff88").pack(pady=10)
        
        self.url = tk.Entry(root, font=("Arial", 10), bg="#333", fg="white")
        self.url.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Button(root, text="DOWNLOAD (FAST)", command=self.download, 
                bg="#00ff88", fg="black", font=("Arial", 9, "bold")).pack(pady=5)
        
        self.status = tk.Label(root, text="", bg=self.bg, fg="#888", font=("Arial", 9))
        self.status.pack()
        
        tk.Label(root, text="Double-click to drag to DAW", bg=self.bg, fg="#666", font=("Arial", 8)).pack(pady=5)
        
        self.files = tk.Listbox(root, bg="#252525", fg="white", bd=0,
                              selectbackground="#00ff88", font=("Arial", 10))
        self.files.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        self.files.bind('<Double-Button-1>', self.open)
        
        self.out = Path.home() / "Music" / "YouTubeDownloads"
        self.out.mkdir(parents=True, exist_ok=True)
        
        self.load()
        
    def load(self):
        self.files.delete(0, tk.END)
        for f in sorted(self.out.glob("*.mp3"), key=lambda x: os.path.getmtime(x), reverse=True):
            self.files.insert(0, f.name)
            
    def download(self):
        url = self.url.get().strip()
        if not url:
            self.status.config(text="Enter URL", fg="red")
            return
        self.status.config(text="Downloading... (faster mode)", fg="yellow")
        threading.Thread(target=self._dl, args=(url,)).start()
        
    def _dl(self, url):
        # Faster: use m4a audio only (no conversion needed)
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",  # Best audio only (no video)
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", str(self.out / "%(title)s.%(ext)s"),
            url
        ]
        
        try:
            subprocess.run(cmd, capture_output=True)
            self.root.after(0, self.done)
        except Exception as e:
            self.root.after(0, lambda: self.status.config(text=str(e), fg="red"))
            
    def done(self):
        self.status.config(text="Done! Double-click to drag", fg="#00ff88")
        self.url.delete(0, tk.END)
        self.load()
        
    def open(self, event):
        idx = self.files.nearest(event.y)
        if idx >= 0:
            fname = self.files.get(idx)
            subprocess.Popen(f'explorer /select,"{self.out / fname}"')

YouTubeLoader(tk.Tk()).root.mainloop()
