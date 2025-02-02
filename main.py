import tkinter as tk
import time
import os, sys
import yt_dlp
import sv_ttk
import customtkinter as ctk
import threading
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
        urlLabel = ctk.CTkLabel(self.root, text="Output Folder")
        urlLabel.grid(row=1, column=0, padx=5, pady=5)
        self.urlInput = ctk.CTkEntry(self.root, width=int(self.height / 2))
        self.urlInput.grid(row=1, column=1, padx=5, pady=5)

        # Setup Download Button
        self.dlButton = ctk.CTkButton(self.root, text="Directory")
        self.dlButton.grid(row=1, column=2, padx=5, pady=5)

        # Thumbnail Image section
        #img = tk.PhotoImage(file="./ytdlpGUI.png")
        img = ctk.CTkImage(light_image=Image.open('./ytdlpGUI.png'), size=(int(self.height / 3), int(self.width / 3)))
        imageLabel = ctk.CTkLabel(self.root, image=img, text="")
        imageLabel.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)

        # Status area panel
        #statusLabel = ctk.CTkLabel(self.root, text="Log:")
        #statusLabel.grid(row=3, column=0, padx=5, pady=5)
        self.statusArea = ctk.CTkTextbox(self.root, height=int(self.width / 5), width=int(self.height / 3))#scrolledtext.ScrolledText(self.root, height=10)#ctk.CTkScrollableFrame(self.root, height=8)
        self.statusArea.grid(row=3, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.statusArea.configure(state='disabled')
        
        
        # # Configure grid layout (3x3)
        # self.root.grid_columnconfigure(0, weight=3)
        # self.root.grid_columnconfigure(1, weight=0)
        # self.root.grid_columnconfigure(2, weight=1)
        # self.root.grid_rowconfigure(1, weight=1)
        # self.root.grid_rowconfigure(2, weight=0)
        
        # # URL Entry and Button (row 0)
        # #self.url_label = ctk.CTkLabel(self.root, text="URL:")
        # #self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # self.urlInput = ctk.CTkEntry(self.root)
        # self.urlInput.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew", columnspan=2)
        
        # self.dlButton = ctk.CTkButton(self.root, text="Fetch", command=self.MainButton)
        # self.dlButton.grid(row=0, column=3, padx=10, pady=10, sticky="e")
        
        # # Image Area (row 1)
        # self.imageFrame = ctk.CTkFrame(self.root, corner_radius=0)
        # self.imageFrame.grid(row=1, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # self.imageLabel = ctk.CTkLabel(self.imageFrame, text="Image Area", fg_color="gray20", corner_radius=8)
        # self.imageLabel.pack(padx=10, pady=10, fill="both", expand=True)
        
        # # Scroll Area (right side)
        # self.optionsFrame = ctk.CTkScrollableFrame(self.root, label_text="Scroll Area")
        # self.optionsFrame.grid(row=1, column=2, rowspan=2, padx=(0, 10), pady=10, sticky="nsew", columnspan=2)
        
        # # Add some example widgets to scroll area
        # for i in range(10):
        #     label = ctk.CTkLabel(self.optionsFrame, text=f"Item {i+1}")
        #     label.pack(pady=2)
        
        # # Log Text Area (bottom left)
        # self.statusArea = ctk.CTkTextbox(self.root, height=100, corner_radius=8)
        # self.statusArea.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        # self.statusArea.insert("0.0", "Log messages will appear here...\n\n")
        # self.statusArea.configure(state="disabled")
        
        # # Configure weights for resizing
        # self.imageFrame.grid_columnconfigure(0, weight=1)
        # self.imageFrame.grid_rowconfigure(0, weight=1)
        # self.optionsFrame.grid_columnconfigure(0, weight=1)
        
    def MainButton(self):
        if not self.urlInput.get():
             return
        
        threading.Thread(target=self.DLThread, args=(self.urlInput.get(), ), daemon=True).start()

    def DLThread(self, url):
        ydl_opts = {
            'ignoreerrors': True,
            'progress_hooks': [self.ProgressBar],
            'logger': self,
            'noprogress': True  # Disable default progress output
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.SendStatusMessage("Download completed successfully")

        except Exception as e:
            self.SendStatusMessage(f"Error: {str(e)}")

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

app = GUI()
