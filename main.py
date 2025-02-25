import time
import os
import threading
import subprocess
import requests
import re
import customtkinter as ctk
from customtkinter import filedialog
import yt_dlp
from PIL import Image

class GUI:

    version = 0.51
    stopp = False
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('YT-DLP GUI')
        
        ctk.set_appearance_mode("System")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")
        
        self.height = self.root.winfo_screenwidth()
        self.width = self.root.winfo_screenheight()
        self.root.geometry(f'{int(self.height / 1.5)}x{int(self.width / 1.5)}')
        
        self.SetupUI()

        self.CheckForUpdate()

        self.root.mainloop()


    def SetupUI(self):
        self.root.columnconfigure(0, weight=8)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        
        self.inputFrame = ctk.CTkFrame(self.root)
        self.inputFrame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        self.infoFrame = ctk.CTkFrame(self.root)
        self.infoFrame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.configFrame = ctk.CTkFrame(self.root)
        self.configFrame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        self.bottomFrame = ctk.CTkFrame(self.root)
        self.bottomFrame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=5, pady=(0, 5))
        self.bottomFrame.rowconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(0, weight=2)
        self.bottomFrame.columnconfigure(1, weight=1)
        
        # INPUT AREA setup --------------------------------------------------------------------------------------------------------------------

        ctk.CTkLabel(self.inputFrame, text="URL:").grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.urlEntry = ctk.CTkEntry(self.inputFrame, width=int(self.width))
        self.urlEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.downloadButton = ctk.CTkButton(self.inputFrame, text="Download", command=self.MainButton, fg_color='green')
        self.downloadButton.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

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
        self.statusArea.insert("end", f"[{time.strftime('%H:%M:%S')}]: version: {self.version} | start ...\n\n")
        self.statusArea.configure(state="disabled")

        # ------------------------------------------------------------------------------------------------------------------------------
        
        # Actual options setup here
        ctk.CTkLabel(self.configFrame, text="Output Format: ").grid(row=0, column=0, pady=5, padx=5)
        self.outputFormat = ctk.CTkSegmentedButton(self.configFrame)
        self.outputFormat.grid(row=0, column=1, pady=5)
        self.outputFormat.configure(values=["Video", "Audio only"])
        self.outputFormat.set('Video')

        ctk.CTkLabel(self.configFrame, text="Video Quality: ").grid(row=1, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.vidQuality = ctk.CTkOptionMenu(self.configFrame, values=['144p', '240p', '480p', '720p', '1080p', '1440p', '2160p'], dynamic_resizing=False)
        self.vidQuality.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text="Audio Quality: ").grid(row=2, column=0, pady=5, padx=5) # AUDIO QUALITY
        self.audioQuality = ctk.CTkOptionMenu(self.configFrame, values=['Best', '32k', '96k', '128k', '160k', '192k', '256k'], dynamic_resizing=False)
        self.audioQuality.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text="Audio Format: ").grid(row=3, column=0, pady=5, padx=5) # VIDEO QUALITY
        self.audioFormat = ctk.CTkOptionMenu(self.configFrame, values=['mp3', 'opus'], dynamic_resizing=False)
        self.audioFormat.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text='Split by Chapters if found').grid(row=4, column=0, padx=(15, 5), pady=5)
        self.splitChapters = ctk.CTkCheckBox(self.configFrame, text='')
        self.splitChapters.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.configFrame, text='Playlist').grid(row=5, column=0, padx=(15, 5), pady=5)
        self.playlistSelector = ctk.CTkCheckBox(self.configFrame, text='')
        self.playlistSelector.grid(row=5, column=1, padx=5, pady=5)
        


        self.stoppButton = ctk.CTkButton(self.configFrame, text='Interupt Download', command=self.InteruptDownload, fg_color='red')
        self.stoppButton.grid(row=20, column=0, padx=5, pady=5, sticky='nsew')
        self.stoppButton.configure(state=ctk.DISABLED)

        # --------------------------------------------------------------------------------------------------------------------------------

        self.progressBar = ctk.CTkProgressBar(self.bottomFrame, height=(self.height * 0.009), width=self.width, progress_color='green')
        self.progressBar.grid(row=0, column=0, sticky='ew', padx=5)
        self.progressBar.set(0)

        self.speedLimit = ctk.CTkEntry(self.bottomFrame, height=9, width=100)
        self.speedLimit.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.totalProgressBar = ctk.CTkProgressBar(self.bottomFrame, height=(self.height * 0.009), width=self.width)
        self.totalProgressBar.grid(row=1, column=0, sticky='ew', padx=5, columnspan=2)
        self.totalProgressBar.set(0)
        # self.totalProgressBar.configure(text='1 or 2 total')
        self.totalProgressCount = ctk.StringVar()
        self.totalProgressCount.set('')
        self.totalProgressCounter = ctk.CTkLabel(self.bottomFrame, textvariable=self.totalProgressCount, bg_color="transparent",  text_color='white')
        self.totalProgressCounter.grid(row=1, column=0)
        
        # self.incSpeedLimit = ctk.CTkButton(self.bottomFrame, width=30, text='+')
        # self.incSpeedLimit.grid(row=0, column=2, padx=3)

        # self.decSpeedLimit = ctk.CTkButton(self.bottomFrame, width=30, text='-')
        # self.decSpeedLimit.grid(row=0, column=3, padx=3)

        ctk.CTkLabel(self.bottomFrame, text='B/s').grid(row=0, column=2, padx=5)
        
        
    
    def MainButton(self):
        if self.directoryEntry.get() == "":
            self.SendStatusMessage("No output directory.")

            return

        if not self.urlEntry.get():
            self.SendStatusMessage("No link.")

            return
        
        threading.Thread(target=self.DLThread, args=(self.urlEntry.get(), ), daemon=True).start()

    def DLThread(self, url):
        self.stoppButton.configure(state=ctk.ACTIVE)

        try: # extract info from URL
            with yt_dlp.YoutubeDL({'logger': None, 'noprogress' : True}) as ydls:
                self.SendStatusMessage(f'Extraction info from URL.')
                info_dict = ydls.extract_info(self.urlEntry.get(), download=False)

                numChaps = info_dict.get('chapters')

                self.SetTotalProgress(info_dict)

                self.SendStatusMessage(f'Successfully extracted info.')
                
        except Exception as e:
            self.SendStatusMessage(f'Error: {str(e)}')
        
        try:
            self.downloadButton.configure(state=ctk.NORMAL) # Allow stopping DL

            cmd = ['yt-dlp']
            output_dir = self.directoryEntry.get()
            
            # Create directory first (without filename template)
            os.makedirs(output_dir, exist_ok=True)  # Fix 1: Create directory separately

            if self.playlistSelector.get() or 'playlist' in self.urlEntry.get():
                output_dir += info_dict.get('title') + '/'
                self.SendStatusMessage('Playlist url detected.')
                cmd.append('--yes-playlist')
            
            if self.splitChapters.get() and numChaps != None:
            # if self.splitChapters.get():
                # Set BASE directory with -P (static path)
                # cmd.extend(['-P', output_dir + info_dict.get('title') + '/'])
                if 'title' not in output_dir:
                    output_dir += info_dict.get('title') + '/'
                # cmd.extend(['-P', output_dir + '%(title)s/'])
                
                # Then use -o to create subfolder structure within it
                cmd.extend(['-o', 'full-vid/%(chapter)s.%(ext)s'])  # Folder will use actual title
                cmd.append('--split-chapters')
            else:
                cmd.extend(['-o', '%(title)s.%(ext)s'])

            cmd.extend(['-P', output_dir])

            # Limit download rate
            limit = self.GetSpeedLimit()

            if limit:
                self.SendStatusMessage(f'Limiting download speed to: {limit}B/s')
                cmd.extend(['-r', str(limit)]) # apparently YT-DLP takes String for speed limit, fix later
            
            # Format selection
            if self.outputFormat.get() == "Audio only":
                if self.audioQuality.get() != 'Best':
                    cmd.extend(['-x', '--audio-format', f'{self.audioFormat.get()}', '--audio-quality', self.audioQuality.get()])
                
                else:
                    cmd.extend(['-x', '--audio-format', f'{self.audioFormat.get()}', '--audio-quality', '0'])

            else:
                cmd.extend(['-f', f'bestvideo[height<={self.vidQuality.get()[:-1]}]+bestaudio'])
            
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
                if self.stopp: # if stop button is pressed
                    break

                line = process.stdout.readline()

                if not line and process.poll() is not None:
                    break

                if line:
                    # Check if it's a download-related line
                    if '[download]' in line:
                        # Use regex to find percentage (e.g: "42.5%")
                        match = re.search(r'(\d{1,3}(\.\d+)?)%', line)
                        
                        if match:
                            try:
                                progress = float(match.group(1)) / 100

                                self.progressBar.set(progress)
                                # Optional: Send progress to status
                                # self.SendStatusMessage(f"Download progress: {progress * 100:.1f}%")
                                
                            except (ValueError, AttributeError) as err:
                                self.SendStatusMessage(f'Error occurred with progress bar: {err}')
                        else:
                            # Send non-percentage download messages
                            self.SendStatusMessage(line.strip())
                    else:
                        # Send all non-download messages
                        self.SendStatusMessage(line.strip())
            
            if process.returncode == 0:
                self.SendStatusMessage("Download completed successfully")

            elif self.stopp:
                self.SendStatusMessage(f'Download interupted')

            else:
                self.SendStatusMessage(f"Error occurred (exit code {process.returncode})")

            self.downloadButton.configure(state=ctk.NORMAL)
            self.stoppButton.configure(state=ctk.DISABLED)
            self.stopp = False

        except Exception as e:
            self.SendStatusMessage(f"Error: {str(e)}")

    def SetTotalProgress(self, info):
        playlistTotal = info.get('playlist_count')

        if playlistTotal is not None:
            self.totalProgressCount.set(f'{1} of {playlistTotal} total')

        else:
            self.totalProgressCount.set('1 of 1 total')
            

    def GetSpeedLimit(self):
        temp = self.speedLimit.get().strip()

        try:
            temp = float(temp)

            return temp

        except Exception as err:
            self.SendStatusMessage(f'Invalid input for download speed limit. Use Integer/float values. {err}')

            return None

    def InteruptDownload(self):
        self.stopp = True

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

    def CheckForUpdate(self):
        response = requests.get('https://github.com/Abhi-P-0/YT-DLP_GUI/releases/latest')
        checkedVer = float(response.url.split('/').pop()[1:]) # Version on github (latest)
        
        if checkedVer > self.version:
            self.SendStatusMessage('\n-------------------------------------------\n|\t\t\t|\n|     New version available.\t\t\t|\n|\t\t\t|\n-------------------------------------------')

app = GUI()
