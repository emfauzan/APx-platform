import tkinter
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd
import customtkinter
from customtkinter import filedialog

from sound_control import *
from viewer import *

# System Setting
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("blue")

class Myapp(): # Class for GUI

    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry('1050x600')
        self.root.title("APx Platform")
        
        self.hardware = ["APx525"]
        self.variable = tkinter.StringVar()
        self.variable.set("Choice Hardware Platform")
        
        self.hw_platform = customtkinter.CTkOptionMenu(self.root, variable=self.variable, values=self.hardware)
        self.hw_platform.grid(row=0, column=2, pady=15, sticky="n")
        self.frame_api = customtkinter.CTkFrame(master=self.root)
        self.frame_api.grid(row=1, column=2, padx=(20,20), sticky="n")
        self.entry_folder = customtkinter.CTkLabel(self.frame_api, text="C:\Program Files\Audio Precision\APx500 8.0\API", font=("Lato", 10.5))
        self.entry_folder.grid(row=1, column=2, padx=5, sticky="n")
        self.api_loc = customtkinter.CTkButton(self.root, text="Change API Reference", font=("Ubuntu", 12), command=self.files)
        self.api_loc.grid(row=2, column=2, sticky="n")
        
        # Calibration Frame
        self.frame_1 = customtkinter.CTkFrame(master=self.root)
        self.frame_1.grid(row=4, column=1, padx=(40, 40), pady=(40, 40), sticky="nsew")
        
        # Measurement Frame
        self.frame_2 = customtkinter.CTkFrame(master=self.root)
        self.frame_2.grid(row=4, column=2, padx=(40, 40), pady=(40, 40), sticky="nsew")
        
        # Viewer&Report Frame
        self.frame_3 = customtkinter.CTkFrame(master=self.root)
        self.frame_3.grid(row=4, column=3, padx=(40, 40), pady=(40, 40), sticky="nsew")
        
        self.calibration = customtkinter.CTkLabel(self.frame_1, text="CALIBRATION", font=("Nunito",15))
        self.calibration.grid(row=4, column=1, pady=10)
        self.measurement = customtkinter.CTkLabel(self.frame_2, text="MEASUREMENT", font=("Nunito",15))
        self.measurement.grid(row=4, column=2, pady=10)
        self.result = customtkinter.CTkLabel(self.frame_3, text="VIEWER & REPORTS", font=("Nunito",15))
        self.result.grid(row=4, column=3, pady=10)

        # CALIBRATION
        self.c1 = customtkinter.CTkButton(self.frame_1, text="KEMAR", font=("Ubuntu", 12))
        self.c1.grid(row=5, column=1, padx=(65, 65), pady=(5, 10))
        self.c2 = customtkinter.CTkButton(self.frame_1, text="Mic", font=("Ubuntu", 12))
        self.c2.grid(row=6, column=1, padx=(50, 50), pady=(5, 10))
        self.c3 = customtkinter.CTkButton(self.frame_1, text="Speaker", font=("Ubuntu", 12))
        self.c3.grid(row=7, column=1, padx=(50, 50), pady=(5, 10))
        self.c4 = customtkinter.CTkButton(self.frame_1, text="DUT Nominal", font=("Ubuntu", 12))
        self.c4.grid(row=8, column=1, padx=(50, 50), pady=(5, 10))
        self.c5 = customtkinter.CTkButton(self.frame_1, text="EQ Normalization", font=("Ubuntu", 12))
        self.c5.grid(row=9, column=1, padx=(50, 50), pady=(5, 15))

        # MEASUREMENT
        self.m1 = customtkinter.CTkButton(self.frame_2, text="Load JSON Script", font=("Ubuntu", 12), command=self.open_file)
        self.m1.grid(row=5, column=2, padx=(65, 65), pady=(5, 10))
        self.m1 = customtkinter.CTkButton(self.frame_2, text="Run JSON Script", font=("Ubuntu", 12))
        self.m1.grid(row=6, column=2, padx=(50, 50), pady=(5, 10))
        self.m1 = customtkinter.CTkButton(self.frame_2, text="Save Data", font=("Ubuntu", 12))
        self.m1.grid(row=7, column=2, padx=(50, 50), pady=(5, 10))

        # VIEWER & REPORT
        self.v1 = customtkinter.CTkButton(self.frame_3, text="Single Viewer", font=("Ubuntu", 12), command=plot)
        self.v1.grid(row=5, column=3, padx=(65, 65), pady=(5, 10))
        self.v2 = customtkinter.CTkButton(self.frame_3, text="Object Viewer", font=("Ubuntu", 12))
        self.v2.grid(row=6, column=3, padx=(50, 50), pady=(5, 10))
        self.v3 = customtkinter.CTkButton(self.frame_3, text="Data Comparison", font=("Ubuntu", 12))
        self.v3.grid(row=7, column=3, padx=(50, 50), pady=(5, 10))
        self.v4 = customtkinter.CTkButton(self.frame_3, text="Data Conversion", font=("Ubuntu", 12))
        self.v4.grid(row=8, column=3, padx=(50, 50), pady=(5, 10))
        self.gen = customtkinter.CTkButton(self.frame_3, text="Report Generator", font=("Ubuntu", 12),command=lambda:self.generator())
        self.gen.grid(row=9, column=3, padx=(50, 50), pady=(5, 15))
        
        # SOUND CONTROL
        self.label = customtkinter.CTkLabel(self.root, text="Volume Setting", font=("Nunito",15))
        self.label.grid(row=10, column=1)
        self.toggleBtn = customtkinter.CTkButton(self.root, border_width=2.5, border_color="red", text_color="red" , text="Mute Off", font=("Ubuntu", 12), command=self.toggle_mute)
        self.toggleBtn.grid(row=11, column=3)
        self.var = customtkinter.IntVar(value=getCurrentMasterVolume())
        self.scale = customtkinter.CTkSlider(self.root, from_=0, to=100, variable=self.var, command=setMasterVolume, orientation="horizontal", button_corner_radius=3, button_length=20)
        self.scale.grid(row=11, column=1)
        self.label = customtkinter.CTkLabel(self.root, font=("Nunito",15))
        self.label.configure(text=displayCurrentVolume())
        #self.label.grid(row=12, column=1)
        
    def open_file(self): # Method for load JSON file
        filetypes = [("Json File", "*.json")] 
        filenames = fd.askopenfilename(title="Open File", filetypes=filetypes)
        df = pd.read_json(filenames)
    
    def files(self): # Methon for load dir APx API
        self.foldername = filedialog.askdirectory(initialdir = "C:\Program Files\Audio Precision\APx500 8.0\API", title="C:\Program Files\Audio Precision\APx500 8.0\API")
        self.entry_folder.configure(text=self.foldername)

    def generator(self): # Child GUI for Report Generator
        self.report = tk.Toplevel(self.root)
        self.report.geometry("300x250")
        self.report.title("Report Generator")
        self.label_gen = customtkinter.CTkLabel(self.report, text="REPORT GENERATOR", font=("Nunito",15))
        self.label_gen.grid(row=1, column=1)

        # CHECKBOX
        self.cek1 = customtkinter.CTkRadioButton(self.report, text="Golden Sample Result",font=("Ubuntu", 12))
        self.cek1.grid(row=2, column=1)
        self.cek2 = customtkinter.CTkRadioButton(self.report, text="Curve Boundary",font=("Ubuntu", 12))
        self.cek2.grid(row=3, column=1)
        self.cek3 = customtkinter.CTkRadioButton(self.report, text="Value Tolerance",font=("Ubuntu", 12))
        self.cek3.grid(row=4, column=1)
        self.cek4 = customtkinter.CTkRadioButton(self.report, text="Pass/Fail",font=("Ubuntu", 12))
        self.cek4.grid(row=5, column=1)
        self.cek5 = customtkinter.CTkRadioButton(self.report, text="Statistical Table",font=("Ubuntu", 12))
        self.cek5.grid(row=6, column=1)
        

        self.button = customtkinter.CTkButton(self.report, text="Generate!", font=("Ubuntu", 12))
        self.button.grid(row=7, column=1, padx=(50, 50), pady=(5, 10))
    
    def toggle_mute(self): # to get the present state of the toggle button
        if self.toggleBtn.cget('text') == 'Mute Off':
            self.toggleBtn.configure(text='Mute On')
            mute(1)
        else:
            self.toggleBtn.configure(text='Mute Off')
            mute(0)

app = Myapp()
app.root.mainloop()