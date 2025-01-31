import tkinter as tk
import os, sys
import yt_dlp
import sv_ttk
import customtkinter as ctk

class GUI:

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('YT-DLP GUI')
        self.root.resizable(0, 0)

        self.SetupUI()

        self.root.mainloop()


    def SetupUI(self):
        #sv_ttk.set_theme("dark")
        ctk.set_appearance_mode("System")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")
        
        height = self.root.winfo_screenwidth()
        width = self.root.winfo_screenheight()

        self.root.geometry(f'{int(height / 1.5)}x{int(width / 1.5)}')

        # Setup URL Input
        urlLabel = ctk.CTkLabel(self.root, text="URL")
        urlLabel.grid(row=0, column=0, padx=5, pady=5)
        urlInput = ctk.CTkEntry(self.root, width=int(height / 2))
        urlInput.grid(row=0, column=1, padx=5, pady=5)

        #Setup Download Button
        dlButton = ctk.CTkButton(self.root, text="Download")
        dlButton.grid(row=0, column=2, padx=5, pady=5)
        

app = GUI()
