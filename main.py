import tkinter as tk
from tkinter import filedialog
import time
import os, sys
import yt_dlp
import sv_ttk
import customtkinter as ctk
import threading
import subprocess
from PIL import Image

class GUI:

    
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('YT-DLP GUI')
        #self.root.resizable(0, 0)
        #sv_ttk.set_theme("dark")
        ctk.set_appearance_mode("System")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")
        
        self.height = self.root.winfo_screenwidth()
        self.width = self.root.winfo_screenheight()
        self.root.geometry(f'{int(self.height / 1.5)}x{int(self.width / 1.5)}')
        
        self.SetupUI()

        self.root.mainloop()


    def SetupUI(self):
        self.root.grid_columnconfigure(0, weight=0)
        #self.root.grid_rowconfigure(1, weight=1)
        #self.root.grid_rowconfigure(3, weight=2)

        # Setup URL Input
        urlLabel = ctk.CTkLabel(self.root, text="URL")
        urlLabel.grid(row=0, column=0, padx=5, pady=5)
        self.urlInput = ctk.CTkEntry(self.root, width=int(self.height / 2))
        self.urlInput.grid(row=0, column=1, padx=5, pady=5)

        # Setup Download Button
        self.dlButton = ctk.CTkButton(self.root, text="Download", command=self.MainButton)
        self.dlButton.grid(row=0, column=2, padx=5, pady=5)

        # Setup File Output
        directoryLabel = ctk.CTkLabel(self.root, text="Output Folder")
        directoryLabel.grid(row=1, column=0, padx=5, pady=5)
        self.directoryInput = ctk.CTkEntry(self.root, width=int(self.height / 2))
        self.directoryInput.grid(row=1, column=1, padx=5, pady=5)

        # Setup Download Button
        self.dirButton = ctk.CTkButton(self.root, text="Directory", command=self.SelectOutputDirectory)
        self.dirButton.grid(row=1, column=2, padx=5, pady=5)

        # Status and Image area frame
        # self.InfoArea = ctk.CTkScrollableFrame(self.root, label_text='', width=(int(self.width / 5)), height=(int(self.height / 2)))
        # self.InfoArea.grid(row=2, column=0, padx=5, pady=5, stick='nsw', rowspan=2, columnspan=2)

        # Thumbnail Image section
        #img = tk.PhotoImage(file="./ytdlpGUI.png")
        img = ctk.CTkImage(light_image=Image.open('./ytdlpGUI.png'), size=(int(self.height / 2), int(self.width / 2)))
        imageLabel = ctk.CTkLabel(self.root, image=img, text="")
        imageLabel.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)

        # Status area panel
        #statusLabel = ctk.CTkLabel(self.root, text="Log:")
        #statusLabel.grid(row=3, column=0, padx=5, pady=5)
        self.statusArea = ctk.CTkTextbox(self.root, height=int(self.width / 5), width=int(self.height / 3))#scrolledtext.ScrolledText(self.root, height=10)#ctk.CTkScrollableFrame(self.root, height=8)
        self.statusArea.grid(row=3, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.statusArea.configure(state='disabled')

        # Options for video panel, Frame setup
        self.optionsFrame = ctk.CTkScrollableFrame(self.root, label_text="Options")
        self.optionsFrame.grid(row=2, column=1, padx=5, pady=5, stick='nse', rowspan=2, columnspan=2)

        # Actual options setup here
        ctk.CTkLabel(self.optionsFrame, text="Output Format: ").grid(row=0, column=0, pady=5, padx=5)
        self.outputFormat = ctk.CTkSegmentedButton(self.optionsFrame)
        self.outputFormat.grid(row=0, column=1, pady=5)
        self.outputFormat.configure(values=["Video", "Audio only"])
        self.outputFormat.set('Video')

        ctk.CTkLabel(self.optionsFrame, text="Video Quality: ").grid(row=1, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.vidQuality = ctk.CTkOptionMenu(self.optionsFrame, values=['144', '240', '480', '720', '1080', '1440', '2160'], dynamic_resizing=False)
        self.vidQuality.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.optionsFrame, text="Audio Quality: ").grid(row=2, column=0, pady=5, padx=5) # AUDIO QUALITY
        self.audioQuality = ctk.CTkOptionMenu(self.optionsFrame, values=['32', '96', '128', '160', '192', '256'], dynamic_resizing=False)
        self.audioQuality.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.optionsFrame, text="Audio Format: ").grid(row=3, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.audioFormat = ctk.CTkOptionMenu(self.optionsFrame, values=['mp3', 'opus'], dynamic_resizing=False)
        self.audioFormat.grid(row=3, column=1, padx=5, pady=5)

        self.splitChapters = ctk.CTkCheckBox(self.optionsFrame, text="Split by Chapters")
        self.splitChapters.grid(row=4, column=0, padx=5, pady=5)
        
        
    def UI2(self):
        # Configure grid layout (3x3)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=0)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        
        # URL Entry and Button (row 0)
        #self.url_label = ctk.CTkLabel(self.root, text="URL:")
        #self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.urlInput = ctk.CTkEntry(self.root)
        self.urlInput.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew", columnspan=2)
        
        self.dlButton = ctk.CTkButton(self.root, text="Fetch", command=self.MainButton)
        self.dlButton.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        
        # Image Area (row 1)
        self.imageFrame = ctk.CTkFrame(self.root, corner_radius=0)
        self.imageFrame.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        self.imageLabel = ctk.CTkLabel(self.imageFrame, text="Image Area", fg_color="gray20", corner_radius=8)
        self.imageLabel.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Scroll Area (right side)
        self.optionsFrame = ctk.CTkScrollableFrame(self.root, label_text="Scroll Area")
        self.optionsFrame.grid(row=1, column=2, rowspan=2, padx=(0, 10), pady=10, sticky="nsew", columnspan=2)
        
        # Add some example widgets to scroll area
        for i in range(10):
            label = ctk.CTkLabel(self.optionsFrame, text=f"Item {i+1}")
            label.pack(pady=2)
        
        # Log Text Area (bottom left)
        self.statusArea = ctk.CTkTextbox(self.root, height=100, corner_radius=8)
        self.statusArea.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.statusArea.insert("0.0", "Log messages will appear here...\n\n")
        self.statusArea.configure(state="disabled")
        
        # Configure weights for resizing
        self.imageFrame.grid_columnconfigure(0, weight=1)
        self.imageFrame.grid_rowconfigure(0, weight=1)
        self.optionsFrame.grid_columnconfigure(0, weight=1)
        
    def MainButton(self):
        if self.directoryInput.get() == "":
            self.SendStatusMessage("No output directory.")

            return

        if not self.urlInput.get():
            self.SendStatusMessage("No link.")

            return
        
        threading.Thread(target=self.DLThread, args=(self.urlInput.get(), ), daemon=True).start()

    def DLThread(self, url):
        try:
            cmd = ['yt-dlp']
            output_dir = self.directoryInput.get()
            
            # Create directory first (without filename template)
            os.makedirs(output_dir, exist_ok=True)  # Fix 1: Create directory separately

            cmd.extend(['-P', output_dir])
            
            # Build output template
            if self.splitChapters.get():
                cmd.append('--split-chapters')
                # output_template = os.path.join(output_dir, '%(title)s [%(chapter)s].%(ext)s')
                cmd.extend(['-o', '%(title)s [%(chapter)s].%(ext)s'])
            else:
                # output_template = os.path.join(output_dir, '%(title)s.%(ext)s')  # Fix 2: Template includes directory
                cmd.extend(['-o', '%(title)s.%(ext)s'])
            
            # cmd.extend(['-o', output_template])

            # Format selection
            if self.outputFormat.get() == "Audio only":
                cmd.extend(['-x', '--audio-format', f'{self.audioFormat.get()}', '--audio-quality', f'{self.audioQuality.get()}k'])
            else:
                cmd.extend(['-f', f'bestvideo[height<={self.vidQuality.get()}]+bestaudio'])
            
            cmd.append(url)
            
            self.SendStatusMessage(f"Executing command: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                text=True
            )
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break

                if line:
                    self.SendStatusMessage(line.strip())
            
            if process.returncode == 0:
                self.SendStatusMessage("Download completed successfully")

            else:
                self.SendStatusMessage(f"Error occurred (exit code {process.returncode})")

        except Exception as e:
            self.SendStatusMessage(f"Error: {str(e)}")

    def UpdateOptionsConfiguration(self, info):
        self.SendStatusMessage(f'\n{self.outputFormat.get()} mode. Video quality: {self.vidQuality.get()} Audio quality: {self.audioQuality.get()}\n')

        opts = {
            'format': f'bestvideo[height<={self.vidQuality.get()}]+bestaudio',
            'ignoreerrors': True,
            'progress_hooks': [self.ProgressBar],
            'logger': self,
            'noprogress': True,
            'outtmpl': self.directoryInput.get() + info.get('title') + '.' + info.get('ext'),
            # Removed 'postprocessors' to allow yt-dlp defaults (includes merger if needed)
        }

        if self.splitChapters.get():
            self.SendStatusMessage('Splitting chapters into individual videos.')
            # Ensure directory path ends with a separator
            directory = self.directoryInput.get().rstrip('/\\') + '/'
            opts.update({
                'outtmpl': f"{directory}%(title)s [%(chapter)s].%(ext)s",
                'postprocessors': [
                    {'key': 'FFmpegMerger'},  # Merge video + audio first
                    {'key': 'FFmpegSplitChapters'}  # Then split into chapters
                ]
            })

        if self.outputFormat.get() == "Audio only":
            # Convert audio quality to bitrate (e.g., 192 -> '192k')
            audio_bitrate = f"{self.audioQuality.get()}k"
            opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': self.audioQuality.get(),
                }],
                'outtmpl': f"{self.directoryInput.get()}/%(title)s"
            })

        return opts

    def ProgressBar(self, d):
        if d['status'] == 'downloading':
            msg = (f"Downloading: {d.get('_percent_str', '')} "
                   f"of {d.get('_total_bytes_str', '')} "
                   f"at {d.get('_speed_str', '')}")
            
        elif d['status'] == 'finished':
            msg = "Post-processing complete"

        else:
            return
        
        self.SendStatusMessage(msg)

    def debug(self, msg):
        # Filter out redundant messages
        if "Deleting original file" not in msg:
            self.SendStatusMessage(msg)

    def warning(self, msg):
        self.SendStatusMessage(f"Warning: {msg}")

    def error(self, msg):
        self.SendStatusMessage(f"ERROR: {msg}")

    def SendStatusMessage(self, msg):
        self.root.after(0, self.UpdateStatusDisplay, msg)

    def UpdateStatusDisplay(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.statusArea.configure(state='normal')

        self.statusArea.insert('end', f'[{timestamp}] {message}\n')

        self.statusArea.see('end')  # Auto-scroll to bottom
        self.statusArea.configure(state='disabled')

    def SelectOutputDirectory(self):
        # Open the directory dialog
        fileOutputPath = filedialog.askdirectory(
            title="Select a Folder",
            initialdir="~"  # Start at user's home directory
        ) + '/'
        # directory = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
        # if directory:
        #     self.dir_input.delete(0, ctk.END)
        #     self.dir_input.insert(0, directory + '/')
        
        if fileOutputPath:
            self.directoryInput.delete(0, ctk.END)
            self.directoryInput.insert(0, fileOutputPath)

app = GUI()
