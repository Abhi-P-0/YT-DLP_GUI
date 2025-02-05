import time
import os
import customtkinter as ctk
from customtkinter import filedialog
import threading
import subprocess
from PIL import Image

class GUI:

    
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('YT-DLP GUI')
        
        ctk.set_appearance_mode("System")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")
        
        self.height = self.root.winfo_screenwidth()
        self.width = self.root.winfo_screenheight()
        self.root.geometry(f'{int(self.height / 1.5)}x{int(self.width / 1.5)}')
        
        self.SetupUI()

        self.root.mainloop()


    def SetupUI(self):
        self.root.columnconfigure(0, weight=8)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)
        
        self.inputFrame = ctk.CTkFrame(self.root)
        self.inputFrame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.infoFrame = ctk.CTkFrame(self.root)
        self.infoFrame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.configFrame = ctk.CTkFrame(self.root)
        self.configFrame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
        # INPUT AREA setup --------------------------------------------------------------------------------------------------------------------

        ctk.CTkLabel(self.inputFrame, text="URL:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.urlEntry = ctk.CTkEntry(self.inputFrame, width=int(self.width))
        self.urlEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.fetchButton = ctk.CTkButton(self.inputFrame, text="Download", command=self.MainButton)
        self.fetchButton.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Configure frame's internal column weights
        self.inputFrame.columnconfigure(1, weight=10)  # Makes entry expand
        self.inputFrame.columnconfigure(2, weight=1)

        # ------------------------------------

        ctk.CTkLabel(self.inputFrame, text="Directory:").grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.directoryEntry = ctk.CTkEntry(self.inputFrame, width=int(self.width))
        self.directoryEntry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.directoryInput = ctk.CTkButton(self.inputFrame, text="Browse", command=self.SelectOutputDirectory)
        self.directoryInput.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # ------------------------------------------------------------------------------------------------------------------------------

        # INFO AREA setup --------------------------------------------------------------------------------------------------------------------

        self.imageArea = ctk.CTkLabel(self.infoFrame, text="Thumbnail....", fg_color="gray20", corner_radius=8)
        self.imageArea.pack(padx=10, pady=10, fill="both", expand=True)

        self.statusArea = ctk.CTkTextbox(self.infoFrame, height=int(self.height / 12), corner_radius=8)
        self.statusArea.pack(padx=10, pady=10, fill='both')
        self.statusArea.insert("end", f"[{time.strftime('%H:%M:%S')}]: start ...\n\n")
        self.statusArea.configure(state="disabled")

        # ------------------------------------------------------------------------------------------------------------------------------
        
        # Actual options setup here
        ctk.CTkLabel(self.configFrame, text="Output Format: ").grid(row=0, column=0, pady=5, padx=5)
        self.outputFormat = ctk.CTkSegmentedButton(self.configFrame)
        self.outputFormat.grid(row=0, column=1, pady=5)
        self.outputFormat.configure(values=["Video", "Audio only"])
        self.outputFormat.set('Video')

        ctk.CTkLabel(self.configFrame, text="Video Quality: ").grid(row=1, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.vidQuality = ctk.CTkOptionMenu(self.configFrame, values=['144', '240', '480', '720', '1080', '1440', '2160'], dynamic_resizing=False)
        self.vidQuality.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text="Audio Quality: ").grid(row=2, column=0, pady=5, padx=5) # AUDIO QUALITY
        self.audioQuality = ctk.CTkOptionMenu(self.configFrame, values=['32', '96', '128', '160', '192', '256'], dynamic_resizing=False)
        self.audioQuality.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text="Audio Format: ").grid(row=3, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.audioFormat = ctk.CTkOptionMenu(self.configFrame, values=['mp3', 'opus'], dynamic_resizing=False)
        self.audioFormat.grid(row=3, column=1, padx=5, pady=5)

        self.splitChapters = ctk.CTkCheckBox(self.configFrame, text="Split by Chapters")
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
        if self.directoryEntry.get() == "":
            self.SendStatusMessage("No output directory.")

            return

        if not self.urlEntry.get():
            self.SendStatusMessage("No link.")

            return
        
        threading.Thread(target=self.DLThread, args=(self.urlEntry.get(), ), daemon=True).start()

    def DLThread(self, url):
        try:
            cmd = ['yt-dlp']
            output_dir = self.directoryEntry.get()
            
            # Create directory first (without filename template)
            os.makedirs(output_dir, exist_ok=True)  # Fix 1: Create directory separately

            cmd.extend(['-P', output_dir])
            
            # Build output template
            if self.splitChapters.get():
                cmd.append('--split-chapters')
                cmd.extend(['-o', '%(title)s [%(chapter)s].%(ext)s'])
                
            else:
                cmd.extend(['-o', '%(title)s.%(ext)s'])
            
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
            
            while True: # Output to status window in the UI
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
        )
        
        if fileOutputPath:
            fileOutputPath += '/'
            self.directoryEntry.delete(0, ctk.END)
            self.directoryEntry.insert(0, fileOutputPath)

app = GUI()
