from tkinter import filedialog
import tkinter as tk
import os
from APP.Material import material
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Class to represent the GUI
class GUInstance():
    
    def __init__(self):
        
        # GUI variables
        self.root = None
        self.padxVal = 5
        self.padyVal = 5
        self.withVal = 15
        self.resolution = '650x200'
        
        # GUI Entries
        self.material_entry = None
        self.temperature_entry = None
        self.type_entry = None
        self.rate_entry = None
        self.manufacturer_entry = None
        self.poisson_entry = None
        self.caliButton = None
        self.engState = None
        self.trueState = None
        self.percState = None
        self.adiState = None
        self.graph = None
        
        # Material variables
        self.filePath = None
        self.materialName = None
        self.temperature = None
        self.type = None
        self.rate = None
        self.manufacturer = None
        self.poisson = None
        self.calibration = None
        
        
        
    # Get input file name and create the output file name
    def select_input_file(self) -> None:
            
        # Get file from dialog box 
        file_path = filedialog.askopenfilename(
            filetypes=[("Input Files", "*.xlsx")])
        
        # Add the path to the box in the GUI
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            
            # Get original file name
            output_file_name = os.path.basename(file_path).split('.')[0] + "_calibrated"
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_file_name)
    
    
    # Switch the options on the selection boxes
    def select_option(self, varState1: bool,
                            varState2: bool, 
                            option: int) -> None:
        if option == 1:
            varState1.set(True)
            varState2.set(False)
        else:
            varState1.set(False)
            varState2.set(True)
     
     
    # Save the values of the GUI into internal variables       
    def writeValues(self) -> None:
        self.filePath = str(self.input_entry.get())
        self.materialName = str(self.material_entry.get())
        self.temperature = float(self.temperature_entry.get())
        self.type = str(self.type_entry.get())
        self.rate = float(self.rate_entry.get())
        self.manufacturer = str(self.manufacturer_entry.get())
        self.poisson = float(self.poisson_entry.get())
        self.calibration = int(self.caliButton.get())
        
        
    # Preview the results of the calibration 
    def preview(self) -> None:
        self.writeValues()        
        myMaterial = material(self.filePath, self.calibration, self.adiState, self.engState)
        myMaterial.analyseData()
        self.graph = myMaterial.getGraph()
        canvas = FigureCanvasTkAgg(self.graph, master=self.root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=6, column=1)
        
    
    # Start the material calibration    
    def execute(self) -> None:
        self.writeValues()
        myMaterial = material(self.filePath, self.calibration, self.adiState, self.engState)
        myMaterial.analyseData() 
        myMaterial.writeExcelFile()  
        
    
    # Start the GUI
    def run(self) -> None:
        
        # GUI Object 
        self.root = tk.Tk()
        
        # GUI Title
        self.root.title('Material Calibrator')

        # Window resolution
        self.root.geometry('680x200')
        
        # Text Boxes
        output_label = tk.Label(self.root, text='Material Name:')
        output_label.grid(row=0, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.material_entry = tk.Entry(self.root, width=self.withVal)
        self.material_entry.grid(row=0, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Temperature:')
        output_label.grid(row=0, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.temperature_entry = tk.Entry(self.root, width=self.withVal)
        self.temperature_entry.grid(row=0, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Type:')
        output_label.grid(row=1, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.type_entry = tk.Entry(self.root, width=self.withVal)
        self.type_entry.grid(row=1, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Rate:')
        output_label.grid(row=1, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.rate_entry = tk.Entry(self.root, width=self.withVal)
        self.rate_entry.grid(row=1, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Manufacturer:')
        output_label.grid(row=2, column=0, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.manufacturer_entry = tk.Entry(self.root, width=self.withVal)
        self.manufacturer_entry.grid(row=2, column=2, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        output_label = tk.Label(self.root, text='Poisson:')
        output_label.grid(row=2, column=4, columnspan=2, padx=self.padxVal, pady=self.padyVal)
        self.poisson_entry = tk.Entry(self.root, width=self.withVal)
        self.poisson_entry.grid(row=2, column=6, columnspan=2, padx=self.padxVal, pady=self.padyVal)

        # Stress-True stress-strain options
        self.engState = tk.BooleanVar(value = True)
        self.trueState = tk.BooleanVar()

        engLabel = tk.Label(text='Engineering Curve', padx=self.padxVal, pady=self.padyVal)
        trueLabel = tk.Label(text='True Curve', padx=self.padxVal, pady=self.padyVal)

        engCheckBox = tk.Checkbutton(self.root, variable=self.engState, command=lambda: self.select_option(self.engState, self.trueState, 1))
        trueCheckBox = tk.Checkbutton(self.root, variable=self.trueState, command=lambda: self.select_option(self.engState, self.trueState, 2))

        engLabel.grid(row=3, column=0, padx=self.padxVal, pady=self.padyVal)
        trueLabel.grid(row=3, column=4, padx=self.padxVal, pady=self.padyVal)
        engCheckBox.grid(row=3, column=2, padx=self.padxVal, pady=self.padyVal)
        trueCheckBox.grid(row=3, column=6, padx=self.padxVal, pady=self.padyVal)

        # Strain variable options
        self.percState = tk.BooleanVar(value = True)
        self.adiState = tk.BooleanVar()

        percLabel = tk.Label(text='Strain(%)', padx=self.padxVal, pady=self.padyVal)
        adiLabel = tk.Label(text='Strain(-)', padx=self.padxVal, pady=self.padyVal)

        percCheckBox = tk.Checkbutton(self.root, variable=self.percState, command=lambda: self.select_option(self.percState, self.adiState, 1))
        adiCheckBox = tk.Checkbutton(self.root, variable=self.adiState, command=lambda: self.select_option(self.percState, self.adiState, 2))

        percLabel.grid(row=4, column=0, padx=self.padxVal, pady=self.padyVal)
        adiLabel.grid(row=4, column=4, padx=self.padxVal, pady=self.padyVal)
        percCheckBox.grid(row=4, column=2, padx=self.padxVal, pady=self.padyVal)
        adiCheckBox.grid(row=4, column=6, padx=self.padxVal, pady=self.padyVal)

        # Input/Output file Button 
        input_button = tk.Button(self.root, text='Select Input File', compound= 'left',command=self.select_input_file)
        input_button.grid(row=5 , column=0, padx=self.padxVal, pady=self.padyVal)
        self.input_entry = tk.Entry(self.root, width=(self.withVal*3))
        self.input_entry.grid(row=5, column=2,padx=self.padxVal, pady=self.padyVal)
        
        # Calibration button
        self.caliButton = tk.Spinbox(self.root, from_=1, to=100)
        self.caliButton.grid(row=5, column=4, padx=self.padxVal, pady=self.padyVal)
        
        # Preview button
        prevButton = tk.Button(self.root,command=self.preview, text='Preview', width=10)
        prevButton.grid(row=5, column=5, padx=self.padxVal, pady=self.padyVal)
        
        # Run button
        runButton = tk.Button(self.root, command=self.execute, text='Run', background='green')
        runButton.grid(row=5, column=6, padx=self.padxVal, pady=self.padyVal)

        self.root.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.root.grid_columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        # Start GUI
        self.root.mainloop()

        
        